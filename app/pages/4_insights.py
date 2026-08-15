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
import plotly.graph_objects as go
from app.components.styles import inject_premium_styles
from app.components.cards import render_insight_card
from app.services.analytics_service import AnalyticsService
from app.utils.currency import format_currency

# Inject styling
inject_premium_styles()

st.markdown("<h1 class='glowing-title gradient-text'>💡 Business Insights</h1>", unsafe_allow_html=True)
st.markdown("Dynamic data-driven observations and strategic business recommendations compiled directly from customer data profiles.")

# Load dataset to extract dynamic numbers
try:
    analytics = AnalyticsService()
    df = analytics.df
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Helper statistics calculated dynamically
# 1. Month-to-month Churn vs Contract Churn
m2m_churn = df[df['Contract'] == 'Month-to-month']['Churn'].value_counts(normalize=True).get('Yes', 0.0)
annual_churn = df[df['Contract'].isin(['One year', 'Two year'])]['Churn'].value_counts(normalize=True).get('Yes', 0.0)

# 2. Fiber Optic Churn vs DSL Churn
fiber_churn = df[df['InternetService'] == 'Fiber optic']['Churn'].value_counts(normalize=True).get('Yes', 0.0)
dsl_churn = df[df['InternetService'] == 'DSL']['Churn'].value_counts(normalize=True).get('Yes', 0.0)

# 3. Tenure impact (Long vs Short tenure)
long_tenure_churn = df[df['tenure'] > 24]['Churn'].value_counts(normalize=True).get('Yes', 0.0)
short_tenure_churn = df[df['tenure'] <= 24]['Churn'].value_counts(normalize=True).get('Yes', 0.0)

# 4. Monthly charges impact (High vs Low charges)
high_charges_churn = df[df['MonthlyCharges'] > 70]['Churn'].value_counts(normalize=True).get('Yes', 0.0)
low_charges_churn = df[df['MonthlyCharges'] <= 70]['Churn'].value_counts(normalize=True).get('Yes', 0.0)

# 5. Electronic check vs Auto-pay churn
echeck_churn = df[df['PaymentMethod'] == 'Electronic check']['Churn'].value_counts(normalize=True).get('Yes', 0.0)
autopay_churn = df[df['PaymentMethod'].str.contains('automatic')]['Churn'].value_counts(normalize=True).get('Yes', 0.0)

# 6. Security & Tech Support Add-ons
no_security_churn = df[df['OnlineSecurity'] == 'No']['Churn'].value_counts(normalize=True).get('Yes', 0.0)
yes_security_churn = df[df['OnlineSecurity'] == 'Yes']['Churn'].value_counts(normalize=True).get('Yes', 0.0)

st.subheader("📋 Top Churn Risk Insights")

col1, col2 = st.columns(2)

with col1:
    render_insight_card(
        "📄 Contract Structure Impact",
        f"Customers with <strong>month-to-month contracts</strong> are far more likely to churn, exhibiting a rate of <strong>{m2m_churn:.1%}</strong>, "
        f"compared to only <strong>{annual_churn:.1%}</strong> for customers on annual/two-year agreements. "
        "Month-to-month terms represent the single largest churn risk signature.",
        "danger"
    )
    
    render_insight_card(
        "📶 Fiber Optic Service Concern",
        f"Customers subscribed to premium <strong>Fiber Optic</strong> internet service churn at <strong>{fiber_churn:.1%}</strong>, "
        f"substantially higher than DSL subscribers (<strong>{dsl_churn:.1%}</strong>). This suggests technical billing issues or quality concerns.",
        "danger"
    )
    
    render_insight_card(
        "🔒 Online Security Anchoring effect",
        f"Subscribers with active Online Security show high retention rates (only <strong>{yes_security_churn:.1%}</strong> churn "
        f"vs <strong>{no_security_churn:.1%}</strong> for those without), proving that security features act as strong loyalty anchors.",
        "success"
    )

with col2:
    render_insight_card(
        "📅 Active Tenure Sticky effect",
        f"Long-tenure customers (>24 months) have a significantly <strong>lower churn probability</strong> of <strong>{long_tenure_churn:.1%}</strong>, "
        f"whereas short-tenure customers (<=24 months) show a higher churn probability of <strong>{short_tenure_churn:.1%}</strong>.",
        "success"
    )

    render_insight_card(
        "💵 Monthly Charges Price Sensitivity",
        f"Higher monthly charges (> {format_currency(70.0)}) increase churn risk significantly, showing a churn rate of <strong>{high_charges_churn:.1%}</strong>, "
        f"compared to only <strong>{low_charges_churn:.1%}</strong> for customers with charges <= {format_currency(70.0)}.",
        "warning"
    )
    
    render_insight_card(
        "💳 Manual Billing vs Auto-pay friction",
        f"Manual billing via <strong>Electronic Check</strong> correlates with a high <strong>{echeck_churn:.1%}</strong> churn rate, "
        f"while automatic billing channels (Credit Card / Bank Transfer) show a low <strong>{autopay_churn:.1%}</strong> churn rate.",
        "danger"
    )

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📊 Visualizing Key Churn Drivers")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    with st.container(border=True):
        st.markdown("<h4 style='margin-top:0; color:#0F172A;'>📝 Churn Risk by Contract Type</h4>", unsafe_allow_html=True)
        # Calculate risk rates
        contract_order = ["Month-to-month", "One year", "Two year"]
        rates = [df[df['Contract'] == c]['Churn'].value_counts(normalize=True).get('Yes', 0.0) * 100 for c in contract_order]
        fig_c = go.Figure(go.Bar(
            x=rates,
            y=contract_order,
            orientation='h',
            marker=dict(
                color=['#FF6B6B', '#FFB347', '#00D4AA'],
                line=dict(color='#E2E8F0', width=1)
            )
        ))
        fig_c.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#1E293B", family="Plus Jakarta Sans"),
            margin=dict(l=20, r=20, t=35, b=25),
            height=180,
            xaxis=dict(title="Churn Rate (%)", showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155")),
            yaxis=dict(showgrid=False, tickfont=dict(color="#334155"))
        )
        st.plotly_chart(fig_c, use_container_width=True, config={"displayModeBar": False})

with chart_col2:
    with st.container(border=True):
        st.markdown("<h4 style='margin-top:0; color:#0F172A;'>💳 Churn Risk by Payment Channel</h4>", unsafe_allow_html=True)
        pm_methods = ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
        rates_pm = [df[df['PaymentMethod'] == p]['Churn'].value_counts(normalize=True).get('Yes', 0.0) * 100 for p in pm_methods]
        
        # Sort values
        sorted_pm = sorted(zip(pm_methods, rates_pm), key=lambda x: x[1])
        pm_y = [x[0] for x in sorted_pm]
        pm_x = [x[1] for x in sorted_pm]
        
        fig_p = go.Figure(go.Bar(
            x=pm_x,
            y=pm_y,
            orientation='h',
            marker=dict(
                color=['#00D4AA', '#00D4AA', '#FFB347', '#FF6B6B'],
                line=dict(color='#E2E8F0', width=1)
            )
        ))
        fig_p.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#1E293B", family="Plus Jakarta Sans"),
            margin=dict(l=20, r=20, t=35, b=25),
            height=180,
            xaxis=dict(title="Churn Rate (%)", showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#334155")),
            yaxis=dict(showgrid=False, tickfont=dict(color="#334155"))
        )
        st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("💡 Strategic Action Playbooks")

st.markdown(
    """
    <div class="glass-card">
        <h4 style="margin-top:0; color:#0F172A; font-weight: 700;">1. Migrate Month-to-Month Cohorts to Annual Terms (Priority: CRITICAL)</h4>
        <p style="color:#334155; font-size:14px; line-height:1.6;">
            Since month-to-month status is the highest risk marker, implement automated marketing incentives offering 
            a billing discount (e.g. 10-15% discount for 12 months) in exchange for switching to a 1 or 2-year contract. 
            The cost of the promotion is far lower than customer replacement acquisition costs.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="glass-card">
        <h4 style="margin-top:0; color:#0F172A; font-weight: 700;">2. Bundle Online Security and Tech Support Features (Priority: HIGH)</h4>
        <p style="color:#334155; font-size:14px; line-height:1.6;">
            Subscribers with active Online Security and Tech Support add-ons demonstrate high retention rates (only <b>{yes_security_churn:.1%}</b> churn rate vs <b>{no_security_churn:.1%}</b> for those without). 
            Offer a promotional bundle (e.g., first 3 months of security and tech support free) to month-to-month or new subscribers to anchor their accounts.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="glass-card">
        <h4 style="margin-top:0; color:#0F172A; font-weight: 700;">3. Incentivize Auto-Pay Configurations (Priority: MEDIUM)</h4>
        <p style="color:#334155; font-size:14px; line-height:1.6;">
            Target customers using manual checks (specifically Electronic Check payment methods) with direct-mail or in-app billing prompts 
            offering a one-time {format_currency(5.0)} statement credit for registering an automated Credit Card or Bank Transfer payment source. 
            This eliminates monthly transaction friction and dramatically improves lifetime value (LTV).
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
