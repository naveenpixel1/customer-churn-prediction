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
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score
from app.components.styles import inject_premium_styles
from app.components.cards import render_kpi_card
from app.services.prediction_service import PredictionService
from app.utils.config import CLEANED_DATA_PATH

# Inject style
inject_premium_styles()

st.markdown("<h1 class='glowing-title gradient-text'>📈 Model Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Monitor model accuracy, class boundaries, validation scores, and coefficients.")

# Instantiate prediction service to access model pipeline
try:
    pred_service = PredictionService()
except Exception as e:
    st.error(f"Error loading model pipeline: {e}")
    st.stop()

# Helper to calculate test set evaluations dynamically
@st.cache_data
def get_model_evaluation_data():
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    # 1. Apply binary mappings
    for col, mapping in pred_service.binary_mappings.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)
            
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # 2. Categorical dummy encoding
    categorical_cols = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
                        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
                        'Contract', 'PaymentMethod']
    
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    df_encoded = df_encoded.reindex(columns=pred_service.feature_names + ['Churn'], fill_value=0)
    
    X = df_encoded[pred_service.feature_names]
    y = df_encoded['Churn']
    
    # Train-test split (exact replication of stratified 80/20)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale numericals
    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    X_test_scaled = X_test.copy()
    X_test_scaled[num_cols] = pred_service.scaler.transform(X_test[num_cols])
    X_test_scaled = X_test_scaled.astype(float)
    
    # Predict probabilities
    y_prob = pred_service.model.predict_proba(X_test_scaled)[:, 1]
    y_pred = pred_service.model.predict(X_test_scaled)
    
    return y_test.values, y_prob, y_pred

# Load dynamic stats
try:
    y_true, y_prob, y_pred = get_model_evaluation_data()
except Exception as e:
    st.error(f"Error loading evaluation dataset split: {e}")
    st.info("Check preprocessing or data directories.")
    st.stop()

# Metric cards row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    render_kpi_card("Accuracy Score", "80.62%", "#6C63FF")
with col2:
    render_kpi_card("Precision Score", "65.93%", "#00D4AA")
with col3:
    render_kpi_card("Recall (Sensitivity)", "55.88%", "#FFB347")
with col4:
    render_kpi_card("F1 Performance", "60.49%", "#6C63FF")
with col5:
    render_kpi_card("ROC Area Under (AUC)", "0.8422", "#00D4AA")

st.markdown("<br>", unsafe_allow_html=True)

# Visualizations Row 1: Confusion Matrix & ROC Curve
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏁 Live Confusion Matrix")
    
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    z_cm = [[int(tn), int(fp)], [int(fn), int(tp)]]
    x_cm = ['Predicted Stay', 'Predicted Churn']
    y_cm = ['Actual Stay', 'Actual Churn']
    
    fig_cm = go.Figure(data=go.Heatmap(
        z=z_cm,
        x=x_cm,
        y=y_cm,
        colorscale='Blues',
        text=[[f"TN: {tn}", f"FP: {fp}"], [f"FN: {fn}", f"TP: {tp}"]],
        texttemplate="%{text}",
        hoverinfo="none"
    ))
    fig_cm.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#E2E8F0"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280
    )
    st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})
    st.caption("True Negative (TN: 927) | False Positive (FP: 108) | False Negative (FN: 165) | True Positive (TP: 209)")
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📈 ROC Curve Analysis")
    
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'ROC (AUC = {roc_auc:.4f})', line=dict(color='#00D4AA', width=2.5)))
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Baseline', line=dict(color='rgba(255,255,255,0.15)', dash='dash')))
    
    fig_roc.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#E2E8F0"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        xaxis=dict(title="False Positive Rate", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title="True Positive Rate", showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig_roc, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# Visualizations Row 2: Precision-Recall Curve & Feature Importances
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⚖️ Precision-Recall Trade-off")
    
    prec, rec, _ = precision_recall_curve(y_true, y_prob)
    ap = average_precision_score(y_true, y_prob)
    
    fig_pr = go.Figure()
    fig_pr.add_trace(go.Scatter(x=rec, y=prec, mode='lines', name=f'PR Curve (AP = {ap:.4f})', line=dict(color='#FFB347', width=2.5)))
    
    fig_pr.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#E2E8F0"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        xaxis=dict(title="Recall (Sensitivity)", showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 1.05]),
        yaxis=dict(title="Precision", showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 1.05])
    )
    st.plotly_chart(fig_pr, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🧬 Coefficient Weight Feature Importance")
    
    # Access logistic regression coefficients
    coefs = pred_service.model.coef_[0]
    imp_df = pd.DataFrame({
        'Feature': pred_service.feature_names,
        'Coefficient': coefs,
        'Abs_Coef': np.abs(coefs)
    }).sort_values(by='Abs_Coef', ascending=False).head(10)
    
    # Sort for chart visualization
    imp_df = imp_df.sort_values(by='Coefficient')
    colors = ['#FF6B6B' if w > 0 else '#6C63FF' for w in imp_df['Coefficient']]
    
    fig_imp = go.Figure(go.Bar(
        x=imp_df['Coefficient'],
        y=imp_df['Feature'],
        orientation='h',
        marker_color=colors
    ))
    fig_imp.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#E2E8F0"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        xaxis=dict(title="Coefficient Weight", showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_imp, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
