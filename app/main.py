"""
Customer Churn Prediction Web Application
Developed by: Naveen Kumar .D
Technologies: Streamlit, Scikit-learn, Pandas, NumPy, Plotly, Joblib, FPDF2
Year: 2026
"""

import os
import sys

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
from app.components.sidebar import render_sidebar
from app.utils.config import PORTFOLIO_TITLE

# Set up page configurations
st.set_page_config(
    page_title=PORTFOLIO_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS dark-theme styling
inject_premium_styles()

# Define multi-page application routing structure
home_page = st.Page(
    "app/home_content.py", 
    title="Home", 
    icon="🏠", 
    default=True
)
predictor_page = st.Page(
    "app/pages/1_predictor.py", 
    title="Churn Predictor", 
    icon="🔮"
)
analytics_page = st.Page(
    "app/pages/2_analytics.py", 
    title="Analytics", 
    icon="📊"
)
model_performance_page = st.Page(
    "app/pages/3_model_performance.py", 
    title="Model Performance", 
    icon="📈"
)
insights_page = st.Page(
    "app/pages/4_insights.py", 
    title="Business Insights", 
    icon="💡"
)
admin_page = st.Page(
    "app/pages/5_admin.py", 
    title="Admin Console", 
    icon="🔐"
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
