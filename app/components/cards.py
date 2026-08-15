import html
import streamlit as st
import plotly.graph_objects as go

def render_kpi_card(title: str, value: str, border_color: str = '#6C63FF', sparkline_data: list = None, icon: str = '') -> None:
    icon_html = f'<span style="font-size: 15px; margin-right: 6px;">{icon}</span>' if icon else ''
    
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color: {border_color};">
            <div class="kpi-title">{icon_html}{html.escape(str(title))}</div>
            <div class="kpi-value">{html.escape(str(value))}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if sparkline_data and len(sparkline_data) >= 2:
        # Convert hex border color to rgba fill
        fill_color = f"rgba(108, 99, 255, 0.10)"
        if border_color == '#00D4AA' or border_color == '#0D9488':
            fill_color = f"rgba(0, 212, 170, 0.10)"
        elif border_color == '#FFB347' or border_color == '#D97706':
            fill_color = f"rgba(255, 179, 71, 0.10)"
        elif border_color == '#FF6B6B' or border_color == '#EF4444':
            fill_color = f"rgba(255, 107, 107, 0.10)"

        fig = go.Figure(go.Scatter(
            y=sparkline_data,
            mode='lines',
            fill='tozeroy',
            line=dict(color=border_color, width=2),
            fillcolor=fill_color,
            hoverinfo='none'
        ))
        fig.update_layout(
            height=32,
            margin=dict(l=0, r=0, t=2, b=2),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False, fixedrange=True),
            yaxis=dict(visible=False, fixedrange=True)
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def render_verdict_card(probability: float, risk_level: str, prediction: int, confidence: str = 'Moderate') -> None:
    if risk_level == 'Low':
        risk_color = '#0D9488'
        risk_bg = '#F0FDF4'
        verdict = 'Low Churn Risk'
        summary_text = "Account is stable with healthy retention indicators."
    elif risk_level == 'Medium':
        risk_color = '#D97706'
        risk_bg = '#FFFBEB'
        verdict = 'Medium Churn Risk'
        summary_text = "Account displays moderate risk factors. Proactive engagement advised."
    elif risk_level == 'High':
        risk_color = '#EA580C'
        risk_bg = '#FFEDD5'
        verdict = 'High Churn Risk'
        summary_text = "Account requires immediate care! High probability of churn."
    else:
        risk_color = '#DC2626'
        risk_bg = '#FEF2F2'
        verdict = 'Critical Churn Risk'
        summary_text = "Urgent Intervention Needed! Customer is at imminent risk of cancellation."

    st.markdown(
        f"""
        <div class="verdict-box" style="background-color: {risk_bg}; border-left-color: {risk_color};">
            <div style="font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 4px;">Account Diagnostic Result</div>
            <div style="font-size: 22px; font-weight: 800; color: #0F172A; margin-bottom: 4px;">{verdict}</div>
            <div style="font-size: 14px; color: #475569; margin-bottom: 8px;">{summary_text}</div>
            <div style="font-size: 14px; color: #334155; display: flex; gap: 16px; flex-wrap: wrap;">
                <span>Probability: <strong style="color: {risk_color}; font-size: 16px;">{probability:.1%}</strong></span>
                <span style="color: #CBD5E1">|</span>
                <span>Confidence: <strong style="color: #4F46E5; font-size: 16px;">{confidence}</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_account_health_gauge(probability: float, risk_level: str) -> None:
    prob_pct = probability * 100.0
    if risk_level == 'Low':
        bar_color = '#00D4AA'
        status_msg = "Account in Healthy Standing. Low probability of cancellation."
        status_bg = "#F0FDF4"
        status_border = "#0D9488"
    elif risk_level == 'Medium':
        bar_color = '#FFB347'
        status_msg = "Account displays moderate risk. Monitor contract status."
        status_bg = "#FFFBEB"
        status_border = "#D97706"
    elif risk_level == 'High':
        bar_color = '#FF6B6B'
        status_msg = "High Risk Alert: Account needs immediate care and targeted retention offers."
        status_bg = "#FFEDD5"
        status_border = "#EA580C"
    else:
        bar_color = '#DC2626'
        status_msg = "Critical Alarm: Customer shows imminent cancellation indicators!"
        status_bg = "#FEF2F2"
        status_border = "#DC2626"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_pct,
        number={'suffix': '%', 'font': {'size': 42, 'family': 'Plus Jakarta Sans', 'color': '#0F172A'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Current Churn Risk", 'font': {'size': 14, 'color': '#334155', 'family': 'Plus Jakarta Sans', 'weight': 'bold'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
            'bar': {'color': bar_color, 'thickness': 0.35},
            'bgcolor': "#F1F5F9",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 35], 'color': '#ECFDF5'},
                {'range': [35, 60], 'color': '#FEF3C7'},
                {'range': [60, 100], 'color': '#FEE2E2'}
            ],
            'threshold': {
                'line': {'color': bar_color, 'width': 4},
                'thickness': 0.75,
                'value': prob_pct
            }
        }
    ))
    fig.update_layout(
        height=230,
        margin=dict(l=25, r=25, t=40, b=15),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Plus Jakarta Sans", color="#1E293B")
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown(
        f"""
        <div style="background-color: {status_bg}; border-left: 4px solid {status_border}; padding: 12px 16px; border-radius: 8px; font-size: 13px; color: #1E293B; font-weight: 600; margin-top: -10px;">
            {status_msg}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_retention_driver_split(top_risk_drivers: list, top_mitigating_drivers: list) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="font-weight: 700; font-size: 14px; color: #DC2626; margin-bottom: 10px;">Top Churn Accelerators</div>', unsafe_allow_html=True)
        if not top_risk_drivers:
            st.markdown('<div style="font-size: 13px; color: #64748B;">No significant risk drivers detected.</div>', unsafe_allow_html=True)
        else:
            for item in top_risk_drivers[:4]:
                pct = item.get('prob_impact_pct', 0.0)
                label = html.escape(str(item.get('label', item.get('feature_raw', ''))))
                st.markdown(
                    f'<div class="driver-card accelerator" style="display: flex; justify-content: space-between; align-items: center;">'
                    f'<span style="font-size: 13px; font-weight: 600; color: #991B1B;">{label}</span>'
                    f'<span style="font-size: 13px; font-weight: 800; color: #DC2626; background: #FEE2E2; padding: 2px 8px; border-radius: 6px;">+{pct:.1f}%</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
    with col2:
        st.markdown('<div style="font-weight: 700; font-size: 14px; color: #0D9488; margin-bottom: 10px;">Protective Factors</div>', unsafe_allow_html=True)
        if not top_mitigating_drivers:
            st.markdown('<div style="font-size: 13px; color: #64748B;">No major protective factors active.</div>', unsafe_allow_html=True)
        else:
            for item in top_mitigating_drivers[:4]:
                pct = item.get('prob_impact_pct', 0.0)
                label = html.escape(str(item.get('label', item.get('feature_raw', ''))))
                st.markdown(
                    f'<div class="driver-card protective" style="display: flex; justify-content: space-between; align-items: center;">'
                    f'<span style="font-size: 13px; font-weight: 600; color: #065F46;">{label}</span>'
                    f'<span style="font-size: 13px; font-weight: 800; color: #0D9488; background: #E6FFFA; padding: 2px 8px; border-radius: 6px;">{pct:.1f}%</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

def render_risk_transition_badge(orig_prob: float, sim_prob: float, orig_risk: str, sim_risk: str) -> None:
    def get_badge(rl):
        if rl in ['Low']:
            return 'background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0;'
        elif rl in ['Medium']:
            return 'background: #FEF3C7; color: #D97706; border: 1px solid #FDE68A;'
        else:
            return 'background: #FEE2E2; color: #DC2626; border: 1px solid #FCA5A5;'

    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin: 16px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
            <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748B; margin-bottom: 12px; letter-spacing: 0.5px;">Before & After Retention Simulation</div>
            <div style="display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; gap: 12px;">
                <div style="text-align: center; flex: 1; min-width: 140px;">
                    <div style="font-size: 12px; color: #64748B; font-weight: 600; margin-bottom: 4px;">CURRENT RISK</div>
                    <div style="font-size: 26px; font-weight: 800; color: #0F172A;">{orig_prob:.1%}</div>
                    <span style="font-size: 12px; font-weight: 700; padding: 3px 10px; border-radius: 12px; {get_badge(orig_risk)}">{orig_risk.upper()}</span>
                </div>
                <div style="font-size: 28px; color: #6C63FF; font-weight: 800;">&#10140;</div>
                <div style="text-align: center; flex: 1; min-width: 140px;">
                    <div style="font-size: 12px; color: #64748B; font-weight: 600; margin-bottom: 4px;">SIMULATED NEW RISK</div>
                    <div style="font-size: 26px; font-weight: 800; color: #0D9488;">{sim_prob:.1%}</div>
                    <span style="font-size: 12px; font-weight: 700; padding: 3px 10px; border-radius: 12px; {get_badge(sim_risk)}">{sim_risk.upper()}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_mitigation_success_box(reduction_pct: float, clv_impact: float = 1000.0) -> None:
    st.markdown(
        f"""
        <div style="background: #F0FDF4; border: 1px solid #A7F3D0; border-left: 5px solid #0D9488; border-radius: 12px; padding: 18px; margin-top: 14px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <strong style="font-size: 16px; color: #065F46;">Successful Mitigation Likely</strong>
            </div>
            <p style="font-size: 14px; color: #047857; margin: 0 0 8px 0; line-height: 1.5;">
                Applying the selected offer levers reduces churn probability by
                <strong style="color: #047857; font-weight: 800;">{reduction_pct:.1f} percentage points</strong>.
            </p>
            <div style="font-size: 13px; color: #065F46; background: #DCFCE7; padding: 8px 12px; border-radius: 8px; display: inline-block; font-weight: 600;">
                Estimated Lifetime Value Preserved: <strong>+${clv_impact:,.0f}</strong>
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
            <strong style="font-size: 15px; color: #0F172A; display: block; margin-bottom: 6px;">{html.escape(str(title))}</strong>
            <span style="font-size: 14px; color: #334155; line-height: 1.5;">{html.escape(str(content))}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
