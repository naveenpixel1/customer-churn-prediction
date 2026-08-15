import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import logging
from typing import Dict, Any, Tuple
from app.utils.config import MODEL_DIR
from app.utils.security import validate_prediction_input

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FEATURE_LABEL_MAP = {
    'tenure': 'Tenure (Active Months)',
    'MonthlyCharges': 'Monthly Billing Charges',
    'TotalCharges': 'Total Lifetime Charges',
    'SeniorCitizen': 'Senior Citizen Status',
    'Partner': 'Partner Subscribed',
    'Dependents': 'Dependents Subscribed',
    'PaperlessBilling': 'Paperless Billing',
    'PhoneService': 'Phone Service Active',
    'MultipleLines_Yes': 'Multiple Phone Lines',
    'MultipleLines_No phone service': 'No Phone Line Subscribed',
    'InternetService_Fiber optic': 'Fiber Optic Service',
    'InternetService_No': 'No Internet Service',
    'OnlineSecurity_Yes': 'Has Online Security',
    'OnlineSecurity_No internet service': 'No Internet Security Required',
    'OnlineBackup_Yes': 'Has Online Backup',
    'OnlineBackup_No internet service': 'No Internet Backup Required',
    'DeviceProtection_Yes': 'Has Device Protection',
    'DeviceProtection_No internet service': 'No Internet Device Protection Required',
    'TechSupport_Yes': 'Has Tech Support',
    'TechSupport_No internet service': 'No Internet Tech Support Required',
    'StreamingTV_Yes': 'Streaming TV Active',
    'StreamingTV_No internet service': 'No Internet Streaming TV Required',
    'StreamingMovies_Yes': 'Streaming Movies Active',
    'StreamingMovies_No internet service': 'No Internet Streaming Movies Required',
    'Contract_One year': 'One-Year Contract',
    'Contract_Two year': 'Two-Year Contract',
    'Contract_Month-to-month': 'Month-to-Month Contract',
    'PaymentMethod_Credit card (automatic)': 'Automatic Credit Card Pay',
    'PaymentMethod_Electronic check': 'Electronic Check Payment',
    'PaymentMethod_Mailed check': 'Mailed Check Payment',
    'gender': 'Gender Profile',
    'Tenure_To_Monthly_Ratio': 'Tenure to Monthly Ratio',
    'TotalCharges_Per_Month': 'Historical Total Charges per Month',
    'Service_Count': 'Total Active Service Add-ons',
    'Has_Anchor_Service': 'Has Anchor Security/Tech Support'
}

def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + np.exp(-z))

def explain_customer_prediction(
    model: Any, 
    scaler: Any, 
    feature_names: list, 
    input_df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Calculates instance-level feature contributions using Logistic Regression Log-Odds Impact
    or Tree Feature Importances, converting them to percentage point probability impacts (ΔP_i).
    """
    if hasattr(model, 'coef_'):
        coefficients = model.coef_[0]
        intercept = getattr(model, 'intercept_', [0.0])[0]
        feature_vals = input_df.iloc[0].values
        log_odds_impacts = coefficients * feature_vals
        logit_total = float(np.sum(log_odds_impacts) + intercept)
        prob_total = float(sigmoid(logit_total))
        
        explanations = []
        for col, coef, val, impact in zip(feature_names, coefficients, feature_vals, log_odds_impacts):
            if abs(val) < 1e-6 and abs(impact) < 1e-6:
                continue
                
            prob_without_i = sigmoid(logit_total - impact)
            delta_p = prob_total - prob_without_i
            delta_p_pct = float(delta_p * 100.0)
            
            label = FEATURE_LABEL_MAP.get(col, col.replace('_', ' ').title())
            
            explanations.append({
                'feature_raw': col,
                'label': label,
                'value': float(val),
                'coefficient': float(coef),
                'log_odds_impact': float(impact),
                'prob_impact_pct': delta_p_pct
            })
    elif hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        prob_total = float(model.predict_proba(input_df)[0][1])
        feature_vals = input_df.iloc[0].values
        logit_total = 0.0
        explanations = []
        for col, imp, val in zip(feature_names, importances, feature_vals):
            if abs(val) < 1e-6 and abs(imp) < 1e-6:
                continue
            label = FEATURE_LABEL_MAP.get(col, col.replace('_', ' ').title())
            delta_p_pct = float(imp * val * 100.0 * (1 if val > 0 else -1))
            explanations.append({
                'feature_raw': col,
                'label': label,
                'value': float(val),
                'coefficient': float(imp),
                'log_odds_impact': float(imp * val),
                'prob_impact_pct': delta_p_pct
            })
    else:
        prob_total = float(model.predict_proba(input_df)[0][1])
        logit_total = 0.0
        explanations = []
        
    risk_drivers = sorted([e for e in explanations if e['prob_impact_pct'] > 0.01], key=lambda x: x['prob_impact_pct'], reverse=True)
    mitigating_drivers = sorted([e for e in explanations if e['prob_impact_pct'] < -0.01], key=lambda x: x['prob_impact_pct'])
    
    return {
        'total_probability': prob_total,
        'logit_total': logit_total,
        'top_risk_drivers': risk_drivers[:3],
        'top_mitigating_drivers': mitigating_drivers[:3],
        'all_explanations': sorted(explanations, key=lambda x: abs(x['prob_impact_pct']), reverse=True)
    }

class PredictionService:
    _model = None
    _scaler = None
    _feature_names = None
    _binary_mappings = None

    @classmethod
    @st.cache_resource
    def load_pipeline(cls) -> Tuple[Any, Any, Any, Dict[str, Any]]:
        try:
            model = joblib.load(os.path.join(MODEL_DIR, 'model.pkl'))
            scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
            feature_names = joblib.load(os.path.join(MODEL_DIR, 'feature_names.pkl'))
            binary_mappings = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.pkl'))
            logger.info('Successfully loaded ML model pipeline assets from disk.')
            return model, scaler, feature_names, binary_mappings
        except Exception as e:
            logger.error(f'Error loading model pipeline: {e}')
            raise e

    def __init__(self):
        self.model, self.scaler, self.feature_names, self.binary_mappings = self.load_pipeline()
        
        missing_labels = [f for f in self.feature_names if f not in FEATURE_LABEL_MAP]
        if missing_labels:
            logger.warning(f"FEATURE_LABEL_MAP is missing entries for: {missing_labels}")

    def predict(self, input_data: Dict[str, Any], threshold: float = 0.35) -> Dict[str, Any]:
        # 0. Server-side input validation (Item #8, #14)
        is_valid, error_msg = validate_prediction_input(input_data)
        if not is_valid:
            raise ValueError(f"Input validation failed: {error_msg}")

        # 1. Create DataFrame
        input_df = pd.DataFrame([input_data])

        # 2. Map Binary Categorical Columns (Label Encoding mapping)
        for col, mapping in self.binary_mappings.items():
            if col in input_df.columns:
                input_df[col] = input_df[col].map(mapping)

        # 3. Special handling for SeniorCitizen: if it is a string ('Senior Citizen' or 'Non-Senior'), map to 1/0
        if 'SeniorCitizen' in input_df.columns:
            if isinstance(input_df['SeniorCitizen'].iloc[0], str):
                input_df['SeniorCitizen'] = 1 if input_df['SeniorCitizen'].iloc[0] == 'Senior Citizen' else 0

        # 3b. Engineer derived features
        monthly = float(input_data.get('MonthlyCharges', 0.0))
        tenure = float(input_data.get('tenure', 0.0))
        total_chg = float(input_data.get('TotalCharges', monthly * tenure))
        
        input_df['Tenure_To_Monthly_Ratio'] = tenure / (monthly + 1e-5)
        input_df['TotalCharges_Per_Month'] = total_chg / (tenure + 1.0)
        
        service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
        input_df['Service_Count'] = sum(1 for c in service_cols if str(input_data.get(c, '')).lower() in ['yes', '1', 1])
        input_df['Has_Anchor_Service'] = 1 if (str(input_data.get('OnlineSecurity', '')).lower() == 'yes' or str(input_data.get('TechSupport', '')).lower() == 'yes') else 0

        # 4. Apply One-Hot Encoding to Multi-class Categorical columns
        categorical_cols = [
            'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
            'Contract', 'PaymentMethod'
        ]
        # Only keep categorical cols that are actually in input_df
        existing_cat_cols = [c for c in categorical_cols if c in input_df.columns]
        input_df = pd.get_dummies(input_df, columns=existing_cat_cols)

        # 5. Reindex columns using saved feature names layout
        input_df = input_df.reindex(columns=self.feature_names, fill_value=0)

        # 6. Scale Numerical features
        potential_num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Tenure_To_Monthly_Ratio', 'TotalCharges_Per_Month', 'Service_Count']
        num_cols = [c for c in potential_num_cols if c in input_df.columns]
        input_df[num_cols] = self.scaler.transform(input_df[num_cols])
        input_df = input_df.astype(float)

        # 7. Model Inference with custom decision threshold
        probability = float(self.model.predict_proba(input_df)[0][1])
        
        # Domain rule: Brand new customers (tenure = 0) on multi-year/annual contracts with auto-pay/security are low risk
        if tenure == 0 and input_data.get('Contract') in ['Two year', 'One year']:
            probability = min(probability, threshold * 0.4)

        prediction = int(probability >= threshold)

        # 8. Define Risk Level and Confidence relative to threshold
        if probability < (threshold * 0.75):
            risk_level = 'Low'
        elif probability < threshold:
            risk_level = 'Medium'
        elif probability < (threshold + (1.0 - threshold) * 0.5):
            risk_level = 'High'
        else:
            risk_level = 'Critical'

        confidence_val = abs(probability - threshold) * 2.0
        if confidence_val > 0.6:
            confidence = 'High'
        elif confidence_val > 0.2:
            confidence = 'Moderate'
        else:
            confidence = 'Low'

        # 9. CLV & Priority Action Tier Calculation
        clv = self.calculate_clv(monthly, tenure)
        priority_tier = self.get_customer_priority_tier(probability, clv)
        potential_loss = clv if probability >= threshold else 0.0

        # 10. Key drivers & Instance-level Feature Interpretability Explanation
        if hasattr(self.model, 'coef_'):
            coefficients = self.model.coef_[0]
        elif hasattr(self.model, 'feature_importances_'):
            coefficients = self.model.feature_importances_
        else:
            coefficients = np.zeros(len(self.feature_names))

        contributions = {}
        for col, coef in zip(self.feature_names, coefficients):
            val = input_df[col].iloc[0]
            contrib = coef * val
            if abs(contrib) > 0.01:
                contributions[col] = float(contrib)

        sorted_contributions = dict(sorted(contributions.items(), key=lambda item: abs(item[1]), reverse=True))
        explanation_data = explain_customer_prediction(self.model, self.scaler, self.feature_names, input_df)

        result = {
            'prediction': prediction,
            'probability': probability,
            'threshold': threshold,
            'risk_level': risk_level,
            'confidence': confidence,
            'clv': clv,
            'potential_loss': potential_loss,
            'priority_tier': priority_tier,
            'contributions': sorted_contributions,
            'explanation': explanation_data
        }

        logger.info(f'Generated prediction probability: {probability:.4f} (threshold: {threshold:.2f}) | Risk level: {risk_level}')
        return result

    @staticmethod
    def predict_with_threshold(model: Any, X_scaled: np.ndarray, threshold: float = 0.35) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates probabilities and threshold predictions for scaled features array."""
        y_prob = model.predict_proba(X_scaled)[:, 1]
        y_pred = (y_prob >= threshold).astype(int)
        return y_pred, y_prob

    def simulate_retention_impact(
        self, 
        base_input_data: Dict[str, Any], 
        modifications_dict: Dict[str, Any], 
        threshold: float = 0.35
    ) -> Dict[str, Any]:
        """
        Simulates customer churn risk changes when retention offers (contract switch, add-ons, monthly discount) are applied.
        """
        sim_data = base_input_data.copy()
        
        if 'Contract' in modifications_dict:
            sim_data['Contract'] = modifications_dict['Contract']
        if 'TechSupport' in modifications_dict:
            sim_data['TechSupport'] = modifications_dict['TechSupport']
        if 'OnlineSecurity' in modifications_dict:
            sim_data['OnlineSecurity'] = modifications_dict['OnlineSecurity']
        if 'MonthlyDiscount' in modifications_dict:
            discount = float(modifications_dict['MonthlyDiscount'])
            base_charge = float(base_input_data.get('MonthlyCharges', 0.0))
            new_charge = max(0.0, base_charge - discount)
            sim_data['MonthlyCharges'] = new_charge
            tenure = float(sim_data.get('tenure', 0))
            sim_data['TotalCharges'] = max(0.0, tenure * new_charge) if tenure > 0 else 0.0
            
        base_result = self.predict(base_input_data, threshold=threshold)
        sim_result = self.predict(sim_data, threshold=threshold)
        
        orig_prob = base_result['probability']
        sim_prob = sim_result['probability']
        reduction = (orig_prob - sim_prob) * 100.0
        
        return {
            'original_prob': orig_prob,
            'simulated_prob': sim_prob,
            'risk_reduction_pct': float(reduction),
            'original_risk_level': base_result['risk_level'],
            'simulated_risk_level': sim_result['risk_level'],
            'original_prediction': base_result['prediction'],
            'simulated_prediction': sim_result['prediction'],
            'simulated_result': sim_result,
            'is_effective': sim_prob < threshold or reduction > 5.0
        }

    @staticmethod
    def evaluate_threshold_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.35) -> Dict[str, Any]:
        y_pred = (y_prob >= threshold).astype(int)
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        acc = float(accuracy_score(y_true, y_pred))
        prec = float(precision_score(y_true, y_pred, zero_division=0))
        rec = float(recall_score(y_true, y_pred, zero_division=0))
        f1 = float(f1_score(y_true, y_pred, zero_division=0))
        
        return {
            'threshold': threshold,
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'confusion_matrix': cm,
            'tn': int(tn),
            'fp': int(fp),
            'fn': int(fn),
            'tp': int(tp)
        }

    @staticmethod
    def calculate_clv(monthly_charges: float, tenure: float) -> float:
        """
        Calculates expected Customer Lifetime Value (CLV):
        Baseline CLV = MonthlyCharges * max(tenure, 12) * 1.25
        """
        months = max(float(tenure), 12.0)
        return float(monthly_charges * months * 1.25)

    @staticmethod
    def get_customer_priority_tier(probability: float, clv: float) -> Dict[str, str]:
        """
        Assigns priority intervention tier based on risk probability and Customer Lifetime Value (CLV).
        """
        if probability >= 0.35 and clv >= 1200.0:
            return {
                'tier': 'Tier 1 - Critical VIP Retention',
                'color': '#DC2626',
                'bg': '#FEF2F2',
                'action': 'Immediate Concierge Retention Call & Custom Loyalty Discount ($15/mo)'
            }
        elif probability >= 0.35:
            return {
                'tier': 'Tier 2 - High Risk Standard',
                'color': '#EA580C',
                'bg': '#FFEDD5',
                'action': 'Automated In-App Offer & Annual Contract Upgrade Discount'
            }
        elif probability >= 0.20:
            return {
                'tier': 'Tier 3 - Watchlist Account',
                'color': '#D97706',
                'bg': '#FFFBEB',
                'action': 'Promotional Add-on Bundle (Security / Tech Support 3 Months Free)'
            }
        else:
            return {
                'tier': 'Tier 4 - Stable Customer',
                'color': '#0D9488',
                'bg': '#F0FDF4',
                'action': 'Standard Monthly Check-in & Loyalty Points Newsletter'
            }



