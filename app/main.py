"""
Customer Churn Prediction Web Application
Developed by: Naveen Kumar .D
Technologies: Streamlit, Scikit-learn, Pandas, NumPy, Matplotlib, Joblib
"""

import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Customer Churn Prediction System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
MODEL_DIR = "models"
EVAL_DIR = os.path.join("reports", "evaluation")

# Inject premium visual layout styles (Clean sans-serif fonts, shadows, borders)
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .custom-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        padding: 30px 10px;
        margin-top: 50px;
        border-top: 1px solid #e9ecef;
        color: #6c757d;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def load_model_pipeline():
    """Loads and caches the model, scaler, feature names, and mappings."""
    try:
        model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
        scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
        feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.pkl"))
        binary_mappings = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
        return model, scaler, feature_names, binary_mappings
    except Exception as e:
        st.error(f"Error loading model pipeline components: {e}")
        st.info("Please compile the pipeline by running: `python src/model_training.py`")
        return None, None, None, None

# Load model pipeline components
model, scaler, feature_names, binary_mappings = load_model_pipeline()

# --- SIDEBAR BRANDING & STATS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("Project Control Center")
    st.markdown("---")
    
    st.subheader("📋 Project Overview")
    st.write(
        "An interactive end-to-end Machine Learning system engineered to evaluate "
        "customer retention risk. By processing billing history, demographics, "
        "and active services, the system calculates churn probabilities to direct proactive outreach."
    )
    
    st.subheader("📊 Project Statistics")
    st.markdown(
        """
        - **Dataset Size**: `7,043 Customers`
        - **Features**: `20`
        - **Models Compared**: `3`
        - **Best Model**: `Logistic Regression`
        - **Best Accuracy**: `80.62%`
        """
    )
    
    st.subheader("👤 Developer Profile")
    st.markdown(
        """
        **Name**: Naveen Kumar  
        **Role**: AI & ML Developer  
        **Project**: Portfolio Showcase (2026)
        """
    )
    
    st.subheader("🛠️ Technologies Used")
    st.markdown(
        """
        `Python` | `Pandas` | `NumPy` | `Scikit-learn`  
        `Matplotlib` | `Seaborn` | `Streamlit`
        """
    )
    
    st.markdown("---")
    st.caption("🚀 **IBM Telco Customer Churn System**")

# --- MAIN DASHBOARD HEADER ---
st.title("📊 Customer Churn Prediction Dashboard")
st.markdown("---")

# Setup Tabs layout
tab_predictor, tab_metrics, tab_insights = st.tabs([
    "🔮 Churn Predictor", 
    "📊 Model Performance", 
    "💡 Feature Importance & Insights"
])

# ==============================================================================
# TAB 1: CHURN PREDICTOR
# ==============================================================================
with tab_predictor:
    if model is not None:
        # Build Input form layout
        with st.form("churn_input_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("👤 Demographic Profile")
                gender = st.selectbox("Gender", ["Female", "Male"])
                senior_citizen = st.selectbox("Senior Citizen Status", ["Non-Senior", "Senior Citizen"])
                partner = st.selectbox("Has a Partner?", ["No", "Yes"])
                dependents = st.selectbox("Has Dependents?", ["No", "Yes"])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Map senior citizen to binary representation
                senior_val = 1 if senior_citizen == "Senior Citizen" else 0
                
            with col2:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("💰 Account & Financials")
                tenure = st.slider("Tenure (Months active)", min_value=0, max_value=72, value=12)
                contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
                paperless = st.selectbox("Paperless Billing?", ["No", "Yes"])
                payment_method = st.selectbox(
                    "Payment Method", 
                    [
                        "Electronic check", 
                        "Mailed check", 
                        "Bank transfer (automatic)", 
                        "Credit card (automatic)"
                    ]
                )
                monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=65.0)
                total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=780.0)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col3:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("📶 Subscribed Services")
                phone_service = st.selectbox("Phone Service?", ["No", "Yes"])
                internet_service = st.selectbox("Internet Service Provider", ["DSL", "Fiber optic", "No"])
                online_security = st.selectbox("Online Security Add-on", ["No", "Yes", "No internet service"])
                tech_support = st.selectbox("Tech Support Add-on", ["No", "Yes", "No internet service"])
                
                # Advanced details collapsed in an expander for cleaner UI layout
                with st.expander("🛠️ Advanced Service Add-ons"):
                    multiple_lines = st.selectbox("Multiple Lines?", ["No", "Yes", "No phone service"])
                    online_backup = st.selectbox("Online Backup Add-on", ["No", "Yes", "No internet service"])
                    device_protection = st.selectbox("Device Protection Add-on", ["No", "Yes", "No internet service"])
                    streaming_tv = st.selectbox("Streaming TV Service", ["No", "Yes", "No internet service"])
                    streaming_movies = st.selectbox("Streaming Movies Service", ["No", "Yes", "No internet service"])
                st.markdown('</div>', unsafe_allow_html=True)
                
            submit_btn = st.form_submit_button("Predict Churn Risk", use_container_width=True)
            
        if submit_btn:
            # Preprocessing input
            input_data = {
                'gender': gender,
                'SeniorCitizen': senior_val,
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
            
            # 1. Create DataFrame
            input_df = pd.DataFrame([input_data])
            
            # 2. Map Binary Categorical Columns (Label Encoding mapping)
            for col, mapping in binary_mappings.items():
                input_df[col] = input_df[col].map(mapping)
                
            # 3. Apply One-Hot Encoding to Multi-class Categorical columns
            categorical_cols = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
                                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
                                'Contract', 'PaymentMethod']
            
            input_df = pd.get_dummies(input_df, columns=categorical_cols)
            
            # 4. Reindex columns using saved feature layout structure (imputes missing columns as 0)
            input_df = input_df.reindex(columns=feature_names, fill_value=0)
            
            # 5. Scale Numerical features
            num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
            input_df[num_cols] = scaler.transform(input_df[num_cols])
            input_df = input_df.astype(float)
            
            # 6. Model Inference
            prediction = model.predict(input_df)[0]
            probability = model.predict_proba(input_df)[0][1]
            
            # Define Risk Level and Style parameters
            if probability < 0.30:
                risk_title = "Low Churn Risk"
                risk_icon = "🟢"
                risk_color = "#28a745"
                risk_bg = "rgba(40, 167, 69, 0.1)"
                recommendations = (
                    "✓ **Continue Existing Plan** (Maintain active configuration)\n"
                    "✓ **Offer Premium Upgrade** (Pitch value-added movie/TV packages)\n"
                    "✓ **Loyalty Rewards** (Provide tenure milestones vouchers)"
                )
                summary_verdict = "Customer is likely to stay. No immediate retention action required."
            elif probability <= 0.80:
                risk_title = "Medium Churn Risk"
                risk_icon = "🟡"
                risk_color = "#ffc107"
                risk_bg = "rgba(255, 193, 7, 0.15)"
                recommendations = (
                    "✓ **Monitor Closely** (Add account to high-monitoring list)\n"
                    "✓ **Promote Auto-Pay Switch** (Offer a $5 credit to register Auto-Pay)\n"
                    "✓ **Tech Health Check** (Confirm Fiber/DSL service runs fine)"
                )
                summary_verdict = "Customer exhibits moderate risk. Initiate mild retention outreach."
            else:
                risk_title = "High Churn Risk"
                risk_icon = "🔴"
                risk_color = "#dc3545"
                risk_bg = "rgba(220, 53, 69, 0.1)"
                recommendations = (
                    "✓ **Offer annual contract** (Convert month-to-month contracts to 1 or 2 years)\n"
                    "✓ **Offer 15% discount** (Apply retention promo discount to lower Monthly Charges)\n"
                    "✓ **Customer retention call** (Schedule a direct outreach call by the loyalty support team)\n"
                    "✓ **Upgrade support** (Bundle Online Security and Tech Support for free)"
                )
                summary_verdict = "Customer is highly likely to churn. Deploy immediate retention countermeasures."
            
            # Render Diagnostic Outputs
            st.markdown("### 🔍 Risk Analysis Report")
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.markdown(
                    f"""
                    <div style="background-color: {risk_bg}; border: 1px solid rgba(0,0,0,0.05); 
                                padding: 20px; border-radius: 8px; border-left: 5px solid {risk_color}; min-height: 110px;">
                        <span style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; color: #6c757d; font-weight: bold;">Prediction Verdict</span>
                        <h3 style="margin: 4px 0 0 0; color: {risk_color}; font-size: 24px; font-weight: bold;">{risk_icon} {risk_title}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with metric_col2:
                # Custom Color-coded progress bar gauge
                st.markdown(
                    f"""
                    <div style="background-color: rgba(108, 117, 125, 0.05); border: 1px solid rgba(108, 117, 125, 0.1); 
                                padding: 20px; border-radius: 8px; border-left: 5px solid #6c757d; min-height: 110px;">
                        <span style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; color: #6c757d; font-weight: bold;">Churn Probability Gauge</span>
                        <div style="background-color: #e9ecef; border-radius: 8px; width: 100%; height: 22px; margin-top: 8px; overflow: hidden;">
                            <div style="background-color: {risk_color}; width: {probability*100}%; height: 22px; text-align: center; color: white; font-size: 12px; font-weight: bold; line-height: 22px;">
                                {probability:.2%}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action plans
            rec_col1, rec_col2 = st.columns(2)
            with rec_col1:
                st.subheader("💡 Recommended Actions")
                st.markdown(recommendations)
            with rec_col2:
                st.subheader("📋 Decision Summary")
                st.info(summary_verdict)
                
            st.markdown("---")
            st.subheader("📥 Export & Downloads")
            
            # Prepare Download Files
            # 1. Prediction CSV dataframe
            result_df = pd.DataFrame([input_data])
            result_df['Churn_Prediction'] = "Yes" if prediction == 1 else "No"
            result_df['Churn_Probability'] = probability
            csv_data = result_df.to_csv(index=False).encode('utf-8')
            
            # 2. Text Summary Report
            report_text = (
                f"CUSTOMER CHURN PREDICTION REPORT\n"
                f"Generated by: Customer Churn Prediction System\n"
                f"Developer: Naveen Kumar .D\n"
                f"Year: 2026\n"
                f"==================================================\n\n"
                f"CUSTOMER PROFILE:\n"
                f"  - Gender: {gender}\n"
                f"  - Senior Status: {senior_citizen}\n"
                f"  - Tenure: {tenure} months\n"
                f"  - Contract Type: {contract}\n"
                f"  - Payment Channel: {payment_method}\n"
                f"  - Monthly Spend: ${monthly_charges:.2f}\n"
                f"  - Total Spend: ${total_charges:.2f}\n\n"
                f"MODEL RESULTS:\n"
                f"  - Churn Prediction: {'Likely to Churn' if prediction == 1 else 'Not Likely to Churn'}\n"
                f"  - Churn Probability: {probability:.2%}\n"
                f"  - Risk Class: {risk_title}\n\n"
                f"RECOMMENDED RETENTION ACTIONS:\n"
                f"{recommendations.replace('✓', '-')}\n"
            )
            
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.download_button(
                    label="📥 Download Prediction Log (CSV)",
                    data=csv_data,
                    file_name="churn_prediction_log.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with d_col2:
                st.download_button(
                    label="📥 Download Diagnostic Report (Text)",
                    data=report_text,
                    file_name="churn_diagnostic_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    else:
        st.warning("Model and Preprocessing assets are currently unavailable. Make sure your pipeline is compiled.")

# ==============================================================================
# TAB 2: MODEL PERFORMANCE
# ==============================================================================
with tab_metrics:
    st.subheader("📈 Core Classification Metrics ( Logistic Regression )")
    st.markdown(
        "These metrics evaluate the model's performance on the **1,409 customer** test split dataset."
    )
    
    # Render metrics cards row
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    m_col1.metric("Accuracy", "80.62%", help="Overall correct classification rate.")
    m_col2.metric("Precision", "65.93%", help="Accuracy of positive (churn) predictions.")
    m_col3.metric("Recall", "55.88%", help="Proportion of actual churners correctly caught.")
    m_col4.metric("F1-Score", "60.49%", help="Harmonic mean balancing precision & recall.")
    m_col5.metric("ROC-AUC", "0.8422", help="Separation performance ranking risk score.")
    
    st.markdown("---")
    st.subheader("📊 Diagnostic Plots")
    
    # Image file check helper
    def display_plot_or_warning(plot_path, caption, explanation):
        if os.path.exists(plot_path):
            st.image(plot_path, caption=caption, use_container_width=True)
            st.caption(explanation)
        else:
            st.warning(f"Plot file not found at: {plot_path}. Please execute `python src/model_evaluation.py` to compile plots.")
            
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        display_plot_or_warning(
            os.path.join(EVAL_DIR, "confusion_matrix.png"),
            "Confusion Matrix",
            "This grid splits actual values (rows) vs model predictions (columns). "
            "It breaks down True Negatives (927), True Positives (209), "
            "False Positives (108), and False Negatives (165)."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        display_plot_or_warning(
            os.path.join(EVAL_DIR, "precision_recall_curve.png"),
            "Precision-Recall Curve",
            "Maps the trade-off between precision (capturing only true risk) and recall "
            "(catching all true risk) at different probability thresholds. Average Precision (AP) is 0.6558."
        )
        
    with p_col2:
        display_plot_or_warning(
            os.path.join(EVAL_DIR, "roc_curve.png"),
            "ROC Curve",
            "Compares True Positive Rate vs False Positive Rate across thresholds. "
            "Our Area Under the Curve (ROC-AUC) is 0.8422, showing strong discriminative power."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        display_plot_or_warning(
            os.path.join(EVAL_DIR, "metrics_comparison.png"),
            "Performance Balance Overview",
            "A comparison of our model's core metrics to visually show accuracy, "
            "precision, recall, and F1-score balances on the test set."
        )

# ==============================================================================
# TAB 3: FEATURE IMPORTANCE & INSIGHTS
# ==============================================================================
with tab_insights:
    st.subheader("💡 Model Feature Importance Weights")
    st.markdown(
        "Feature importances represent the coefficients of our Logistic Regression model. "
        "Positive coefficients drive churn, while negative coefficients indicate retention."
    )
    
    fi_col1, fi_col2 = st.columns([3, 2])
    with fi_col1:
        display_plot_or_warning(
            os.path.join(EVAL_DIR, "feature_importance.png"),
            "Top 15 Feature Importances",
            "Logistic Regression coefficient values. Orange bars increase the likelihood of churn, while blue bars decrease it."
        )
    with fi_col2:
        st.subheader("📋 Top Feature Explanations")
        st.markdown(
            """
            * **Contract (Month-to-month)**: 
              - *Sign*: Positive (Increases churn risk).
              - *Business Meaning*: Customers without annual contracts can cancel at any time. This is the single strongest predictor of churn.
              
            * **Internet Service (Fiber Optic)**:
              - *Sign*: Positive (Increases churn risk).
              - *Business Meaning*: Despite being a premium product, fiber has high churn. Indicates technical service issues or price sensitivity.
              
            * **Tenure**:
              - *Sign*: Negative (Retains customer).
              - *Business Meaning*: Every additional month a customer stays with the company drops their probability of leaving. Long-tenure customers are very sticky.
              
            * **Payment Method (Electronic Check)**:
              - *Sign*: Positive (Increases churn risk).
              - *Business Meaning*: Electronic checks require manual interaction monthly, which increases transaction failure rates and billing friction compared to automated auto-pay credit card channels.
              
            * **Online Security & Tech Support (No Service)**:
              - *Sign*: Negative (Having security/support drops churn).
              - *Business Meaning*: Subscribing to online protection or active customer support lines anchors the user and increases relationship stability.
            """
        )

# --- PROFESSIONAL FOOTER ---
st.markdown(
    """
    <div class="footer">
        <p><strong>Customer Churn Prediction System</strong></p>
        <p>Developed by Naveen Kumar .D | AI & ML Portfolio Project</p>
        <p>Python | Scikit-learn | Streamlit</p>
        <p><a href="https://github.com" target="_blank">🔗 GitHub Portfolio</a></p>
        <p>&copy; 2026. All Rights Reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
