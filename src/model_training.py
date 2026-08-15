import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def load_cleaned_data(file_path):
    """Loads the preprocessed dataset."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cleaned dataset not found at: {file_path}")
    return pd.read_csv(file_path)

def preprocess_and_encode(df):
    """
    Applies Label Encoding to binary variables, One-Hot Encoding to multi-class variables,
    and returns features X, target y, and information needed for deployment.
    """
    df_encoded = df.copy()
    
    # 1. Define binary columns to map to 0 and 1
    binary_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    
    # Binary mappings
    binary_mappings = {}
    for col in binary_cols:
        # Save mapping for deployment
        unique_vals = sorted(df_encoded[col].unique()) # e.g. ['Female', 'Male'] or ['No', 'Yes']
        mapping = {val: i for i, val in enumerate(unique_vals)}
        binary_mappings[col] = mapping
        df_encoded[col] = df_encoded[col].map(mapping)
        print(f"Mapped binary column '{col}': {mapping}")
        
    # Map target variable Churn (Yes: 1, No: 0)
    df_encoded['Churn'] = df_encoded['Churn'].map({'Yes': 1, 'No': 0})
    
    # 2. Identify remaining multi-class categorical columns for One-Hot Encoding
    categorical_cols = df_encoded.select_dtypes(include=['object', 'string']).columns.tolist()

    print(f"\nMulti-class columns for One-Hot Encoding: {categorical_cols}")
    
    # Apply One-Hot Encoding (drop_first=True to avoid multi-collinearity)
    df_encoded = pd.get_dummies(df_encoded, columns=categorical_cols, drop_first=True)
    
    # Separate features X and target y
    X = df_encoded.drop(columns=['Churn'])
    y = df_encoded['Churn']
    
    return X, y, binary_mappings, X.columns.tolist()

def split_and_scale(X, y):
    """Splits data 80/20 and standardizes continuous features to avoid data leakage."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scaler should only be fit on training set to avoid data leakage
    scaler = StandardScaler()
    
    # Continuous numerical features including derived interaction features
    potential_num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Tenure_To_Monthly_Ratio', 'TotalCharges_Per_Month', 'Service_Count']
    num_cols = [c for c in potential_num_cols if c in X.columns]
    
    # Scale training numerical cols
    X_train_scaled = X_train.copy()
    X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
    
    # Scale testing numerical cols (transform only!)
    X_test_scaled = X_test.copy()
    X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])
    
    # Convert dummy columns to integer 0/1 instead of bool (ensures model compatibility)
    X_train_scaled = X_train_scaled.astype(float)
    X_test_scaled = X_test_scaled.astype(float)
    
    print(f"\nTrain set shape: {X_train_scaled.shape}")
    print(f"Test set shape: {X_test_scaled.shape}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

from sklearn.model_selection import GridSearchCV
import xgboost as xgb

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Trains and hyperparameter tunes Logistic Regression, Decision Tree, Random Forest, and XGBoost via GridSearchCV."""
    neg_pos_ratio = float((len(y_train) - sum(y_train)) / sum(y_train)) if sum(y_train) > 0 else 1.0
    
    model_grids = {
        "Logistic Regression": (
            LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
            {'C': [0.1, 1.0, 10.0]}
        ),
        "Decision Tree": (
            DecisionTreeClassifier(class_weight='balanced', random_state=42),
            {'max_depth': [4, 6, 8], 'min_samples_split': [2, 5]}
        ),
        "Random Forest": (
            RandomForestClassifier(class_weight='balanced', random_state=42),
            {'n_estimators': [100, 150], 'max_depth': [8, 12], 'min_samples_split': [2, 5]}
        ),
        "XGBoost": (
            xgb.XGBClassifier(scale_pos_weight=neg_pos_ratio, eval_metric='logloss', random_state=42),
            {'n_estimators': [100, 150], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]}
        )
    }
    
    results = {}
    trained_models = {}
    
    print("\n--- Training & Hyperparameter Tuning via GridSearchCV ---")
    for name, (base_model, param_grid) in model_grids.items():
        print(f"Optimizing {name} with GridSearchCV...")
        grid = GridSearchCV(base_model, param_grid, cv=3, scoring='roc_auc', n_jobs=-1)
        grid.fit(X_train, y_train)
        
        best_clf = grid.best_estimator_
        trained_models[name] = best_clf
        print(f"  Best params for {name}: {grid.best_params_}")
        
        # Predictions
        y_pred = best_clf.predict(X_test)
        y_prob = best_clf.predict_proba(X_test)[:, 1]
        
        # Compute metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_prob)
        
        results[name] = {
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1-Score": f1,
            "ROC-AUC": roc_auc
        }
        
    return results, trained_models


def main():
    processed_path = os.path.join("data", "processed", "churn_cleaned.csv")
    df = load_cleaned_data(processed_path)
    
    # Preprocess & Encode
    X, y, binary_mappings, feature_names = preprocess_and_encode(df)
    
    # Train Test Split & Scaling
    X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y)
    
    # Model comparisons
    results, trained_models = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # Print results table
    results_df = pd.DataFrame(results).T
    print("\n=== Model Comparison Table ===")
    print(results_df.round(4))
    
    # Determine the best model (using F1-Score or ROC-AUC, as they are better for imbalanced datasets)
    # Let's use ROC-AUC as the primary comparison metric
    best_model_name = results_df["ROC-AUC"].idxmax()
    best_model = trained_models[best_model_name]
    best_model_metrics = results[best_model_name]
    
    print(f"\nBest Model identified based on ROC-AUC: {best_model_name}")
    print(f"ROC-AUC: {best_model_metrics['ROC-AUC']:.4f} | F1-Score: {best_model_metrics['F1-Score']:.4f}")
    
    # Save separate components using joblib with .pkl extension
    joblib.dump(best_model, os.path.join(MODEL_DIR, "model.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(feature_names, os.path.join(MODEL_DIR, "feature_names.pkl"))
    joblib.dump(binary_mappings, os.path.join(MODEL_DIR, "label_encoder.pkl"))
    
    print("\nSaved separate pipeline components to models/:")
    print(" - model.pkl (Best Model)")
    print(" - scaler.pkl (Standard Scaler)")
    print(" - feature_names.pkl (One-hot encoded column layout)")
    print(" - label_encoder.pkl (Binary label mappings)")

if __name__ == "__main__":
    main()
