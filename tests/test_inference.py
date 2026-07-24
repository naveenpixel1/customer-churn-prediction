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

def test_inference_custom_threshold(predictor):
    import numpy as np
    sample_input = {
        'gender': 'Female',
        'SeniorCitizen': 0,
        'Partner': 'No',
        'Dependents': 'No',
        'tenure': 6,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 70.0,
        'TotalCharges': 420.0
    }
    res_default = predictor.predict(sample_input, threshold=0.50)
    res_low = predictor.predict(sample_input, threshold=0.10)
    
    assert res_default['threshold'] == 0.50
    assert res_low['threshold'] == 0.10
    assert res_low['prediction'] == 1

def test_evaluate_threshold_metrics():
    import numpy as np
    y_true = np.array([1, 0, 1, 0, 1, 0, 0, 1])
    y_prob = np.array([0.8, 0.2, 0.4, 0.1, 0.9, 0.35, 0.6, 0.7])
    
    metrics = PredictionService.evaluate_threshold_metrics(y_true, y_prob, threshold=0.35)
    
    assert metrics['threshold'] == 0.35
    assert 'accuracy' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert 'f1_score' in metrics
    assert metrics['tp'] == 4

def test_explain_customer_prediction(predictor):
    sample_input = {
        'gender': 'Female',
        'SeniorCitizen': 0,
        'Partner': 'No',
        'Dependents': 'No',
        'tenure': 2,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 90.0,
        'TotalCharges': 180.0
    }
    res = predictor.predict(sample_input)
    assert 'explanation' in res
    exp = res['explanation']
    
    assert 'top_risk_drivers' in exp
    assert 'top_mitigating_drivers' in exp
    assert isinstance(exp['top_risk_drivers'], list)
    assert isinstance(exp['top_mitigating_drivers'], list)
    
    if exp['top_risk_drivers']:
        first_risk = exp['top_risk_drivers'][0]
        assert 'label' in first_risk
        assert 'prob_impact_pct' in first_risk
        assert first_risk['prob_impact_pct'] > 0

def test_simulate_retention_impact(predictor):
    base_customer = {
        'gender': 'Female',
        'SeniorCitizen': 0,
        'Partner': 'No',
        'Dependents': 'No',
        'tenure': 4,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 95.0,
        'TotalCharges': 380.0
    }
    
    mods = {
        'Contract': 'Two year',
        'TechSupport': 'Yes',
        'OnlineSecurity': 'Yes',
        'MonthlyDiscount': 15.0
    }
    
    sim_res = predictor.simulate_retention_impact(base_customer, mods, threshold=0.35)
    
    assert 'original_prob' in sim_res
    assert 'simulated_prob' in sim_res
    assert 'risk_reduction_pct' in sim_res
    assert sim_res['simulated_prob'] < sim_res['original_prob']
    assert sim_res['risk_reduction_pct'] > 0



