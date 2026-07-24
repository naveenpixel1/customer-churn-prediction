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
from app.services.prediction_service import PredictionService


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

with st.container(border=True):
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
        
        # Execute Prediction via PredictionService with active decision threshold
        active_threshold = float(st.session_state.get('decision_threshold', 0.35))
        pred_service = PredictionService()
        result = pred_service.predict(input_data, threshold=active_threshold)
        
        prediction = result['prediction']
        probability = result['probability']
        risk_level = result['risk_level']
        confidence = result['confidence']
        contributions = result['contributions']
        
        # Sort features pushing toward churn (positive log-odds values)
        sorted_contributions = sorted(
            [(feat, val) for feat, val in contributions.items() if val > 0], 
            key=lambda x: x[1], 
            reverse=True
        )
        
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
    thresh = res.get('threshold', 0.35)
    
    # Custom colored banner
    render_verdict_card(prob, risk_level, pred, conf)
    st.caption(f"🎯 Operating Decision Threshold: **{thresh:.2f}** | Probability Cut-off for Churn Classification")
    
    # Risk Score Assessment Container
    with st.container(border=True):
        st.subheader("🎯 Risk Score Assessment Gauge")
        
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
                    'value': thresh * 100
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E2E8F0"),
            margin=dict(l=20, r=20, t=30, b=20),
            height=230
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    # 🔍 INDIVIDUAL RISK DRIVER ANALYSIS (2-COLUMN BREAKDOWN)
    st.markdown("### 🔍 Individual Risk Driver Analysis")
    st.markdown("Instance-level feature interpretability breakdown comparing top risk factors pushing towards churn (🔴) against protective factors supporting retention (🟢):")
    
    exp_data = res.get('explanation', {})
    risk_drivers = exp_data.get('top_risk_drivers', [])
    mitigating_drivers = exp_data.get('top_mitigating_drivers', [])
    
    col_risk, col_prot = st.columns(2)
    
    with col_risk:
        with st.container(border=True):
            st.markdown("<h4 style='color:#FF6B6B; margin-top:0;'>🔴 Top Churn Risk Drivers</h4>", unsafe_allow_html=True)
            if risk_drivers:
                for item in risk_drivers[:3]:
                    label = item['label']
                    pct = item['prob_impact_pct']
                    st.markdown(
                        f"""
                        <div style="background: rgba(255, 107, 107, 0.08); border: 1px solid rgba(255, 107, 107, 0.3); border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight:600; color:#E2E8F0;">🔴 {label}</span>
                            <span style="color:#FF6B6B; font-weight:700; background: rgba(255, 107, 107, 0.2); padding: 3px 8px; border-radius: 4px;">+{pct:.1f}% churn risk</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("✓ No significant parameters actively driving churn risk for this account.")
                
    with col_prot:
        with st.container(border=True):
            st.markdown("<h4 style='color:#00D4AA; margin-top:0;'>🟢 Protective / Retention Factors</h4>", unsafe_allow_html=True)
            if mitigating_drivers:
                for item in mitigating_drivers[:3]:
                    label = item['label']
                    pct = item['prob_impact_pct']
                    st.markdown(
                        f"""
                        <div style="background: rgba(0, 212, 170, 0.08); border: 1px solid rgba(0, 212, 170, 0.3); border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight:600; color:#E2E8F0;">🟢 {label}</span>
                            <span style="color:#00D4AA; font-weight:700; background: rgba(0, 212, 170, 0.2); padding: 3px 8px; border-radius: 4px;">{pct:.1f}% churn risk</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("✓ No strong protective features identified for this customer profile.")

    # 5. WHAT-IF RETENTION STRATEGY SIMULATOR
    with st.container(border=True):
        st.subheader("🛠️ What-If Retention Strategy Simulator")
        st.markdown(
            "Simulate retention offers in real time (contract upgrades, add-ons, monthly discounts) "
            "and observe the impact on customer churn risk probability."
        )
        
        sim_col1, sim_col2 = st.columns([1, 1])
        
        with sim_col1:
            st.markdown("##### ⚙️ Test Retention Offers")
            current_contract = inputs.get('Contract', 'Month-to-month')
            contract_opts = ["Month-to-month", "One year", "Two year"]
            c_index = contract_opts.index(current_contract) if current_contract in contract_opts else 0
            
            sim_contract = st.selectbox(
                "Contract Switch Offer", 
                contract_opts, 
                index=c_index
            )
            sim_tech_support = st.checkbox("Include Tech Support Add-on", value=(inputs.get('TechSupport') == 'Yes'))
            sim_security = st.checkbox("Include Online Security Add-on", value=(inputs.get('OnlineSecurity') == 'Yes'))
            sim_discount = st.slider("Monthly Billing Discount ($)", min_value=0.0, max_value=30.0, value=0.0, step=1.0)
            
        with sim_col2:
            st.markdown("##### 📊 Real-Time Impact Assessment")
            modifications = {
                'Contract': sim_contract,
                'TechSupport': 'Yes' if sim_tech_support else 'No',
                'OnlineSecurity': 'Yes' if sim_security else 'No',
                'MonthlyDiscount': sim_discount
            }
            
            sim_res = pred_service.simulate_retention_impact(inputs, modifications, threshold=thresh)
            
            orig_p = sim_res['original_prob']
            sim_p = sim_res['simulated_prob']
            red_pct = sim_res['risk_reduction_pct']
            
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 16px; margin-top: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: #94A3B8;">🔴 Original Churn Risk:</span>
                        <span style="font-weight: 700; color: #FF6B6B;">{orig_p:.1%}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: #94A3B8;">🟢 Simulated Churn Risk:</span>
                        <span style="font-weight: 700; color: {'#00D4AA' if sim_p < thresh else '#FFB347'};">{sim_p:.1%}</span>
                    </div>
                    <hr style="border-color: rgba(255, 255, 255, 0.1); margin: 10px 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: 600; color: #E2E8F0;">📉 Net Risk Reduction:</span>
                        <span style="font-weight: 700; color: {'#00D4AA' if red_pct > 0 else '#94A3B8'};">-{red_pct:.1f}%</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            if sim_p < thresh:
                st.success(f"🎉 **Retention Strategy Effective!** This offer drops churn risk to **{sim_p:.1%}** (below operating threshold {thresh:.2f}).")
            elif red_pct > 5.0:
                st.info(f"⚡ **Moderate Risk Reduction**: Churn risk decreased by **-{red_pct:.1f}%**, but remains above threshold.")
            else:
                st.caption("💡 Adjust sliders or select contract upgrades above to see risk reduction.")


        
    # 5. WHAT-IF / PRESCRIPTIVE ANALYTICS SECTION
    with st.container(border=True):
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
