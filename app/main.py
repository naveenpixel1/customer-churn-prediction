"""
Customer Churn Prediction Web Application
Developed by: Naveen Kumar .D
Technologies: Streamlit, Scikit-learn, Pandas, NumPy, Plotly, Joblib, FPDF2
Year: 2026
"""

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

import streamlit as st
from app.components.styles import inject_premium_styles
from app.components.sidebar import render_sidebar
from app.utils.config import PORTFOLIO_TITLE

# Set up page configurations
st.set_page_config(
    page_title=PORTFOLIO_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS light-theme styling
inject_premium_styles()

# Inject security headers via meta tags (Items #18, #19)
st.markdown(
    """
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
    <meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=()">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data: blob:; frame-ancestors 'none';">
    """,
    unsafe_allow_html=True
)

# Define multi-page application routing structure
home_page = st.Page(
    "home_content.py", 
    title="Home", 
    default=True
)
predictor_page = st.Page(
    "pages/1_predictor.py", 
    title="Churn Predictor"
)
analytics_page = st.Page(
    "pages/2_analytics.py", 
    title="Analytics"
)
model_performance_page = st.Page(
    "pages/3_model_performance.py", 
    title="Model Performance"
)
insights_page = st.Page(
    "pages/4_insights.py", 
    title="Business Insights"
)
admin_page = st.Page(
    "pages/5_admin.py", 
    title="Admin Console"
)

# Set up multi-page navigation
pg = st.navigation({
    "Navigation": [
        home_page, 
        predictor_page, 
        analytics_page, 
        model_performance_page, 
        insights_page, 
        admin_page
    ]
})

# Render portfolio sidebar components
render_sidebar()

# Run application lifecycle routing
pg.run()
