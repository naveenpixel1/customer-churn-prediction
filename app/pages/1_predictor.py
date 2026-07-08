import os
import sys
import time

# Ensure root directory is in python path to resolve 'app' imports
current_dir = os.path.dirname(os.path.abspath(__file__))
while current_dir and not os.path.exists(os.path.join(current_dir, 'app')):
    parent = os.path.dirname(current_dir)
    if parent == current_dir:
        break
    current_dir = parent
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import streamlit as st
from app.components.styles import inject_premium_styles
from app.components.cards import render_progress_indicator, render_verdict_card
from app.services.prediction_service import PredictionService
from app.services.history_service import HistoryService
from app.utils.validators import validate_numeric_inputs
from app.utils.export import generate_csv_report, generate_text_report, generate_pdf_report

# Inject styles
inject_premium_styles()

st.markdown("<h1 class='glowing-title gradient-text'>🔮 Customer Churn Prediction</h1>", unsafe_allow_html=True)
st.markdown("Enter customer information below to predict the likelihood of churn.")

# Initialize sessions
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'inputs' not in st.session_state:
    st.session_state.inputs = {}
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# Instantiate services
try:
    predictor = PredictionService()
    history_logger = HistoryService()
except Exception as e:
    st.error(f"Error loading prediction pipeline components: {e}")
    st.info("Ensure you compiled the pipeline by running: `python src/model_training.py`")
    st.stop()

# Progress wizard header
render_progress_indicator(st.session_state.step)

# ----------------- STEP 1: DEMOGRAPHICS -----------------
if st.session_state.step == 1:
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    st.subheader("👤 Demographic Profile")
    st.write("Provide customer demographic indicators below:")
    
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox(
            "Gender", ["Female", "Male"], 
            index=0 if st.session_state.inputs.get("gender") == "Female" else 1,
            help="Select the customer's gender identification."
        )
        senior_citizen = st.selectbox(
            "Senior Citizen Status", ["Non-Senior", "Senior Citizen"],
            index=1 if st.session_state.inputs.get("SeniorCitizen") == 1 else 0,
            help="Does the customer qualify for senior billing programs?"
        )
    with col2:
        partner = st.selectbox(
            "Has a Partner?", ["No", "Yes"],
            index=1 if st.session_state.inputs.get("Partner") == "Yes" else 0,
            help="Indicate if the customer lists a partner on the account."
        )
        dependents = st.selectbox(
            "Has Dependents?", ["No", "Yes"],
            index=1 if st.session_state.inputs.get("Dependents") == "Yes" else 0,
            help="Does the customer have registered child/family dependents?"
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_prev, col_next = st.columns([1, 1])
    with col_next:
        if st.button("Continue to Subscriptions", use_container_width=True):
            st.session_state.inputs.update({
                "gender": gender,
                "SeniorCitizen": 1 if senior_citizen == "Senior Citizen" else 0,
                "Partner": partner,
                "Dependents": dependents
            })
            st.session_state.step = 2
            st.rerun()

# ----------------- STEP 2: SERVICES -----------------
elif st.session_state.step == 2:
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    st.subheader("📶 Subscribed Services")
    st.write("Configure customer service configurations:")
    
    col1, col2 = st.columns(2)
    with col1:
        phone_service = st.selectbox(
            "Phone Service Active?", ["No", "Yes"],
            index=1 if st.session_state.inputs.get("PhoneService") == "Yes" else 0
        )
        multiple_lines = st.selectbox(
            "Multiple Lines Configuration", ["No", "Yes", "No phone service"],
            index=["No", "Yes", "No phone service"].index(st.session_state.inputs.get("MultipleLines", "No"))
        )
        internet_service = st.selectbox(
            "Internet Service Provider Type", ["DSL", "Fiber optic", "No"],
            index=["DSL", "Fiber optic", "No"].index(st.session_state.inputs.get("InternetService", "DSL"))
        )
        online_security = st.selectbox(
            "Online Security Add-on?", ["No", "Yes", "No internet service"],
            index=["No", "Yes", "No internet service"].index(st.session_state.inputs.get("OnlineSecurity", "No"))
        )
    with col2:
        online_backup = st.selectbox(
            "Online Backup Add-on?", ["No", "Yes", "No internet service"],
            index=["No", "Yes", "No internet service"].index(st.session_state.inputs.get("OnlineBackup", "No"))
        )
        device_protection = st.selectbox(
            "Device Protection Add-on?", ["No", "Yes", "No internet service"],
            index=["No", "Yes", "No internet service"].index(st.session_state.inputs.get("DeviceProtection", "No"))
        )
        tech_support = st.selectbox(
            "Tech Support Add-on?", ["No", "Yes", "No internet service"],
            index=["No", "Yes", "No internet service"].index(st.session_state.inputs.get("TechSupport", "No"))
        )
        streaming_tv = st.selectbox(
            "Streaming TV Service?", ["No", "Yes", "No internet service"],
            index=["No", "Yes", "No internet service"].index(st.session_state.inputs.get("StreamingTV", "No"))
        )
        streaming_movies = st.selectbox(
            "Streaming Movies Service?", ["No", "Yes", "No internet service"],
            index=["No", "Yes", "No internet service"].index(st.session_state.inputs.get("StreamingMovies", "No"))
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("Previous Section", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col_next:
        if st.button("Continue to Financials", use_container_width=True):
            st.session_state.inputs.update({
                "PhoneService": phone_service,
                "MultipleLines": multiple_lines,
                "InternetService": internet_service,
                "OnlineSecurity": online_security,
                "OnlineBackup": online_backup,
                "DeviceProtection": device_protection,
                "TechSupport": tech_support,
                "StreamingTV": streaming_tv,
                "StreamingMovies": streaming_movies
            })
            st.session_state.step = 3
            st.rerun()

# ----------------- STEP 3: FINANCIALS -----------------
elif st.session_state.step == 3:
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    st.subheader("💰 Account & Financial Details")
    st.write("Input current contract and payment specifications:")
    
    col1, col2 = st.columns(2)
    with col1:
        tenure = st.slider(
            "Tenure (Active Months)", min_value=0, max_value=72, 
            value=int(st.session_state.inputs.get("tenure", 12)),
            help="Total consecutive months the customer has been active."
        )
        contract = st.selectbox(
            "Contract Arrangement Type", ["Month-to-month", "One year", "Two year"],
            index=["Month-to-month", "One year", "Two year"].index(st.session_state.inputs.get("Contract", "Month-to-month"))
        )
        paperless = st.selectbox(
            "Paperless Billing Active?", ["No", "Yes"],
            index=1 if st.session_state.inputs.get("PaperlessBilling") == "Yes" else 0
        )
        payment_method = st.selectbox(
            "Active Payment Method Channel", 
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
            index=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"].index(st.session_state.inputs.get("PaymentMethod", "Electronic check"))
        )
    with col2:
        monthly_charges = st.number_input(
            "Monthly Billing Charge ($)", min_value=0.0, max_value=200.0, 
            value=float(st.session_state.inputs.get("MonthlyCharges", 65.0)), step=0.50
        )
        total_charges = st.number_input(
            "Total Cumulative Charges ($)", min_value=0.0, max_value=15000.0, 
            value=float(st.session_state.inputs.get("TotalCharges", 780.0)), step=10.0
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("Previous Section", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with col_next:
        if st.button("Evaluate Churn Risk", use_container_width=True):
            # Run checks
            is_valid, err_msg = validate_numeric_inputs(tenure, monthly_charges, total_charges)
            if not is_valid:
                st.error(err_msg)
            else:
                st.session_state.inputs.update({
                    "tenure": tenure,
                    "Contract": contract,
                    "PaperlessBilling": paperless,
                    "PaymentMethod": payment_method,
                    "MonthlyCharges": monthly_charges,
                    "TotalCharges": total_charges
                })
                
                # Execute prediction
                with st.spinner("Processing customer risk signatures..."):
                    time.sleep(1.0)
                    res = predictor.predict(st.session_state.inputs)
                    st.session_state.prediction_result = res
                    # Save prediction history log entry
                    history_logger.append_record(st.session_state.inputs, res)
                    
                st.session_state.step = 4
                st.rerun()

# ----------------- STEP 4: PREDICTION REPORT -----------------
elif st.session_state.step == 4:
    res = st.session_state.prediction_result
    
    if res is None:
        st.warning("No prediction evaluations found. Please complete the wizard again.")
        st.session_state.step = 1
        st.rerun()
        
    prob = res.get("probability", 0.0)
    risk_level = res.get("risk_level", "Low")
    prediction = res.get("prediction", 0)
    confidence = res.get("confidence", "Moderate")
    contributions = res.get("contributions", {})
    
    # Custom glowing output card
    render_verdict_card(prob, risk_level, prediction, confidence)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.subheader("💡 Recommended Actions")
        
        # Recommendations lists based on risk level
        if risk_level == "Low":
            st.success("✓ Customer loyalty score is high. Maintain active billing structures.")
            st.markdown(
                """
                - **Loyalty incentives**: Pitch premier visual subscriptions or high-speed bandwidth upgrades.
                - **Lifecycle programs**: Offer anniversary reward credits automatically.
                """
            )
        elif risk_level == "Medium":
            st.warning("✓ Warning flags detected. Action recommended to secure loyalty.")
            st.markdown(
                """
                - **Billing Migration**: Suggest enrolling in Auto-pay (Bank/Card) via a one-time $5 credit.
                - **Active Outreach**: Send customer experience checks to confirm product satisfaction.
                """
            )
        elif risk_level == "High":
            st.error("✓ Churn risk is elevated. Deploy immediate retention strategies.")
            st.markdown(
                """
                - **Contract Migration**: Offer custom annual contracts at lower monthly rates.
                - **Financial Relief**: Pitch specialized loyalty discounts (e.g. 10% off bills).
                - **High-priority Support**: Routing to loyalty management specialist teams.
                """
            )
        else: # Critical
            st.error("🚨 Critical churn warnings active! Emergency actions required.")
            st.markdown(
                """
                - **Direct Executive Outbound**: Schedule customer support callback immediately.
                - **Plan Restructuring**: Apply deep discount billing credits or downgrade options.
                - **Service Anchors**: Offer free tech security or support features for 6 months.
                """
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.subheader("📊 Key Driver Contributions")
        st.write("Feature weights indicating positive/negative directions on decision outcome:")
        
        # Plotly horizontal bar plot
        import plotly.graph_objects as go
        
        top_contrib = list(contributions.items())[:6]
        features = [c[0] for c in top_contrib]
        weights = [c[1] for c in top_contrib]
        
        # Revert order for chart display
        features.reverse()
        weights.reverse()
        
        colors = ['#FF6B6B' if w > 0 else '#6C63FF' for w in weights]
        
        fig = go.Figure(go.Bar(
            x=weights,
            y=features,
            orientation='h',
            marker_color=colors,
            hovertemplate="Weight: %{x:.3f}<extra></extra>"
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0),
            height=200,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=True, zerolinecolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=False, tickfont=dict(color="#CBD5E1"))
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("Orange bars drive towards churn; blue bars drive towards retention.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Download actions
    st.markdown("### 📥 Export Risk Analysis Outputs")
    
    csv_bytes = generate_csv_report(st.session_state.inputs, res)
    txt_report = generate_text_report(st.session_state.inputs, res)
    pdf_bytes = generate_pdf_report(st.session_state.inputs, res)
    
    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        st.download_button(
            label="📥 Download CSV Summary Data",
            data=csv_bytes,
            file_name=f"churn_prediction_{st.session_state.inputs.get('gender')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with d_col2:
        st.download_button(
            label="📥 Download TXT Diagnostics Report",
            data=txt_report,
            file_name=f"churn_diagnostic_report_{st.session_state.inputs.get('tenure')}m.txt",
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
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Reset Predictor Wizard", use_container_width=True):
        st.session_state.step = 1
        st.session_state.inputs = {}
        st.session_state.prediction_result = None
        st.rerun()
