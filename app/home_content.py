import streamlit as st
from app.components.styles import inject_premium_styles
from app.components.cards import render_kpi_card
from app.utils.config import PORTFOLIO_TITLE, PORTFOLIO_SUBTITLE, DEVELOPER_NAME, PROJECT_TYPE

def render_home_content():
    inject_premium_styles()
    st.markdown(f"<h1 class='glowing-title gradient-text'>{PORTFOLIO_TITLE}</h1>", unsafe_allow_html=True)
    st.write(PORTFOLIO_SUBTITLE)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='glowing-title'>📊 Key Performance Indicators</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card('Overall Model Accuracy', '80.62%', '#6C63FF')
    with col2:
        render_kpi_card('ROC-AUC Score', '0.8422', '#00D4AA')
    with col3:
        render_kpi_card('Average Customer Tenure', '32.4 months', '#FFB347')
    with col4:
        render_kpi_card('Dataset Size', '7,043 clients', '#6C63FF')
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_main, col_sub = st.columns([2, 1])
    with col_main:
        st.markdown(
            """
            <div class="glass-card fade-in">
                <h3 style="margin-top: 0; color: #FFFFFF;">💡 Project Scope & Objectives</h3>
                <p>Welcome to the <strong>Customer Churn Prediction Dashboard</strong>.</p>
                <p>This application uses Machine Learning to predict whether a customer is likely to churn based on demographic information, account details, and subscribed services.</p>
                <p>This portfolio project demonstrates:</p>
                <ul>
                    <li><strong>Data Preprocessing</strong>: Cleaning, encoding, and scale transformations.</li>
                    <li><strong>Exploratory Data Analysis</strong>: Cohort segmentation and billing distributions.</li>
                    <li><strong>Machine Learning Classification</strong>: Training predictive algorithms on historical records.</li>
                    <li><strong>Customer Churn Prediction</strong>: Real-time diagnostic evaluation of individual customer profiles.</li>
                    <li><strong>Model Evaluation</strong>: Precision-recall trade-offs, ROC metrics, and confusion audits.</li>
                    <li><strong>Business Insights</strong>: Data-driven retention recommendation playbooks.</li>
                    <li><strong>Interactive Dashboard using Streamlit</strong>: Premium user experience for end-to-end auditability.</li>
                </ul>
                <h4 style="color: #FFFFFF;">🗺️ Interactive Navigation Map</h4>
                <p>Use the sidebar navigation to browse through the system modules:</p>
                <ol>
                    <li><strong>🔮 Churn Predictor</strong>: Run step-by-step risk scoring validations on individual accounts.</li>
                    <li><strong>📊 Analytics</strong>: Explore population distributions, contract ratios, and payment patterns.</li>
                    <li><strong>🎯 Model Performance</strong>: Audit classification scores, ROC thresholds, and feature importances.</li>
                    <li><strong>💡 Business Insights</strong>: Review automatically generated strategic recommendations.</li>
                    <li><strong>🔐 Admin Console</strong>: Search, query, and manage prediction history logs.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_sub:
        st.markdown(
            """
            <div class="glass-card fade-in">
                <h3 style="margin-top: 0; color: #FFFFFF;">🛠️ Technical Specifications</h3>
                <p><strong>Pipeline & Modeling</strong>:</p>
                <ul>
                    <li>Scikit-learn Pipeline</li>
                    <li>Logistic Regression Classifier</li>
                    <li>Standard Scaling Transform</li>
                    <li>Binary Label Mappings</li>
                </ul>
                <p><strong>User Interface</strong>:</p>
                <ul>
                    <li>Streamlit Multi-page App</li>
                    <li>Plotly Interactive Visuals</li>
                    <li>Embedded CSS Glassmorphism</li>
                </ul>
                <p><strong>Infrastructure</strong>:</p>
                <ul>
                    <li>Dockerized Deployments</li>
                    <li>CSV-backed Prediction Logger</li>
                    <li>Dynamic PDF Report Generator</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown(
        f"""
        <div style="text-align: center; padding: 40px 10px; margin-top: 50px; border-top: 1px solid rgba(255,255,255,0.06); color: #6c757d; font-size: 14px;">
            <p><strong>{PORTFOLIO_TITLE}</strong></p>
            <p>{PROJECT_TYPE} | Developed by {DEVELOPER_NAME}</p>
            <p><a href="https://github.com/naveenpixel1/customer-churn-prediction" target="_blank" style="color: #6C63FF; text-decoration: none; font-weight: 600;">Code Repository on GitHub</a></p>
            <p>Developed using: Python | Scikit-learn | Pandas | NumPy | Plotly | Streamlit</p>
            <p>&copy; 2026. All Rights Reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    render_home_content()
