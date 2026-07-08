import os
import sys
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from typing import Tuple, Dict, Any

# Ensure root directory is in python path to resolve 'app' imports
current_dir = os.path.dirname(os.path.abspath(__file__))
while current_dir and not os.path.exists(os.path.join(current_dir, 'app')):
    parent = os.path.dirname(current_dir)
    if parent == current_dir:
        break
    current_dir = parent
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app.components.styles import inject_premium_styles
from app.components.cards import render_verdict_card, render_insight_card
from app.utils.validators import validate_numeric_inputs
from app.utils.export import generate_csv_report, generate_text_report, generate_pdf_report
from app.services.history_service import HistoryService

# 1. Dynamic de-serialization wrapper cached via Streamlit
@st.cache_resource
def load_ml_pipeline() -> Tuple[Any, Any, Any, Dict[str, Any]]:
    model_path = os.path.join('models', 'model.pkl')
    scaler_path = os.path.join('models', 'scaler.pkl')
    features_path = os.path.join('models', 'feature_names.pkl')
    encoder_path = os.path.join('models', 'label_encoder.pkl')
    
    if not (os.path.exists(model_path) and os.path.exists(scaler_path)):
        raise FileNotFoundError("Model serialization files missing in models/ directory.")
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(features_path)
    binary_mappings = joblib.load(encoder_path)
    return model, scaler, feature_names, binary_mappings

# Inject premium dark styles
inject_premium_styles()

st.markdown("<h1 class='glowing-title gradient-text'>🔮 Churn Predictor Wizard</h1>", unsafe_allow_html=True)
st.markdown("Enter customer details below in the 3-column profile layout to evaluate churn risk indicators in real time.")

# Load serialized model assets
try:
    model, scaler, feature_names, binary_mappings = load_ml_pipeline()
    history_logger = HistoryService()
except Exception as e:
    st.error(f"Failed to load machine learning assets: {e}")
    st.stop()

# Initialize session state for logging history
if 'prediction_ran' not in st.session_state:
    st.session_state.prediction_ran = False
if 'last_inputs' not in st.session_state:
    st.session_state.last_inputs = {}
if 'last_result' not in st.session_state:
    st.session_state.last_result = {}

# 2. 3-COLUMN INTERACTIVE INPUT FORM LAYOUT
st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
st.subheader("⚙️ Customer Account Profile Inputs")

col_dem, col_ser, col_acc = st.columns(3)

with col_dem:
    st.markdown("<h4 style='color:#6C63FF; margin-top:0;'>👤 Demographics</h4>", unsafe_allow_html=True)
    gender = st.selectbox("Gender", ["Female", "Male"], index=0)
    senior_citizen = st.selectbox("Senior Citizen Status", ["No", "Yes"], index=0)
    partner = st.selectbox("Has a Partner?", ["No", "Yes"], index=0)
    dependents = st.selectbox("Has Dependents?", ["No", "Yes"], index=0)

with col_ser:
    st.markdown("<h4 style='color:#00D4AA; margin-top:0;'>📶 Active Services</h4>", unsafe_allow_html=True)
    phone_service = st.selectbox("Phone Service Subscribed?", ["No", "Yes"], index=1)
    multiple_lines = st.selectbox("Multiple Lines Configuration", ["No", "Yes", "No phone service"], index=0)
    internet_service = st.selectbox("Internet Service Provider Type", ["DSL", "Fiber optic", "No"], index=1)
    online_security = st.selectbox("Online Security Add-on?", ["No", "Yes", "No internet service"], index=0)
    online_backup = st.selectbox("Online Backup Add-on?", ["No", "Yes", "No internet service"], index=0)
    device_protection = st.selectbox("Device Protection Add-on?", ["No", "Yes", "No internet service"], index=0)
    tech_support = st.selectbox("Tech Support Add-on?", ["No", "Yes", "No internet service"], index=0)
    streaming_tv = st.selectbox("Streaming TV Service?", ["No", "Yes", "No internet service"], index=0)
    streaming_movies = st.selectbox("Streaming Movies Service?", ["No", "Yes", "No internet service"], index=0)

with col_acc:
    st.markdown("<h4 style='color:#FFB347; margin-top:0;'>💳 Financials & Account</h4>", unsafe_allow_html=True)
    tenure = st.slider("Tenure (Active Months)", min_value=0, max_value=72, value=12)
    contract = st.selectbox("Contract Agreement Type", ["Month-to-month", "One year", "Two year"], index=0)
    paperless = st.selectbox("Paperless Billing Active?", ["No", "Yes"], index=1)
    payment_method = st.selectbox(
        "Active Payment Method Channel", 
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], 
        index=0
    )
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=65.0, step=0.5)
    
    # Dynamically estimate total charges as Tenure * Monthly Charges, but allow manual overrides
    calculated_total = float(tenure * monthly_charges) if tenure > 0 else 0.0
    total_charges = st.number_input(
        "Total Charges ($)", 
        min_value=0.0, 
        max_value=15000.0, 
        value=calculated_total, 
        step=10.0,
        help="Estimated based on current monthly charges and tenure. Override if necessary."
    )

st.markdown('</div>', unsafe_allow_html=True)

# Action validation trigger
if st.button("🔮 Analyze Customer Risk Profile", use_container_width=True):
    # Perform numeric boundaries validation
    is_valid, error_msg = validate_numeric_inputs(tenure, monthly_charges, total_charges)
    
    if not is_valid:
        st.error(error_msg)
    else:
        # Save validated selections in dict
        input_data = {
            'gender': gender,
            'SeniorCitizen': 1 if senior_citizen == "Yes" else 0,
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': phone_service,
            'MultipleLines': multiple_lines,
            'InternetService': internet_service,
            'OnlineSecurity': online_security,
            'OnlineBackup': online_backup,
            'DeviceProtection': device_protection,
            'TechSupport': tech_support,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'Contract': contract,
            'PaperlessBilling': paperless,
            'PaymentMethod': payment_method,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges
        }
        
        # 3. PREPROCESSING PIPELINE
        input_df = pd.DataFrame([input_data])
        
        # Map binary categories mapped via serialization encoder
        for col, mapping in binary_mappings.items():
            if col in input_df.columns:
                input_df[col] = input_df[col].map(mapping)
                
        # Handle multi-class category columns mapping dummies
        categorical_cols = [
            'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
            'Contract', 'PaymentMethod'
        ]
        input_df = pd.get_dummies(input_df, columns=categorical_cols)
        
        # Re-index columns layout to match fit format
        input_df = input_df.reindex(columns=feature_names, fill_value=0)
        
        # Scale continuous features
        num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
        input_df[num_cols] = scaler.transform(input_df[num_cols])
        input_df = input_df.astype(float)
        
        # Execute Logistic Regression prediction
        prediction = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0][1])
        
        # Assess risk levels
        if probability < 0.3:
            risk_level = 'Low'
        elif probability < 0.6:
            risk_level = 'Medium'
        elif probability < 0.8:
            risk_level = 'High'
        else:
            risk_level = 'Critical'
            
        confidence_val = abs(probability - 0.5) * 2.0
        confidence = 'High' if confidence_val > 0.7 else ('Moderate' if confidence_val > 0.3 else 'Low')
        
        # 4. RIGHT COLUMN EXPLAINABILITY: Calculate Log-Odds contributions (Weight * Scaled Input)
        coefficients = model.coef_[0]
        feature_vals = input_df.iloc[0].values
        
        contributions = {}
        for name, coef, val in zip(feature_names, coefficients, feature_vals):
            cont_val = float(coef * val)
            if abs(cont_val) > 0.001:
                contributions[name] = cont_val
                
        # Sort features pushing toward churn (positive log-odds values)
        sorted_contributions = sorted(
            [(feat, val) for feat, val in contributions.items() if val > 0], 
            key=lambda x: x[1], 
            reverse=True
        )
        
        result = {
            'prediction': prediction,
            'probability': probability,
            'risk_level': risk_level,
            'confidence': confidence,
            'contributions': dict(sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True))
        }
        
        # Append record to csv history
        history_logger.append_record(input_data, result)
        
        # Store in session state
        st.session_state.prediction_ran = True
        st.session_state.last_inputs = input_data
        st.session_state.last_result = result
        st.session_state.sorted_pos_contributions = sorted_contributions

# ----------------- REAL-TIME DIAGNOSTIC PRESENTATION -----------------
if st.session_state.prediction_ran:
    inputs = st.session_state.last_inputs
    res = st.session_state.last_result
    sorted_pos = st.session_state.sorted_pos_contributions
    
    prob = res['probability']
    risk_level = res['risk_level']
    pred = res['prediction']
    conf = res['confidence']
    
    # Custom colored banner
    render_verdict_card(prob, risk_level, pred, conf)
    
    out_col1, out_col2 = st.columns(2)
    
    with out_col1:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.subheader("🎯 Risk Score Assessment")
        
        # Premium color gauge plotting
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                'bar': {'color': "#6C63FF", 'thickness': 0.3},
                'bgcolor': "rgba(26, 29, 46, 0.5)",
                'borderwidth': 2,
                'bordercolor': "rgba(108, 99, 255, 0.2)",
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(0, 212, 170, 0.2)'},
                    {'range': [30, 70], 'color': 'rgba(255, 179, 71, 0.2)'},
                    {'range': [70, 100], 'color': 'rgba(255, 107, 107, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': "#FF6B6B", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E2E8F0"),
            margin=dict(l=20, r=20, t=30, b=20),
            height=250
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
        
    with out_col2:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.subheader("🧬 Local Churn Driver Contributions")
        st.write("Top parameters contributing positively to customer attrition probability (Log-Odds weights):")
        
        # Display top 3 features driving churn
        if sorted_pos:
            for i, (feat, val) in enumerate(sorted_pos[:3]):
                clean_name = feat.replace('_', ' ').title()
                st.markdown(
                    f"""
                    <div style="background: rgba(255, 107, 107, 0.05); border: 1px solid rgba(255, 107, 107, 0.2); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight:600; color:#E2E8F0;">{i+1}. {clean_name}</span>
                        <span style="color:#FF6B6B; font-weight:700;">+{val:.3f} log-odds</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.write("✓ No features are positively pushing this customer towards churn.")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 5. WHAT-IF / PRESCRIPTIVE ANALYTICS SECTION
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    st.subheader("💡 Prescriptive Retention Playbook")
    
    recs = []
    
    # 1. Month-to-month contracts check
    if inputs.get('Contract') == 'Month-to-month':
        recs.append((
            "📅 Migrate Month-to-Month Cohorts",
            "This account is on a month-to-month contract. Offer a 10% monthly discount bundle "
            "if they transition to an annual contract plan to significantly secure client lifecycle value (CLV)."
        ))
        
    # 2. Fiber Optic check with tech support
    if inputs.get('InternetService') == 'Fiber optic' and inputs.get('TechSupport') != 'Yes':
        recs.append((
            "📶 Fiber Optic Support Bundling",
            "Subscribed to Fiber Optic internet without Online Tech Support. Fiber optic lines show higher friction "
            "rates; offer a bundled Tech Support add-on at a 50% discount to stabilize service satisfaction."
        ))
        
    # 3. Payment Method electronic check friction check
    if inputs.get('PaymentMethod') == 'Electronic check':
        recs.append((
            "💳 Automate Payment Methods",
            "Active payment channel is Electronic Check. Incentivize migrating to bank transfer auto-pay "
            "or Credit Card auto-pay configurations by offering a one-time $5 statement billing credit."
        ))
        
    # 4. Price sensitivity vs Low tenure checks
    if inputs.get('tenure', 0) <= 12 and inputs.get('MonthlyCharges', 0.0) >= 80.0:
        recs.append((
            "💵 High-Value New Cohort Onboarding",
            "Customer is in their initial onboarding phase (tenure <= 12m) with billing charges >= $80.00. "
            "Schedule a direct customer success callback check-in to confirm network reliability and satisfaction."
        ))
        
    # 5. Online Security add-on missing check
    if inputs.get('OnlineSecurity') != 'Yes' and inputs.get('InternetService') != 'No':
        recs.append((
            "🔐 Proactive Security Promotion",
            "Active internet service is configured without Online Security. Promote active online security bundles "
            "to increase customer account locking."
        ))
        
    if not recs:
        # Fallback for very low risk profiles
        st.success("✓ Customer risk profile is solid. Maintain default billing quality service check-ins.")
    else:
        # Render dynamic recommendations
        for title, desc in recs[:3]:
            render_insight_card(title, desc, "danger" if risk_level in ['High', 'Critical'] else "warning")
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Report exporter utilities
    st.markdown("### 📥 Download Risk Assessment Artifacts")
    
    csv_bytes = generate_csv_report(inputs, res)
    txt_report = generate_text_report(inputs, res)
    pdf_bytes = generate_pdf_report(inputs, res)
    
    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        st.download_button(
            label="📥 Download CSV Summary Data",
            data=csv_bytes,
            file_name=f"churn_prediction_{inputs.get('gender')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with d_col2:
        st.download_button(
            label="📥 Download TXT Diagnostics Report",
            data=txt_report,
            file_name=f"churn_diagnostic_report_{inputs.get('tenure')}m.txt",
            mime="text/plain",
            use_container_width=True
        )
    with d_col3:
        st.download_button(
            label="📥 Download PDF Enterprise Report",
            data=pdf_bytes,
            file_name="churn_assessment_pdf_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
