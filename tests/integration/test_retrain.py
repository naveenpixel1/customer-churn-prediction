import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from src.retrain_pipeline import run_retraining_pipeline

@pytest.mark.slow
def test_retrain_pipeline_runs():
    summary = run_retraining_pipeline()
    assert 'best_model_name' in summary
    assert summary['best_model_name'] in ['Logistic Regression', 'Decision Tree', 'Random Forest', 'XGBoost']
    assert 'metrics' in summary
    assert 'ROC-AUC' in summary['metrics']
    assert summary['metrics']['ROC-AUC'] > 0.5
