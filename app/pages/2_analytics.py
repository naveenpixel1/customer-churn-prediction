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
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from app.components.styles import inject_premium_styles
from app.components.cards import render_kpi_card
from app.services.analytics_service import AnalyticsService

# Inject styling
inject_premium_styles()

st.markdown("<h1 class='glowing-title gradient-text'>📊 Customer Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Inspect distributions, billing trends, contract relationships, and correlation variables.")

# Instantiate service
try:
    analytics = AnalyticsService()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.info("Make sure the dataset preprocessing pipeline was completed by running `python src/preprocess.py` first.")
    st.stop()

# Sidebar filter selections
st.sidebar.subheader("🔍 Filter Cohorts")
contracts = st.sidebar.multiselect(
    "Contract Terms", 
    options=["Month-to-month", "One year", "Two year"], 
    default=["Month-to-month", "One year", "Two year"]
)
internets = st.sidebar.multiselect(
    "Internet Service Options", 
    options=["DSL", "Fiber optic", "No"], 
    default=["DSL", "Fiber optic", "No"]
)
seniors = st.sidebar.selectbox(
    "Senior Citizen Cohort", 
    options=["All Customers", "Senior Citizen Only", "Non-Senior Only"]
)

# Apply filters
df_filtered = analytics.filter_data(
    contract_types=contracts, 
    internet_services=internets, 
    senior_citizen=seniors
)

# Render KPIs
kpis = analytics.get_summary_stats(df_filtered)

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
with kpi_col1:
    render_kpi_card("Total Cohort Count", f"{kpis['total_customers']:,} accounts", "#6C63FF")
with kpi_col2:
    render_kpi_card("Cohort Churn Rate", f"{kpis['churn_rate']:.2%}", "#FF6B6B" if kpis['churn_rate'] > 0.2 else "#00D4AA")
with kpi_col3:
    render_kpi_card("Avg Tenure Period", f"{kpis['avg_tenure']:.1f} months", "#FFB347")
with kpi_col4:
    render_kpi_card("Avg Monthly Charge", f"${kpis['avg_monthly_charges']:.2f}", "#6C63FF")

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- VISUALIZATION ROWS -----------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🥧 Overall Retention Distribution")
    
    churn_counts = df_filtered['Churn'].value_counts()
    if not churn_counts.empty:
        fig_pie = px.pie(
            names=churn_counts.index,
            values=churn_counts.values,
            hole=0.45,
            color=churn_counts.index,
            color_discrete_map={"No": "#6C63FF", "Yes": "#FF6B6B"},
            labels={"names": "Churned?"}
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E2E8F0"),
            margin=dict(l=20, r=20, t=20, b=20),
            height=300
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No matching records for current filters.")
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📅 Tenure Analysis Histogram")
    
    if not df_filtered.empty:
        fig_tenure = px.histogram(
            df_filtered,
            x="tenure",
            color="Churn",
            barmode="overlay",
            color_discrete_map={"No": "#6C63FF", "Yes": "#FF6B6B"},
            labels={"tenure": "Active Tenure (Months)", "count": "Customer Count"},
            opacity=0.65
        )
        fig_tenure.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E2E8F0"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig_tenure, use_container_width=True)
    else:
        st.info("No matching records.")
    st.markdown('</div>', unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📝 Contract Type vs Churn Count")
    
    if not df_filtered.empty:
        contract_data = df_filtered.groupby(['Contract', 'Churn']).size().reset_index(name='Count')
        fig_contract = px.bar(
            contract_data,
            x="Contract",
            y="Count",
            color="Churn",
            barmode="group",
            color_discrete_map={"No": "#6C63FF", "Yes": "#FF6B6B"},
            labels={"Count": "Customer Count"}
        )
        fig_contract.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E2E8F0"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig_contract, use_container_width=True)
    else:
        st.info("No data.")
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💵 Monthly Charges Distribution (Boxplot)")
    
    if not df_filtered.empty:
        fig_charges = px.box(
            df_filtered,
            x="Churn",
            y="MonthlyCharges",
            color="Churn",
            color_discrete_map={"No": "#6C63FF", "Yes": "#FF6B6B"},
            labels={"MonthlyCharges": "Monthly Charge ($)", "Churn": "Churn Status"}
        )
        fig_charges.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E2E8F0"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig_charges, use_container_width=True)
    else:
        st.info("No data.")
    st.markdown('</div>', unsafe_allow_html=True)

row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📶 Internet Service Provider Type vs Churn")
    
    if not df_filtered.empty:
        internet_data = df_filtered.groupby(['InternetService', 'Churn']).size().reset_index(name='Count')
        fig_internet = px.bar(
            internet_data,
            x="InternetService",
            y="Count",
            color="Churn",
            barmode="group",
            color_discrete_map={"No": "#6C63FF", "Yes": "#FF6B6B"},
            labels={"Count": "Customer Count"}
        )
        fig_internet.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E2E8F0"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig_internet, use_container_width=True)
    else:
        st.info("No data.")
    st.markdown('</div>', unsafe_allow_html=True)

with row3_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💳 Churn Counts by Payment Method")
    
    if not df_filtered.empty:
        payment_data = df_filtered.groupby(['PaymentMethod', 'Churn']).size().reset_index(name='Count')
        fig_payment = px.bar(
            payment_data,
            x="Count",
            y="PaymentMethod",
            color="Churn",
            orientation='h',
            color_discrete_map={"No": "#6C63FF", "Yes": "#FF6B6B"},
            labels={"Count": "Customer Count", "PaymentMethod": "Payment Channel"}
        )
        fig_payment.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#E2E8F0"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_payment, use_container_width=True)
    else:
        st.info("No data.")
    st.markdown('</div>', unsafe_allow_html=True)

# Heatmap Row
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🔗 Correlation Heatmap (Continuous Variables)")

if not df_filtered.empty:
    df_corr = df_filtered.copy()
    df_corr['Churn_Numeric'] = df_corr['Churn'].map({"Yes": 1, "No": 0})
    numeric_cols = ['tenure', 'SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'Churn_Numeric']
    
    exist_numeric = [col for col in numeric_cols if col in df_corr.columns]
    df_corr['TotalCharges'] = pd.to_numeric(df_corr['TotalCharges'], errors='coerce').fillna(0.0)
    
    corr = df_corr[exist_numeric].corr()
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        colorscale='Viridis',
        zmin=-1, zmax=1,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        hoverongaps=False
    ))
    fig_heatmap.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#E2E8F0"),
        margin=dict(l=10, r=10, t=30, b=10),
        height=320
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    st.info("No correlation data.")
st.markdown('</div>', unsafe_allow_html=True)
