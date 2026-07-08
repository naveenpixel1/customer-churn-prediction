import os
import sys
import pytest

# Ensure project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.prediction_service import PredictionService

@pytest.fixture
def predictor():
    try:
        return PredictionService()
    except Exception as e:
        pytest.skip(f"Model pipeline files not available: {e}")

def test_inference_runs_successfully(predictor):
    # Arrange
    sample_input = {
        'gender': 'Female',
        'SeniorCitizen': 0,
        'Partner': 'Yes',
        'Dependents': 'Yes',
        'tenure': 24,
        'PhoneService': 'Yes',
        'MultipleLines': 'Yes',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'Yes',
        'TechSupport': 'No',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 95.0,
        'TotalCharges': 2280.0
    }
    
    # Act
    result = predictor.predict(sample_input)
    
    # Assert
    assert 'prediction' in result
    assert result['prediction'] in [0, 1]
    
    assert 'probability' in result
    assert 0.0 <= result['probability'] <= 1.0
    
    assert 'risk_level' in result
    assert result['risk_level'] in ['Low', 'Medium', 'High', 'Critical']
    
    assert 'confidence' in result
    assert result['confidence'] in ['Low', 'Moderate', 'High']
    
    assert 'contributions' in result
    assert isinstance(result['contributions'], dict)

def test_inference_handles_new_customers(predictor):
    # Arrange
    new_customer = {
        'gender': 'Male',
        'SeniorCitizen': 0,
        'Partner': 'Yes',
        'Dependents': 'Yes',
        'tenure': 0,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'Yes',
        'TechSupport': 'Yes',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Two year',
        'PaperlessBilling': 'No',
        'PaymentMethod': 'Credit card (automatic)',
        'MonthlyCharges': 20.0,
        'TotalCharges': 0.0
    }
    
    # Act
    result = predictor.predict(new_customer)
    
    # Assert
    assert result['risk_level'] == 'Low' # new customer with low-risk features should be low risk
    assert result['prediction'] == 0
