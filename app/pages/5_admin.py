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
import pandas as pd
from dotenv import load_dotenv
from app.components.styles import inject_premium_styles
from app.components.cards import render_kpi_card
from app.services.history_service import HistoryService

# Load environment variables
load_dotenv()

# Inject styling
inject_premium_styles()

st.markdown("<h1 class='glowing-title gradient-text'>🔐 Admin Console</h1>", unsafe_allow_html=True)

# Authentication configurations from env (fallback values provided for portfolio showcase)
ENV_USER = os.getenv("ADMIN_USER", "naveen")
ENV_PASS = os.getenv("ADMIN_PASS", "naveen@0104")

# Session state authentication logic
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    with st.container(border=True):
        st.subheader("Login Access Required")
        st.write("Enter credentials to unlock prediction history logs:")
        
        with st.form("admin_login_form"):
            username = st.text_input("Username", value="")
            password = st.text_input("Password", type="password", value="")
            login_btn = st.form_submit_button("Authenticate Access", use_container_width=True)
            
        if login_btn:
            if username == ENV_USER and password == ENV_PASS:
                st.session_state.admin_authenticated = True
                st.success("Access Granted.")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    st.stop()

# ----------------- ADMIN DASHBOARD CONTENT -----------------
history_service = HistoryService()

# Sidebar logout shortcut
if st.sidebar.button("🔐 Logout of Admin Session"):
    st.session_state.admin_authenticated = False
    st.rerun()

st.markdown("Monitor historical query logs, audit model inputs, filter risks, and manage files.")

# Load history
df_history = history_service.load_history()

if df_history.empty:
    st.info("No prediction queries logged yet. Please complete a churn prediction query in the Churn Predictor wizard.")
    st.stop()

# Summary analytics of logs
total_predictions = len(df_history)
high_critical_count = len(df_history[df_history['risk_level'].isin(['High', 'Critical'])])
avg_probability = df_history['probability'].mean()

col1, col2, col3 = st.columns(3)
with col1:
    render_kpi_card("Total Logs Audited", f"{total_predictions} queries", "#6C63FF")
with col2:
    render_kpi_card("Avg Churn Risk Score", f"{avg_probability:.2%}", "#FFB347")
with col3:
    render_kpi_card("Elevated Risks (High/Crit)", f"{high_critical_count} alerts", "#FF6B6B" if high_critical_count > 0 else "#00D4AA")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("🔍 Query & Search History")
    
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        search_q = st.text_input("Search logs (e.g. payment method, gender, contract type)", "")
    with col_f2:
        risk_filter = st.multiselect(
            "Risk Class", 
            options=["Low", "Medium", "High", "Critical"], 
            default=["Low", "Medium", "High", "Critical"]
        )
    
    # Apply filters
    df_filtered = df_history[df_history['risk_level'].isin(risk_filter)]
    
    if search_q:
        search_cols = ["gender", "Contract", "PaymentMethod", "risk_level"]
        mask = df_filtered[search_cols].astype(str).apply(lambda x: x.str.contains(search_q, case=False)).any(axis=1)
        df_filtered = df_filtered[mask]
    
    st.markdown("---")
    
    # Render table
    if not df_filtered.empty:
        display_cols = ["timestamp", "gender", "tenure", "Contract", "MonthlyCharges", "TotalCharges", "probability", "risk_level"]
        st.dataframe(
            df_filtered[display_cols].style.format({
                "probability": "{:.1%}",
                "MonthlyCharges": "${:.2f}",
                "TotalCharges": "${:.2f}"
            }),
            use_container_width=True
        )
        
        # Download log capability
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Logs to CSV",
            data=csv_data,
            file_name="churn_logs_export.csv",
            mime="text/csv"
        )
    else:
        st.info("No logged queries matching filters.")

# Maintenance tools
st.subheader("⚙️ Log Maintenance Tools")
with st.expander("⚠️ Danger Zone Operations"):
    st.warning("These operations will permanently delete records from history databases.")
    
    # Deleting individual record
    # Ensure timestamp format matches for comparison
    df_history['timestamp_str'] = df_history['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")
    delete_options = df_history['timestamp_str'].tolist()
    record_to_delete = st.selectbox("Select exact log timestamp to delete", options=delete_options)
    
    if st.button("Delete Selected Log Entry"):
        if history_service.delete_record(record_to_delete):
            st.success(f"Record for timestamp {record_to_delete} deleted successfully.")
            st.rerun()
        else:
            st.error("Failed to delete record.")
            
    st.markdown("---")
    
    if st.button("Clear Prediction Logs Database", type="secondary"):
        history_service.clear_all()
        st.success("All prediction queries cleared successfully.")
        st.rerun()
