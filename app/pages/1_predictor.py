import os
import sys

# Ensure project root is in sys.path
_current = os.path.dirname(os.path.abspath(__file__))
while _current and _current != os.path.dirname(_current):
    if os.path.exists(os.path.join(_current, "app")):
        if _current not in sys.path:
            sys.path.insert(0, _current)
        break
    _current = os.path.dirname(_current)

from app.utils.bootstrap import ensure_project_root_in_path
ensure_project_root_in_path()

import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from typing import Tuple, Dict, Any

from app.components.styles import inject_premium_styles
from app.components.cards import (
    render_verdict_card,
    render_insight_card,
    render_account_health_gauge,
    render_retention_driver_split,
    render_risk_transition_badge,
    render_mitigation_success_box
)
from app.utils.validators import validate_numeric_inputs
from app.utils.export import generate_csv_report, generate_text_report, generate_pdf_report
from app.services.history_service import HistoryService
from app.services.prediction_service import PredictionService
from app.utils.security import validate_prediction_input, sanitize_html
from app.utils.currency import format_currency, get_currency_symbol

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

st.markdown("<h1 class='glowing-title gradient-text'>Account Health Dashboard</h1>", unsafe_allow_html=True)
st.markdown('<p style="font-size: 15px; color: #64748B; margin-top: -8px; margin-bottom: 24px;">Monitor customer churn probability, analyze risk drivers, and simulate retention offer levers in real time.</p>', unsafe_allow_html=True)

try:
    model, scaler, feature_names, binary_mappings = load_ml_pipeline()
    history_logger = HistoryService()
    pred_service = PredictionService()
except Exception as e:
    st.error(f"Failed to load machine learning assets: {e}")
    st.stop()

if 'prediction_ran' not in st.session_state:
    st.session_state.prediction_ran = False
if 'last_inputs' not in st.session_state:
    st.session_state.last_inputs = {}
if 'last_result' not in st.session_state:
    st.session_state.last_result = {}

# --- CUSTOMER PROFILE INPUTS (3 DISTINCT CARDS) ---
with st.container():
    col_dem, col_ser, col_acc = st.columns(3)

    with col_dem:
        with st.container(border=True):
            st.markdown('<h4 style="color:#4F46E5; margin-top:0; font-weight:700; font-size:16px;">Demographics</h4>', unsafe_allow_html=True)
            gender = st.selectbox("Gender", ["Female", "Male"], index=0)
            senior_citizen = st.selectbox("Senior Citizen Status", ["No", "Yes"], index=0)
            partner = st.selectbox("Has a Partner?", ["No", "Yes"], index=0)
            dependents = st.selectbox("Has Dependents?", ["No", "Yes"], index=0)

    with col_ser:
        with st.container(border=True):
            st.markdown('<h4 style="color:#0D9488; margin-top:0; font-weight:700; font-size:16px;">Active Services</h4>', unsafe_allow_html=True)
            phone_service = st.selectbox("Phone Service", ["No", "Yes"], index=1)
            multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"], index=0)
            internet_service = st.selectbox("Internet Service Provider", ["Fiber optic", "DSL", "No"], index=0)

            t_security = st.toggle("Online Security Add-on", value=False)
            t_backup = st.toggle("Online Backup Add-on", value=True)
            t_protection = st.toggle("Device Protection Add-on", value=True)
            t_support = st.toggle("Tech Support Add-on", value=False)
            t_tv = st.toggle("Streaming TV Service", value=True)
            t_movies = st.toggle("Streaming Movies Service", value=True)

            no_inet = (internet_service == "No")
            online_security = "Yes" if t_security else ("No internet service" if no_inet else "No")
            online_backup = "Yes" if t_backup else ("No internet service" if no_inet else "No")
            device_protection = "Yes" if t_protection else ("No internet service" if no_inet else "No")
            tech_support = "Yes" if t_support else ("No internet service" if no_inet else "No")
            streaming_tv = "Yes" if t_tv else ("No internet service" if no_inet else "No")
            streaming_movies = "Yes" if t_movies else ("No internet service" if no_inet else "No")

    with col_acc:
        with st.container(border=True):
            sym = get_currency_symbol()
            st.markdown('<h4 style="color:#D97706; margin-top:0; font-weight:700; font-size:16px;">Financials & Account</h4>', unsafe_allow_html=True)
            tenure = st.slider("Tenure (Active Months)", min_value=0, max_value=72, value=24)
            contract = st.selectbox("Contract Agreement Type", ["Month-to-month", "One year", "Two year"], index=0)
            paperless = st.selectbox("Paperless Billing Active?", ["Yes", "No"], index=0)
            payment_method = st.selectbox(
                "Active Payment Channel",
                ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
                index=0
            )
            monthly_charges = st.number_input(f"Monthly Charges ({sym})", min_value=0.0, max_value=500.0, value=95.0, step=1.0)
            calculated_total = float(tenure * monthly_charges) if tenure > 0 else 0.0
            total_charges = st.number_input(
                f"Total Charges ({sym})",
                min_value=0.0,
                max_value=50000.0,
                value=calculated_total,
                step=10.0,
                help="Estimated total lifetime charges based on tenure and monthly bill."
            )

# Prominent Indigo Action Button
if st.button("Analyze Customer Risk Profile", use_container_width=True):
    is_valid, error_msg = validate_numeric_inputs(tenure, monthly_charges, total_charges)
    if not is_valid:
        st.error(error_msg)
    else:
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
        active_threshold = float(st.session_state.get('decision_threshold', 0.35))
        
        # Server-side schema validation (Items #8, #14)
        schema_valid, schema_err = validate_prediction_input(input_data)
        if not schema_valid:
            st.error(f"Input validation error: {sanitize_html(schema_err)}")
        else:
            result = pred_service.predict(input_data, threshold=active_threshold)
            history_logger.append_record(input_data, result)
            st.session_state.prediction_ran = True
            st.session_state.last_inputs = input_data
            st.session_state.last_result = result

# --- RISK ANALYSIS RESULTS LAYOUT ---
if st.session_state.prediction_ran:
    inputs = st.session_state.last_inputs
    res = st.session_state.last_result
    prob = res['probability']
    risk_level = res['risk_level']
    pred = res['prediction']
    conf = res['confidence']
    thresh = res.get('threshold', 0.35)

    st.markdown('<hr style="border-color: #E2E8F0; margin: 24px 0;">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#0F172A; font-weight:800;">Real-Time Account Risk Diagnostics</h3>', unsafe_allow_html=True)

    # 1. CURRENT ACCOUNT HEALTH (CIRCULAR GAUGE)
    with st.container(border=True):
        st.markdown('<h4 style="color:#0F172A; font-weight:700; margin-top:0;">Current Account Health</h4>', unsafe_allow_html=True)
        render_account_health_gauge(prob, risk_level)

    # 1b. CUSTOMER LIFETIME VALUE & PRIORITY TIER CARD
    clv_val = res.get('clv', 1000.0)
    p_tier = res.get('priority_tier', {})
    tier_name = p_tier.get('tier', 'Standard Account')
    tier_color = p_tier.get('color', '#6C63FF')
    tier_bg = p_tier.get('bg', '#F8FAFC')
    tier_action = p_tier.get('action', 'Standard retention workflow')

    st.markdown(
        f"""
        <div style="background: {tier_bg}; border: 1px solid {tier_color}; border-left: 6px solid {tier_color}; border-radius: 12px; padding: 18px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.5px;">Customer Lifetime Value & Action Tier</div>
                    <div style="font-size: 19px; font-weight: 800; color: {tier_color}; margin-top: 2px;">{tier_name}</div>
                    <div style="font-size: 13px; color: #334155; margin-top: 4px;"><strong>Actionable Strategy:</strong> {tier_action}</div>
                </div>
                <div style="text-align: right; background: #FFFFFF; padding: 10px 16px; border-radius: 10px; border: 1px solid #E2E8F0;">
                    <div style="font-size: 11px; color: #64748B; font-weight: 700;">PROJECTED CLV</div>
                    <div style="font-size: 22px; font-weight: 800; color: #0F172A;">{format_currency(clv_val)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. RETENTION DRIVERS SPLIT-VIEW
    with st.container(border=True):
        st.markdown('<h4 style="color:#0F172A; font-weight:700; margin-top:0;">Retention Drivers Analysis</h4>', unsafe_allow_html=True)
        exp_data = res.get('explanation', {})
        risk_drivers = exp_data.get('top_risk_drivers', [])
        mitigating_drivers = exp_data.get('top_mitigating_drivers', [])
        render_retention_driver_split(risk_drivers, mitigating_drivers)

    # 3. INTERACTIVE RETENTION SIMULATOR
    with st.container(border=True):
        st.markdown('<h4 style="color:#0F172A; font-weight:700; margin-top:0;">Interactive Retention Simulator</h4>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 14px; color: #64748B;">Select proactive retention offer levers below to evaluate risk reduction and customer lifetime value preservation.</p>', unsafe_allow_html=True)

        sim_col1, sim_col2 = st.columns([1, 1])
        with sim_col1:
            st.markdown('<div style="font-size: 14px; font-weight: 700; color: #4F46E5; margin-bottom: 10px;">Offer Levers</div>', unsafe_allow_html=True)
            current_contract = inputs.get('Contract', 'Month-to-month')
            contract_opts = ["Month-to-month", "One year", "Two year"]
            c_index = contract_opts.index(current_contract) if current_contract in contract_opts else 0
            sim_contract = st.selectbox("Contract Switch Offer", contract_opts, index=c_index)
            sim_tech_support = st.toggle("Add Premium Tech Support", value=(inputs.get('TechSupport') == 'Yes'))
            sim_security = st.toggle("Add Device Security", value=(inputs.get('OnlineSecurity') == 'Yes'))
            sim_discount = st.slider(f"Monthly Billing Discount ({get_currency_symbol()})", min_value=0.0, max_value=50.0, value=10.0, step=1.0)

        with sim_col2:
            st.markdown('<div style="font-size: 14px; font-weight: 700; color: #0D9488; margin-bottom: 10px;">Simulated Risk Transition</div>', unsafe_allow_html=True)
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
            sim_risk = sim_res['simulated_risk_level']
            render_risk_transition_badge(orig_p, sim_p, risk_level, sim_risk)
            if sim_p < thresh or red_pct > 5.0:
                render_mitigation_success_box(red_pct, clv_impact=1000.0)
            else:
                st.info("Adjust contract terms or add tech support to see risk reduction.")

    # PRESCRIPTIVE RETENTION PLAYBOOK
    with st.container(border=True):
        st.markdown('<h4 style="color:#0F172A; font-weight:700; margin-top:0;">Prescriptive Retention Playbook</h4>', unsafe_allow_html=True)
        recs = []
        if inputs.get('Contract') == 'Month-to-month':
            recs.append(("Migrate Month-to-Month Cohorts", "This account is on a month-to-month contract. Offer a 10% monthly discount bundle if they transition to an annual contract plan."))
        if inputs.get('InternetService') == 'Fiber optic' and inputs.get('TechSupport') != 'Yes':
            recs.append(("Fiber Optic Support Bundling", "Subscribed to Fiber Optic internet without Online Tech Support. Offer a bundled Tech Support add-on at a 50% discount."))
        if inputs.get('PaymentMethod') == 'Electronic check':
            recs.append(("Automate Payment Methods", "Active payment channel is Electronic Check. Incentivize migrating to bank auto-pay or Credit Card auto-pay with a $5 billing credit."))
        if not recs:
            st.success("Customer risk profile is solid. Maintain standard billing check-ins.")
        else:
            for title, desc in recs[:3]:
                render_insight_card(title, desc, "danger" if risk_level in ['High', 'Critical'] else "warning")

    # Report exporters
    st.markdown('<h4 style="color:#0F172A; font-weight:700;">Export Diagnostic Artifacts</h4>', unsafe_allow_html=True)
    csv_bytes = generate_csv_report(inputs, res)
    txt_report = generate_text_report(inputs, res)
    pdf_bytes = generate_pdf_report(inputs, res)
    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        st.download_button(label="Download CSV Summary", data=csv_bytes, file_name=f"churn_prediction_{inputs.get('gender')}.csv", mime="text/csv", use_container_width=True)
    with d_col2:
        st.download_button(label="Download TXT Diagnostics", data=txt_report, file_name=f"churn_diagnostic_report_{inputs.get('tenure')}m.txt", mime="text/plain", use_container_width=True)
    with d_col3:
        st.download_button(label="Download PDF Report", data=pdf_bytes, file_name="churn_assessment_pdf_report.pdf", mime="application/pdf", use_container_width=True)
