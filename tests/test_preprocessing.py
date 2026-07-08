import os
import sys
import pandas as pd
import numpy as np

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocess import clean_data

def test_clean_data_drops_duplicates():
    # Arrange
    data = {
        'customerID': ['1', '1', '2'],
        'gender': ['Male', 'Male', 'Female'],
        'SeniorCitizen': [0, 0, 1],
        'Partner': ['Yes', 'Yes', 'No'],
        'Dependents': ['No', 'No', 'Yes'],
        'tenure': [12, 12, 24],
        'PhoneService': ['Yes', 'Yes', 'No'],
        'MultipleLines': ['No', 'No', 'No phone service'],
        'InternetService': ['DSL', 'DSL', 'No'],
        'OnlineSecurity': ['Yes', 'Yes', 'No internet service'],
        'OnlineBackup': ['No', 'No', 'No internet service'],
        'DeviceProtection': ['No', 'No', 'No internet service'],
        'TechSupport': ['Yes', 'Yes', 'No internet service'],
        'StreamingTV': ['No', 'No', 'No internet service'],
        'StreamingMovies': ['No', 'No', 'No internet service'],
        'Contract': ['Month-to-month', 'Month-to-month', 'Two year'],
        'PaperlessBilling': ['Yes', 'Yes', 'No'],
        'PaymentMethod': ['Mailed check', 'Mailed check', 'Bank transfer (automatic)'],
        'MonthlyCharges': [45.80, 45.80, 20.05],
        'TotalCharges': ['550.0', '550.0', '480.2']
    }
    df = pd.DataFrame(data)
    
    # Act
    df_cleaned = clean_data(df)
    
    # Assert
    # Duplicate rows should be dropped (row 1 is identical to row 0)
    # Plus, customerID column should be dropped
    assert df_cleaned.shape[0] == 2
    assert 'customerID' not in df_cleaned.columns

def test_clean_data_imputes_missing_total_charges():
    # Arrange
    data = {
        'customerID': ['3', '4'],
        'gender': ['Male', 'Female'],
        'SeniorCitizen': [0, 0],
        'Partner': ['No', 'Yes'],
        'Dependents': ['No', 'No'],
        'tenure': [0, 5], # New customer vs regular customer
        'PhoneService': ['Yes', 'Yes'],
        'MultipleLines': ['No', 'Yes'],
        'InternetService': ['DSL', 'Fiber optic'],
        'OnlineSecurity': ['No', 'Yes'],
        'OnlineBackup': ['No', 'No'],
        'DeviceProtection': ['No', 'Yes'],
        'TechSupport': ['No', 'No'],
        'StreamingTV': ['No', 'Yes'],
        'StreamingMovies': ['No', 'Yes'],
        'Contract': ['Month-to-month', 'One year'],
        'PaperlessBilling': ['No', 'Yes'],
        'PaymentMethod': ['Mailed check', 'Electronic check'],
        'MonthlyCharges': [20.00, 95.50],
        'TotalCharges': [' ', '477.5'] # Empty string for tenure=0
    }
    df = pd.DataFrame(data)
    
    # Act
    df_cleaned = clean_data(df)
    
    # Assert
    # TotalCharges empty space for tenure=0 should become 0.0
    assert df_cleaned['TotalCharges'].iloc[0] == 0.0
    assert df_cleaned['TotalCharges'].iloc[1] == 477.5
    assert df_cleaned['TotalCharges'].dtype == float
