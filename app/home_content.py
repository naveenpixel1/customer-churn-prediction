import streamlit as st
from app.components.styles import inject_premium_styles
from app.components.cards import render_kpi_card
from app.utils.config import PORTFOLIO_TITLE, PORTFOLIO_SUBTITLE, DEVELOPER_NAME, PROJECT_TYPE, MODEL_METRICS
from app.utils.model_metadata import load_model_metadata

def render_home_content():
    metadata = load_model_metadata() or {}
    metrics = MODEL_METRICS
    best_model_name = metadata.get("best_model_name", "Unknown")
    
    st.markdown(f"<h1 class='glowing-title gradient-text'>{PORTFOLIO_TITLE}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 16px; color: #64748B; margin-top: -6px; margin-bottom: 20px;'>{PORTFOLIO_SUBTITLE}</p>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #0F172A; font-weight: 800;'>Model & Business Key Performance Indicators</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card('F1 Score (Balanced)', f"{metrics.get('F1-Score', 0.6049):.2%}", '#6C63FF', sparkline_data=[0.57, 0.585, 0.592, 0.601, metrics.get('F1-Score', 0.6049)], icon='⚖️')
    with col2:
        render_kpi_card('Recall Rate (Sensitivity)', f"{metrics.get('Recall', 0.5588):.2%}", '#D97706', sparkline_data=[0.51, 0.53, 0.542, 0.551, metrics.get('Recall', 0.5588)], icon='🎯')
    with col3:
        render_kpi_card('ROC-AUC Score', f"{metrics.get('ROC-AUC', 0.8422):.4f}", '#0D9488', sparkline_data=[0.81, 0.825, 0.832, 0.838, metrics.get('ROC-AUC', 0.8422)], icon='📈')
    with col4:
        render_kpi_card('Overall Accuracy', f"{metrics.get('Accuracy', 0.8062):.2%}", '#4F46E5', sparkline_data=[0.78, 0.792, 0.798, 0.802, metrics.get('Accuracy', 0.8062)], icon='🏆')
         
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_main, col_sub = st.columns([2, 1])
    with col_main:
        with st.container(border=True):
            st.markdown(
                """
                <h3 style="margin-top: 0; color: #0F172A; font-weight: 800;">Project Scope & Objectives</h3>
                <p style="color: #334155; line-height: 1.6;">Welcome to the <strong>Customer Churn Prediction System</strong>.</p>
                <p style="color: #334155; line-height: 1.6;">This application uses Machine Learning to predict whether a customer is likely to churn based on demographic information, account details, and subscribed services.</p>
                <p style="color: #334155; line-height: 1.6;">Key system components:</p>
                <ul style="color: #334155; line-height: 1.7;">
                    <li><strong>Data Preprocessing</strong>: Cleaning, encoding, and scale transformations.</li>
                    <li><strong>Exploratory Data Analysis</strong>: Cohort segmentation and billing distributions.</li>
                    <li><strong>Machine Learning Classification</strong>: Benchmark models on historical records.</li>
                    <li><strong>Account Health Dashboard</strong>: Real-time diagnostic evaluation & interactive retention simulator.</li>
                    <li><strong>Model Performance Audit</strong>: Precision-recall trade-offs, ROC metrics, and confusion heatmaps.</li>
                    <li><strong>Business Playbooks</strong>: Strategic recommendations and exportable reports.</li>
                </ul>
                <h4 style="color: #0F172A; font-weight: 700;">Navigation Overview</h4>
                <ol style="color: #334155; line-height: 1.7;">
                    <li><strong>Churn Predictor / Account Health Dashboard</strong>: Interactive customer profile evaluation, retention driver breakdown, and retention simulator.</li>
                    <li><strong>Analytics</strong>: Population distributions, contract ratios, and payment patterns.</li>
                    <li><strong>Model Performance</strong>: Audit classification scores, ROC thresholds, and feature importances.</li>
                    <li><strong>Business Insights</strong>: Strategic action recommendations.</li>
                    <li><strong>Admin Console</strong>: Prediction history query logs.</li>
                </ol>
                """,
                unsafe_allow_html=True
            )
        
    with col_sub:
        with st.container(border=True):
            st.markdown(
                f"""
                <h3 style="margin-top: 0; color: #0F172A; font-weight: 800;">Portfolio Summary</h3>
                <div style="margin-bottom: 12px;">
                    <span style="font-size: 12px; text-transform: uppercase; color: #64748B; font-weight: 700; display: block;">Developer</span>
                    <strong style="font-size: 15px; color: #0F172A;">{DEVELOPER_NAME}</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="font-size: 12px; text-transform: uppercase; color: #64748B; font-weight: 700; display: block;">Project Type</span>
                    <strong style="font-size: 15px; color: #6C63FF;">{PROJECT_TYPE}</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="font-size: 12px; text-transform: uppercase; color: #64748B; font-weight: 700; display: block;">Best Model</span>
                    <strong style="font-size: 15px; color: #0D9488;">{best_model_name}</strong>
                </div>
                <div style="margin-bottom: 12px;">
                    <span style="font-size: 12px; text-transform: uppercase; color: #64748B; font-weight: 700; display: block;">Dataset Source</span>
                    <span style="font-size: 13px; color: #334155;">IBM Watson Telco Churn (7,043 Records)</span>
                </div>
                """,
                unsafe_allow_html=True
            )

render_home_content()
