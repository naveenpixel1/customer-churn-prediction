import os
import sys
import joblib
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

# Ensure project root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.preprocess import load_data, clean_data, save_processed_data
from src.model_training import preprocess_and_encode, split_and_scale, train_and_evaluate_models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_retraining_pipeline() -> Dict[str, Any]:
    """
    Executes the full automated retraining pipeline:
    1. Loads raw dataset and cleans data.
    2. Integrates query logs from data/history.csv if available.
    3. Preprocesses and scales features.
    4. Trains and benchmarks models (Logistic Regression, Decision Tree, Random Forest, XGBoost).
    5. Identifies best performing model based on ROC-AUC.
    6. Saves updated artifacts to models/ directory.
    """
    logger.info("--- Starting Automated Retraining Pipeline ---")
    
    raw_path = os.path.join("data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
    processed_path = os.path.join("data", "processed", "churn_cleaned.csv")
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    
    # 1. Load and Clean Raw Data
    df_raw = load_data(raw_path)
    df_cleaned = clean_data(df_raw)
    
    # 2. Merge History Logs if available
    history_path = os.path.join("data", "history.csv")
    if os.path.exists(history_path):
        try:
            df_hist = pd.read_csv(history_path)
            if not df_hist.empty and 'Churn' in df_hist.columns:
                required_cols = [
                    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                    'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
                    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
                    'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
                    'MonthlyCharges', 'TotalCharges', 'Churn'
                ]
                common_cols = [c for c in required_cols if c in df_cleaned.columns and c in df_hist.columns]
                if len(common_cols) >= 10:
                    df_cleaned = pd.concat([df_cleaned, df_hist[common_cols]], ignore_index=True)
                    df_cleaned = df_cleaned.drop_duplicates()
                    logger.info(f"Integrated history logs into training dataset. Total rows: {len(df_cleaned)}")
                else:
                    logger.warning(f"Skipping history merge: only {len(common_cols)} required common columns found (need >= 10).")
        except Exception as e:
            logger.warning(f"Could not merge history logs: {e}")
            
    # Save updated clean dataset
    save_processed_data(df_cleaned, processed_path)
    
    # 3. Preprocess & Encode
    X, y, binary_mappings, feature_names = preprocess_and_encode(df_cleaned)
    
    # 4. Train Test Split & Scale
    X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y)
    
    # 5. Train & Benchmark Models
    results, trained_models = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # 6. Select Best Model by ROC-AUC
    results_df = pd.DataFrame(results).T
    best_model_name = results_df["ROC-AUC"].idxmax()
    best_model = trained_models[best_model_name]
    best_metrics = results[best_model_name]
    
    logger.info(f"Top performing model identified: {best_model_name}")
    logger.info(f"ROC-AUC: {best_metrics['ROC-AUC']:.4f} | F1-Score: {best_metrics['F1-Score']:.4f}")
    
    # 7. Save Serialized Artifacts
    joblib.dump(best_model, os.path.join(model_dir, "model.pkl"))
    joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))
    joblib.dump(feature_names, os.path.join(model_dir, "feature_names.pkl"))
    joblib.dump(binary_mappings, os.path.join(model_dir, "label_encoder.pkl"))
    
    metrics_path = os.path.join(model_dir, "metrics.json")
    import json
    metrics_payload = {
        "best_model_name": best_model_name,
        "metrics": best_metrics,
        "dataset_size": len(df_cleaned),
        "training_timestamp": pd.Timestamp.now().isoformat()
    }
    with open(metrics_path, "w") as f:
        json.dump(metrics_payload, f, indent=2)
    logger.info("Saved updated model pipeline artifacts to models/")
    
    # 8. Clear Streamlit cache if running in Streamlit
    try:
        import streamlit as st
        st.cache_resource.clear()
        st.cache_data.clear()
        logger.info("Cleared Streamlit pipeline resource caches.")
    except Exception:
        pass
        
    return {
        'best_model_name': best_model_name,
        'metrics': best_metrics,
        'all_results': results,
        'dataset_size': len(df_cleaned)
    }

if __name__ == "__main__":
    summary = run_retraining_pipeline()
    print("\n=== Retraining Summary ===")
    print(f"Best Model: {summary['best_model_name']}")
    print(f"Dataset Size: {summary['dataset_size']} rows")
    print(f"ROC-AUC: {summary['metrics']['ROC-AUC']:.4f}")
    print(f"F1-Score: {summary['metrics']['F1-Score']:.4f}")
