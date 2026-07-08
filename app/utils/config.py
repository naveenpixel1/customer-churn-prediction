import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / 'models'
DATA_DIR = BASE_DIR / 'data'
REPORTS_DIR = BASE_DIR / 'reports'
EVAL_DIR = REPORTS_DIR / 'evaluation'
FIGURES_DIR = REPORTS_DIR / 'figures'
HISTORY_FILE = DATA_DIR / 'history.csv'
CLEANED_DATA_PATH = DATA_DIR / 'processed' / 'churn_cleaned.csv'
RAW_DATA_PATH = DATA_DIR / 'raw' / 'WA_Fn-UseC_-Telco-Customer-Churn.csv'

MODEL_METRICS = {
    'Accuracy': 0.8062,
    'Precision': 0.6593,
    'Recall': 0.5588,
    'F1-Score': 0.6049,
    'ROC-AUC': 0.8422
}

DEMOGRAPHIC_FEATURES = ['gender', 'SeniorCitizen', 'Partner', 'Dependents']
FINANCIAL_FEATURES = ['tenure', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']
SERVICE_FEATURES = [
    'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'
]

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
if CLEANED_DATA_PATH.parent:
    os.makedirs(CLEANED_DATA_PATH.parent, exist_ok=True)

PORTFOLIO_TITLE = '📊 Customer Churn Prediction Dashboard'
PORTFOLIO_SUBTITLE = (
    'An End-to-End Machine Learning Project for Predicting Customer Churn using '
    'Customer Demographics, Account Information, and Service Usage Patterns.'
)
DEVELOPER_NAME = 'Naveen Kumar .D'
PROJECT_TYPE = 'Machine Learning Portfolio Project'
MODEL_STATUS = 'Ready'
