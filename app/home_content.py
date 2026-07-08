import streamlit as st
from app.components.cards import render_kpi_card
from app.utils.config import PORTFOLIO_TITLE, PORTFOLIO_SUBTITLE, DEVELOPER_NAME, PROJECT_TYPE

def render_home_content():
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
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.subheader('💡 Project Scope & Objectives')
        st.markdown(
            """
            Welcome to the **Customer Churn Prediction Dashboard**.
            
            This application uses Machine Learning to predict whether a customer is likely to churn based on demographic information, account details, and subscribed services.
            
            This portfolio project demonstrates:
            
            * **Data Preprocessing**: Cleaning, encoding, and scale transformations.
            * **Exploratory Data Analysis**: Cohort segmentation and billing distributions.
            * **Machine Learning Classification**: Training predictive algorithms on historical records.
            * **Customer Churn Prediction**: Real-time diagnostic evaluation of individual customer profiles.
            * **Model Evaluation**: Precision-recall trade-offs, ROC metrics, and confusion audits.
            * **Business Insights**: Data-driven retention recommendation playbooks.
            * **Interactive Dashboard using Streamlit**: Premium user experience for end-to-end auditability.
            """
        )
        
        st.markdown(
            """
            #### 🗺️ Interactive Navigation Map
            Use the sidebar navigation to browse through the system modules:
            
            1. **🔮 Churn Predictor**: Run step-by-step risk scoring validations on individual accounts.
            2. **📊 Analytics**: Explore population distributions, contract ratios, and payment patterns.
            3. **🎯 Model Performance**: Audit classification scores, ROC thresholds, and feature importances.
            4. **💡 Business Insights**: Review automatically generated strategic recommendations.
            5. **🔐 Admin Console**: Search, query, and manage prediction history logs.
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_sub:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.subheader('🛠️ Technical Specifications')
        st.markdown(
            """
            **Pipeline & Modeling**:
            - Scikit-learn Pipeline
            - Logistic Regression Classifier
            - Standard Scaling Transform
            - Binary Label Mappings
            
            **User Interface**:
            - Streamlit Multi-page App
            - Plotly Interactive Visuals
            - Embedded CSS Glassmorphism
            
            **Infrastructure**:
            - Dockerized Deployments
            - CSV-backed Prediction Logger
            - Dynamic PDF Report Generator
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown(
        f"""
        <div style="text-align: center; padding: 40px 10px; margin-top: 50px; border-top: 1px solid rgba(255,255,255,0.06); color: #6c757d; font-size: 14px;">
            <p><strong>{PORTFOLIO_TITLE}</strong></p>
            <p>{PROJECT_TYPE} | Developed by {DEVELOPER_NAME}</p>
            <p>Developed using: Python | Scikit-learn | Pandas | NumPy | Plotly | Streamlit</p>
            <p>&copy; 2026. All Rights Reserved.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    render_home_content()
