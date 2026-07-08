import streamlit as st
from app.utils.config import PORTFOLIO_TITLE, PROJECT_TYPE, DEVELOPER_NAME, MODEL_STATUS

def render_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 10px 0;">
                <h3 style="margin: 0; color: #FFFFFF; font-weight: 800; font-size: 20px; line-height: 1.3;">{PORTFOLIO_TITLE}</h3>
                <span style="color: #6C63FF; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">{PROJECT_TYPE}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<hr style='margin: 10px 0; border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background: rgba(0, 212, 170, 0.05); border: 1px solid rgba(0, 212, 170, 0.15); border-radius: 8px; padding: 10px; margin-bottom: 12px; display: flex; align-items: center;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #00D4AA; display: inline-block; margin-right: 10px; box-shadow: 0 0 10px #00D4AA;"></span>
                <span style="font-size: 13px; color: #E2E8F0; font-weight: 600;">Model Status: {MODEL_STATUS}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style="background: rgba(108, 99, 255, 0.05); border: 1px solid rgba(108, 99, 255, 0.15); border-radius: 8px; padding: 10px; margin-bottom: 15px; display: flex; align-items: center;">
                <span style="font-size: 16px; margin-right: 8px;">👤</span>
                <span style="font-size: 13px; color: #E2E8F0; font-weight: 500;">Developed by <strong>{DEVELOPER_NAME}</strong></span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<hr style='margin: 10px 0; border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        st.subheader("📊 Model Specifications")
        st.markdown(
            """
            - **Primary Algorithm**: `Logistic Regression`
            - **Accuracy Limit**: `80.62%`
            - **ROC-AUC Score**: `0.8422`
            - **F1 Performance**: `60.49%`
            - **Feature Dimension**: `20 features`
            """
        )
        st.subheader("🛠️ Tech Stack")
        st.markdown(
            "`Python 3.11` | `Streamlit` | `Plotly`  \n`Scikit-learn` | `Joblib` | `FPDF2`"
        )
        st.markdown("<hr style='margin: 15px 0; border-color: rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        st.caption("🔒 Local Prediction Mode | Portfolio Environment")
