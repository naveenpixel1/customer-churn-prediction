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
from app.components.styles import inject_premium_styles
from app.components.cards import render_insight_card
from app.services.analytics_service import AnalyticsService

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
        f"Higher monthly charges (> $70) increase churn risk significantly, showing a churn rate of <strong>{high_charges_churn:.1%}</strong>, "
        f"compared to only <strong>{low_charges_churn:.1%}</strong> for customers with charges <= $70.",
        "warning"
    )
    
    render_insight_card(
        "💳 Manual Billing vs Auto-pay friction",
        f"Manual billing via <strong>Electronic Check</strong> correlates with a high <strong>{echeck_churn:.1%}</strong> churn rate, "
        f"while automatic billing channels (Credit Card / Bank Transfer) show a low <strong>{autopay_churn:.1%}</strong> churn rate.",
        "danger"
    )

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("💡 Strategic Action Playbooks")

st.markdown(
    """
    <div class="glass-card">
        <h4 style="margin-top:0; color:#FFFFFF; font-weight: 700;">1. Migrate Month-to-Month Cohorts to Annual Terms (Priority: CRITICAL)</h4>
        <p style="color:#CBD5E1; font-size:14px; line-height:1.5;">
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
        <h4 style="margin-top:0; color:#FFFFFF; font-weight: 700;">2. Bundle Online Security and Tech Support Features (Priority: HIGH)</h4>
        <p style="color:#CBD5E1; font-size:14px; line-height:1.5;">
            Subscribers with active Online Security and Tech Support add-ons demonstrate high retention rates (only <b>{yes_security_churn:.1%}</b> churn rate vs <b>{no_security_churn:.1%}</b> for those without). 
            Offer a promotional bundle (e.g., first 3 months of security and tech support free) to month-to-month or new subscribers to anchor their accounts.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="glass-card">
        <h4 style="margin-top:0; color:#FFFFFF; font-weight: 700;">3. Incentivize Auto-Pay Configurations (Priority: MEDIUM)</h4>
        <p style="color:#CBD5E1; font-size:14px; line-height:1.5;">
            Target customers using manual checks (specifically Electronic Check payment methods) with direct-mail or in-app billing prompts 
            offering a one-time $5.00 statement credit for registering an automated Credit Card or Bank Transfer payment source. 
            This eliminates monthly transaction friction and dramatically improves lifetime value (LTV).
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
