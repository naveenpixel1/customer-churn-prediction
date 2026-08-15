import streamlit as st
from app.utils.config import PORTFOLIO_TITLE, PROJECT_TYPE, DEVELOPER_NAME, MODEL_STATUS, MODEL_METRICS
from app.utils.model_metadata import load_model_metadata

from app.utils.currency import render_currency_selector

def render_sidebar():
    metadata = load_model_metadata() or {}
    best_model_name = metadata.get("best_model_name", "Unknown")
    metrics = MODEL_METRICS
    
    with st.sidebar:
        st.markdown(
            f'<div style="padding: 10px 0;">'
            f'<h3 style="margin: 0; color: #0F172A; font-weight: 800; font-size: 18px; line-height: 1.3;">{PORTFOLIO_TITLE}</h3>'
            f'<span style="color: #6C63FF; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{PROJECT_TYPE}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('<hr style="margin: 10px 0; border-color: #E2E8F0;">', unsafe_allow_html=True)
        
        # Currency Localization Selector (Item: Indian website / Currency switcher)
        render_currency_selector()
        st.markdown('<div style="margin-bottom: 12px;"></div>', unsafe_allow_html=True)
        
        st.markdown(
            f'<div style="background: #F0FDF4; border: 1px solid #A7F3D0; border-radius: 8px; padding: 10px; margin-bottom: 12px; display: flex; align-items: center;">'
            f'<span style="width: 8px; height: 8px; border-radius: 50%; background: #0D9488; display: inline-block; margin-right: 10px; box-shadow: 0 0 6px #0D9488;"></span>'
            f'<span style="font-size: 13px; color: #065F46; font-weight: 600;">Model Status: {MODEL_STATUS}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px; margin-bottom: 15px;">'
            f'<div style="font-size: 13px; color: #334155; font-weight: 500;">Developed by <strong>{DEVELOPER_NAME}</strong></div>'
            f'<a href="https://github.com/naveenpixel1/customer-churn-prediction" target="_blank" style="color: #6C63FF; font-size: 13px; font-weight: 700; text-decoration: none;">GitHub Repository</a>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('<hr style="margin: 10px 0; border-color: #E2E8F0;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #0F172A; font-weight: 700; font-size: 14px; margin-bottom: 8px;">Model Specifications</h4>', unsafe_allow_html=True)
        st.markdown(
            f"- **Primary Algorithm**: `{best_model_name}`\n"
            f"- **F1 Performance**: `{metrics.get('F1-Score', 0.0):.2%}`\n"
            f"- **Recall Rate**: `{metrics.get('Recall', 0.0):.2%}`\n"
            f"- **ROC-AUC Score**: `{metrics.get('ROC-AUC', 0.0):.4f}`\n"
            f"- **Overall Accuracy**: `{metrics.get('Accuracy', 0.0):.2%}`\n"
            f"- **Feature Dimension**: `30 features`"
        )
        st.markdown('<h4 style="color: #0F172A; font-weight: 700; font-size: 14px; margin-bottom: 8px;">Tech Stack</h4>', unsafe_allow_html=True)
        st.markdown("`Python 3.11` | `Streamlit` | `Plotly`  \n`Scikit-learn` | `Joblib` | `FPDF2`")
        st.markdown('<hr style="margin: 12px 0; border-color: #E2E8F0;">', unsafe_allow_html=True)
        st.caption("Local Prediction Mode | Account Health Dashboard")
