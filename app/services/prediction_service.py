import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import logging
from typing import Dict, Any, Tuple
from app.utils.config import MODEL_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
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
        num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
        input_df[num_cols] = self.scaler.transform(input_df[num_cols])
        input_df = input_df.astype(float)

        # 7. Model Inference
        prediction = int(self.model.predict(input_df)[0])
        probability = float(self.model.predict_proba(input_df)[0][1])

        # 8. Define Risk Level and Confidence
        if probability < 0.3:
            risk_level = 'Low'
        elif probability < 0.6:
            risk_level = 'Medium'
        elif probability < 0.8:
            risk_level = 'High'
        else:
            risk_level = 'Critical'

        confidence_val = abs(probability - 0.5) * 2.0
        if confidence_val > 0.7:
            confidence = 'High'
        elif confidence_val > 0.3:
            confidence = 'Moderate'
        else:
            confidence = 'Low'

        # 9. Key drivers (Feature Importance contributions for this prediction)
        coefficients = self.model.coef_[0]
        contributions = {}
        for col, coef in zip(self.feature_names, coefficients):
            val = input_df[col].iloc[0]
            contrib = coef * val
            if abs(contrib) > 0.01:
                contributions[col] = float(contrib)

        sorted_contributions = dict(sorted(contributions.items(), key=lambda item: abs(item[1]), reverse=True))

        result = {
            'prediction': prediction,
            'probability': probability,
            'risk_level': risk_level,
            'confidence': confidence,
            'contributions': sorted_contributions
        }

        logger.info(f'Generated prediction probability: {probability:.4f} | Risk level: {risk_level}')
        return result
