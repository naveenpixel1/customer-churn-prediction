import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix, 
    classification_report, 
    roc_curve, 
    auc, 
    precision_recall_curve, 
    average_precision_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# Configuration directories
MODEL_DIR = "models"
EVAL_DIR = os.path.join("reports", "evaluation")
os.makedirs(EVAL_DIR, exist_ok=True)

# Use professional styling
sns.set_theme(style="whitegrid")

def load_evaluation_components():
    """Loads the model, scaler, feature layout, and label encoders."""
    model_path = os.path.join(MODEL_DIR, "model.pkl")
    scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
    features_path = os.path.join(MODEL_DIR, "feature_names.pkl")
    mappings_path = os.path.join(MODEL_DIR, "label_encoder.pkl")
    
    for path in [model_path, scaler_path, features_path, mappings_path]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Component not found: {path}. Run src/model_training.py first.")
            
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(features_path)
    binary_mappings = joblib.load(mappings_path)
    
    return model, scaler, feature_names, binary_mappings

def preprocess_eval_data(df, binary_mappings, feature_names):
    """Applies the exact same encoding and features structure to the evaluation dataset."""
    df_encoded = df.copy()
    
    # 1. Apply binary mappings
    for col, mapping in binary_mappings.items():
        df_encoded[col] = df_encoded[col].map(mapping)
        
    df_encoded['Churn'] = df_encoded['Churn'].map({'Yes': 1, 'No': 0})
    
    # 2. Identify multi-class columns
    categorical_cols = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
                        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
                        'Contract', 'PaymentMethod']
    
    # Apply One-Hot Encoding
    df_encoded = pd.get_dummies(df_encoded, columns=categorical_cols, drop_first=True)
    
    # Reindex columns to match the trained layout
    df_encoded = df_encoded.reindex(columns=feature_names + ['Churn'], fill_value=0)
    
    X = df_encoded[feature_names]
    y = df_encoded['Churn']
    
    return X, y

def plot_confusion_matrix(cm):
    """Generates and saves the confusion matrix plot."""
    plt.figure(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                xticklabels=['Predicted No Churn', 'Predicted Churn'], 
                yticklabels=['Actual No Churn', 'Actual Churn'])
    plt.title("Confusion Matrix - Logistic Regression Model")
    plt.ylabel("Actual Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    
    save_path = os.path.join(EVAL_DIR, "confusion_matrix.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def plot_roc_curve(y_test, y_prob):
    """Generates and saves the ROC Curve plot."""
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(7, 6))
    plt.plot(fpr, tpr, color='#d95f02', lw=2, label=f'ROC Curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='#2b5c8f', lw=1, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity / Recall)')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.tight_layout()
    
    save_path = os.path.join(EVAL_DIR, "roc_curve.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def plot_precision_recall_curve(y_test, y_prob):
    """Generates and saves the Precision-Recall Curve plot."""
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)
    
    plt.figure(figsize=(7, 6))
    plt.plot(recall, precision, color='#8c96c6', lw=2, label=f'PR Curve (AP = {pr_auc:.4f})')
    plt.xlabel('Recall (Sensitivity)')
    plt.ylabel('Precision (Positive Predictive Value)')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.tight_layout()
    
    save_path = os.path.join(EVAL_DIR, "precision_recall_curve.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def plot_feature_importance(model, feature_names):
    """
    Extracts coefficients from Logistic Regression, 
    sorts them by absolute magnitude, and saves a bar chart.
    """
    # Logistic regression coefficients represent log-odds impact
    coefficients = model.coef_[0]
    
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefficients,
        'Abs_Coefficient': np.abs(coefficients)
    }).sort_values(by='Abs_Coefficient', ascending=False)
    
    top_importance = importance_df.head(15).copy()
    
    plt.figure(figsize=(10, 8))
    colors = ['#d95f02' if coef > 0 else '#2b5c8f' for coef in top_importance['Coefficient']]
    
    sns.barplot(data=top_importance, x='Coefficient', y='Feature', palette=colors, hue='Feature', legend=False)
    plt.axvline(0, color='black', lw=1, linestyle='--')
    plt.title("Top 15 Feature Importances (Logistic Regression Coefficients)")
    plt.xlabel("Coefficient Value (Positive drives Churn, Negative retains Customer)")
    plt.ylabel("Features")
    plt.tight_layout()
    
    save_path = os.path.join(EVAL_DIR, "feature_importance.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def plot_metrics_comparison_bar(acc, prec, rec, f1):
    """Generates a bar chart comparing the model's primary metrics."""
    metrics = {
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1-Score': f1
    }
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(metrics.keys(), metrics.values(), color=['#2b5c8f', '#8c96c6', '#88419d', '#810f7c'], width=0.5)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.02, f'{height:.2%}', 
                 ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.ylim([0.0, 1.0])
    plt.title("Best Model (Logistic Regression) Core Performance Metrics")
    plt.ylabel("Score (%)")
    plt.tight_layout()
    
    save_path = os.path.join(EVAL_DIR, "metrics_comparison.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved: {save_path}")

def print_detailed_metric_explanations(acc, prec, rec, f1, roc_auc):
    """Prints comprehensive explanation for each metric."""
    print("\n" + "="*80)
    print("=== SENIOR ENGINEER'S METRIC DIAGNOSTIC BREAKDOWN ===")
    print("="*80)
    
    print("\n1. ACCURACY")
    print("   - What it measures: The percentage of total predictions the model got correct (both churn and active).")
    print("   - Why it matters  : Provides a high-level sanity check on general classification power.")
    print(f"   - Current Result  : {acc:.2%} correct. In our project, this means the model correctly labels roughly 8 out of 10 customers.")
    
    print("\n2. PRECISION")
    print("   - What it measures: Out of all customers the model predicted would leave, how many actually left?")
    print("   - Why it matters  : Directly impacts wasted budget. If precision is low, we target many loyal customers, wasting promo offers.")
    print(f"   - Current Result  : {prec:.2%}. If the model flags a customer as a churn risk, there is a {prec:.1%} chance they will actually leave.")
    
    print("\n3. RECALL / SENSITIVITY")
    print("   - What it measures: Out of all customers who actually left, how many did the model successfully find?")
    print("   - Why it matters  : Directly impacts lost revenue (Type II Error). If recall is low, high-risk churners slip away quietly.")
    print(f"   - Current Result  : {rec:.2%}. The model successfully captures {rec:.1%} of our leaving customer base.")
    
    print("\n4. F1-SCORE")
    print("   - What it measures: The harmonic mean of Precision and Recall, providing a single balanced metric.")
    print("   - Why it matters  : Crucial for evaluating model performance under class imbalance without bias.")
    print(f"   - Current Result  : {f1:.2%}. Shows a solid, balanced classification boundary between catching churners and protecting margin.")
    
    print("\n5. ROC-AUC (Area Under ROC Curve)")
    print("   - What it measures: The model's ability to distinguish and rank probability risk scores across all thresholds.")
    print("   - Why it matters  : Benchmarks how well the model separates churners from active base regardless of threshold settings.")
    print(f"   - Current Result  : {roc_auc:.4f}. There is an {roc_auc*100:.1f}% probability that a randomly chosen churner is given a higher risk score than a loyal customer.")

def print_final_summary(acc, prec, rec, f1, roc_auc):
    """Prints clean terminal summary box."""
    print("\n" + "#"*50)
    print("### FINAL SUMMARY - PHASE 6: MODEL EVALUATION ###")
    print("#"*50)
    print("  * Best Model Identified : Logistic Regression")
    print(f"  * Accuracy              : {acc:.4%}")
    print(f"  * Precision             : {prec:.4%}")
    print(f"  * Recall                : {rec:.4%}")
    print(f"  * F1-Score              : {f1:.4%}")
    print(f"  * ROC-AUC               : {roc_auc:.4f}")
    print("#"*50)

def main():
    processed_path = os.path.join("data", "processed", "churn_cleaned.csv")
    print(f"Loading cleaned dataset for evaluation: {processed_path}")
    df = pd.read_csv(processed_path)
    
    # Load model pipeline components
    model, scaler, feature_names, binary_mappings = load_evaluation_components()
    
    # Preprocess & Align layout
    X, y = preprocess_eval_data(df, binary_mappings, feature_names)
    
    # Split using the exact same split logic to isolate the test partition (stratified, random_state=42)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale test features (transform only)
    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    X_test_scaled = X_test.copy()
    X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])
    X_test_scaled = X_test_scaled.astype(float)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    # Get exact scores
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    # Classification Report
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=['No Churn', 'Churn']))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("=== Confusion Matrix Values ===")
    print(f"True Negatives (TN)  : {tn} (Predicted Active, Actually Active)")
    print(f"False Positives (FP) : {fp} (Predicted Churn, Actually Active) - Type I Error")
    print(f"False Negatives (FN) : {fn} (Predicted Active, Actually Churned) - Type II Error")
    print(f"True Positives (TP)  : {tp} (Predicted Churn, Actually Churned)")
    
    # Generate all plots
    print("\nGenerating evaluation plots in reports/evaluation/...")
    plot_confusion_matrix(cm)
    plot_roc_curve(y_test, y_prob)
    plot_precision_recall_curve(y_test, y_prob)
    plot_feature_importance(model, feature_names)
    plot_metrics_comparison_bar(acc, prec, rec, f1)
    
    # Explanations
    print_detailed_metric_explanations(acc, prec, rec, f1, roc_auc)
    
    # Final Summary Box
    print_final_summary(acc, prec, rec, f1, roc_auc)

if __name__ == "__main__":
    main()
