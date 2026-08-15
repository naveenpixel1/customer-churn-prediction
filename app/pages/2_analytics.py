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
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from app.components.styles import inject_premium_styles
from app.components.cards import render_kpi_card
from app.services.analytics_service import AnalyticsService
from app.utils.currency import format_currency, get_currency_symbol

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
    render_kpi_card("Total Cohort Count", f"{kpis['total_customers']:,} accounts", "#6C63FF", sparkline_data=[5000, 5800, 6400, 6800, kpis['total_customers']], icon='👥')
with kpi_col2:
    render_kpi_card("Cohort Churn Rate", f"{kpis['churn_rate']:.2%}", "#FF6B6B" if kpis['churn_rate'] > 0.2 else "#00D4AA", sparkline_data=[0.31, 0.29, 0.28, 0.27, kpis['churn_rate']], icon='📉')
with kpi_col3:
    render_kpi_card("Avg Tenure Period", f"{kpis['avg_tenure']:.1f} months", "#FFB347", sparkline_data=[28.0, 29.5, 30.8, 31.5, kpis['avg_tenure']], icon='📅')
with kpi_col4:
    render_kpi_card("Avg Monthly Charge", f"{format_currency(kpis['avg_monthly_charges'])}", "#6C63FF", sparkline_data=[58.0, 60.5, 62.0, 63.8, kpis['avg_monthly_charges']], icon='💵')

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- VISUALIZATION ROWS -----------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    with st.container(border=True):
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
                font=dict(color="#1E293B", family="Plus Jakarta Sans"),
                legend=dict(font=dict(color="#1E293B")),
                margin=dict(l=30, r=30, t=35, b=30),
                height=310
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No matching records for current filters.")

with row1_col2:
    with st.container(border=True):
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
                font=dict(color="#1E293B", family="Plus Jakarta Sans"),
                legend=dict(font=dict(color="#1E293B")),
                margin=dict(l=45, r=25, t=40, b=40),
                height=310,
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155")),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155"))
            )
            st.plotly_chart(fig_tenure, use_container_width=True)
        else:
            st.info("No matching records.")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    with st.container(border=True):
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
                font=dict(color="#1E293B", family="Plus Jakarta Sans"),
                legend=dict(font=dict(color="#1E293B")),
                margin=dict(l=45, r=25, t=40, b=40),
                height=310,
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155")),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155"))
            )
            st.plotly_chart(fig_contract, use_container_width=True)
        else:
            st.info("No data.")

with row2_col2:
    with st.container(border=True):
        st.subheader("💵 Monthly Charges Distribution (Boxplot)")
        
        if not df_filtered.empty:
            fig_charges = px.box(
                df_filtered,
                x="Churn",
                y="MonthlyCharges",
                color="Churn",
                color_discrete_map={"No": "#6C63FF", "Yes": "#FF6B6B"},
                labels={"MonthlyCharges": f"Monthly Charge ({get_currency_symbol()})", "Churn": "Churn Status"}
            )
            fig_charges.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#1E293B", family="Plus Jakarta Sans"),
                legend=dict(font=dict(color="#1E293B")),
                margin=dict(l=45, r=25, t=40, b=40),
                height=310,
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155")),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155"))
            )
            st.plotly_chart(fig_charges, use_container_width=True)
        else:
            st.info("No data.")

row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    with st.container(border=True):
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
                font=dict(color="#1E293B", family="Plus Jakarta Sans"),
                legend=dict(font=dict(color="#1E293B")),
                margin=dict(l=45, r=25, t=40, b=40),
                height=310,
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155")),
                yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155"))
            )
            st.plotly_chart(fig_internet, use_container_width=True)
        else:
            st.info("No data.")

with row3_col2:
    with st.container(border=True):
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
                font=dict(color="#1E293B", family="Plus Jakarta Sans"),
                legend=dict(font=dict(color="#1E293B")),
                margin=dict(l=140, r=25, t=40, b=40),
                height=310,
                xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155")),
                yaxis=dict(showgrid=False, tickfont=dict(color="#334155"))
            )
            st.plotly_chart(fig_payment, use_container_width=True)
        else:
            st.info("No data.")

# Heatmap Row
with st.container(border=True):
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
            font=dict(color="#1E293B", family="Plus Jakarta Sans"),
            margin=dict(l=90, r=25, t=45, b=45),
            height=340,
            xaxis=dict(tickfont=dict(color="#334155")),
            yaxis=dict(tickfont=dict(color="#334155"))
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("No correlation data.")
