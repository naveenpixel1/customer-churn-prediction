import streamlit as st

def render_kpi_card(title: str, value: str, border_color: str = '#6C63FF') -> None:
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color: {border_color};">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_verdict_card(probability: float, risk_level: str, prediction: int, confidence: str = 'Moderate') -> None:
    if risk_level == 'Low':
        risk_color = '#00D4AA'
        risk_bg = 'rgba(0, 212, 170, 0.08)'
        icon = '✅'
        verdict = 'Low Churn Risk'
    elif risk_level == 'Medium':
        risk_color = '#FFB347'
        risk_bg = 'rgba(255, 179, 71, 0.08)'
        icon = '⚠'
        verdict = 'Medium Churn Risk'
    elif risk_level == 'High':
        risk_color = '#FF6B6B'
        risk_bg = 'rgba(255, 107, 107, 0.08)'
        icon = '🚨'
        verdict = 'High Churn Risk'
    else: # Critical
        risk_color = '#E11D48'
        risk_bg = 'rgba(225, 29, 72, 0.08)'
        icon = '🚨'
        verdict = 'High Churn Risk (Critical)'

    st.markdown(
        f"""
        <div class="verdict-box" style="background-color: {risk_bg}; border-left-color: {risk_color}; border-radius: 12px; padding: 20px; margin-bottom: 16px; border-left: 5px solid;">
            <div style="font-size: 13px; text-transform: uppercase; color: #94A3B8; font-weight: 600; letter-spacing: 1px; margin-bottom: 4px;">Model Diagnostic Result</div>
            <div style="font-size: 24px; font-weight: 800; color: #FFFFFF; margin-bottom: 6px;">{icon} {verdict}</div>
            <div style="font-size: 15px; color: #E2E8F0; display: flex; gap: 20px; flex-wrap: wrap;">
                <span>Prediction Probability: <strong style="color: {risk_color}; font-size: 17px;">{probability:.2%}</strong></span>
                <span style="color: rgba(255,255,255,0.15)">|</span>
                <span>Confidence Score: <strong style="color: #6C63FF; font-size: 17px;">{confidence}</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_insight_card(title: str, content: str, category: str = 'warning') -> None:
    css_class = 'insight-card'
    if category == 'danger':
        css_class += ' danger'
    elif category == 'success':
        css_class += ' success'

    st.markdown(
        f"""
        <div class="{css_class}">
            <strong style="font-size: 15px; color: #FFFFFF; display: block; margin-bottom: 6px;">{title}</strong>
            <span style="font-size: 14px; color: #CBD5E1; line-height: 1.5;">{content}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_progress_indicator(current_step: int) -> None:
    steps = [(1, 'Customer Profile'), (2, 'Subscriptions'), (3, 'Financials'), (4, 'Evaluation')]
    html = '<div class="step-container">'
    
    for step_num, step_name in steps:
        active_class = ''
        if step_num < current_step:
            active_class = 'completed'
            indicator = '✓'
        elif step_num == current_step:
            active_class = 'active'
            indicator = str(step_num)
        else:
            indicator = str(step_num)

        html += f"""
        <div class="step-node {active_class}">
            <span class="step-circle">{indicator}</span>
            <span>{step_name}</span>
        </div>
        """
        if step_num < 4:
            html += '<div style="flex-grow: 1; height: 2px; background: rgba(255,255,255,0.06); margin: 0 15px;"></div>'

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
