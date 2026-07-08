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
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 class='glowing-title'>🔄 End-to-End Machine Learning Pipeline</h3>", unsafe_allow_html=True)
    st.markdown(
        """<div class="glass-card fade-in" style="padding: 20px;">
<p style="color: #94A3B8; font-size: 14px; margin-top:0; margin-bottom: 20px;">The diagram below illustrates the live data preprocessing, scaling transformation, and classification inference pipeline executed upon customer evaluation.</p>
<svg viewBox="0 0 800 120" xmlns="http://www.w3.org/2000/svg" style="background: rgba(15, 18, 36, 0.4); border-radius: 12px; border: 1px solid rgba(108, 99, 255, 0.15); padding: 15px; width: 100%;">
<style>
@keyframes crawl {
    to {
        stroke-dashoffset: -12;
    }
}
.flow-line {
    stroke-dasharray: 6,6;
    animation: crawl 0.8s linear infinite;
}
@keyframes pulse-glow {
    0% { filter: drop-shadow(0 0 2px rgba(108,99,255,0.15)); }
    100% { filter: drop-shadow(0 0 5px rgba(0,212,170,0.45)); }
}
.glowing-node {
    animation: pulse-glow 2s ease-in-out infinite alternate;
}
</style>
<defs>
<linearGradient id="purple-cyan" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#8B5CF6" />
<stop offset="100%" stop-color="#00D4AA" />
</linearGradient>
</defs>
<rect x="10" y="25" width="130" height="50" rx="8" fill="rgba(108,99,255,0.08)" stroke="#6C63FF" stroke-width="1.5" class="glowing-node" />
<text x="75" y="48" fill="#E2E8F0" font-size="11" font-weight="600" text-anchor="middle">Step 1: Input</text>
<text x="75" y="62" fill="#94A3B8" font-size="9" text-anchor="middle">Demographics & Services</text>

<line x1="140" y1="50" x2="165" y2="50" stroke="rgba(0, 212, 170, 0.15)" stroke-width="2" />
<line x1="140" y1="50" x2="165" y2="50" stroke="#00D4AA" stroke-width="2" class="flow-line" />
<polygon points="165,46 172,50 165,54" fill="#00D4AA" />

<rect x="172" y="25" width="130" height="50" rx="8" fill="rgba(108,99,255,0.08)" stroke="#6C63FF" stroke-width="1.5" class="glowing-node" />
<text x="237" y="48" fill="#E2E8F0" font-size="11" font-weight="600" text-anchor="middle">Step 2: Preprocess</text>
<text x="237" y="62" fill="#94A3B8" font-size="9" text-anchor="middle">One-Hot Dummies Alignment</text>

<line x1="302" y1="50" x2="327" y2="50" stroke="rgba(0, 212, 170, 0.15)" stroke-width="2" />
<line x1="302" y1="50" x2="327" y2="50" stroke="#00D4AA" stroke-width="2" class="flow-line" />
<polygon points="327,46 334,50 327,54" fill="#00D4AA" />

<rect x="334" y="25" width="130" height="50" rx="8" fill="rgba(108,99,255,0.08)" stroke="#6C63FF" stroke-width="1.5" class="glowing-node" />
<text x="399" y="48" fill="#E2E8F0" font-size="11" font-weight="600" text-anchor="middle">Step 3: Scale</text>
<text x="399" y="62" fill="#94A3B8" font-size="9" text-anchor="middle">Robust Scaling (scaler.pkl)</text>

<line x1="464" y1="50" x2="489" y2="50" stroke="rgba(0, 212, 170, 0.15)" stroke-width="2" />
<line x1="464" y1="50" x2="489" y2="50" stroke="#00D4AA" stroke-width="2" class="flow-line" />
<polygon points="489,46 496,50 489,54" fill="#00D4AA" />

<rect x="496" y="25" width="130" height="50" rx="8" fill="rgba(108, 99, 255, 0.15)" stroke="url(#purple-cyan)" stroke-width="2" class="glowing-node" />
<text x="561" y="48" fill="#FFFFFF" font-size="11" font-weight="700" text-anchor="middle">Step 4: Predict</text>
<text x="561" y="62" fill="#00D4AA" font-size="9" font-weight="600" text-anchor="middle">Inference (model.pkl)</text>

<line x1="626" y1="50" x2="651" y2="50" stroke="rgba(0, 212, 170, 0.15)" stroke-width="2" />
<line x1="626" y1="50" x2="651" y2="50" stroke="#00D4AA" stroke-width="2" class="flow-line" />
<polygon points="651,46 658,50 651,54" fill="#00D4AA" />

<rect x="658" y="25" width="130" height="50" rx="8" fill="rgba(0,212,170,0.08)" stroke="#00D4AA" stroke-width="1.5" class="glowing-node" />
<text x="723" y="48" fill="#E2E8F0" font-size="11" font-weight="600" text-anchor="middle">Step 5: Explain</text>
<text x="723" y="62" fill="#94A3B8" font-size="9" text-anchor="middle">Log-Odds Feature Drivers</text>
</svg>
</div>""",
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
