import os
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from app.utils.config import HISTORY_FILE

class HistoryService:

    @staticmethod
    def initialize_history_file() -> None:
        if not os.path.exists(HISTORY_FILE):
            if HISTORY_FILE.parent:
                os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
            columns = [
                'timestamp', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 
                'tenure', 'PhoneService', 'MultipleLines', 'InternetService', 
                'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 
                'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 
                'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'prediction', 
                'probability', 'risk_level'
            ]
            df = pd.DataFrame(columns=columns)
            df.to_csv(HISTORY_FILE, index=False)

    def __init__(self):
        self.initialize_history_file()

    def append_record(self, input_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'gender': input_data.get('gender'),
            'SeniorCitizen': int(input_data.get('SeniorCitizen', 0)),
            'Partner': input_data.get('Partner'),
            'Dependents': input_data.get('Dependents'),
            'tenure': int(input_data.get('tenure', 0)),
            'PhoneService': input_data.get('PhoneService'),
            'MultipleLines': input_data.get('MultipleLines'),
            'InternetService': input_data.get('InternetService'),
            'OnlineSecurity': input_data.get('OnlineSecurity'),
            'OnlineBackup': input_data.get('OnlineBackup'),
            'DeviceProtection': input_data.get('DeviceProtection'),
            'TechSupport': input_data.get('TechSupport'),
            'StreamingTV': input_data.get('StreamingTV'),
            'StreamingMovies': input_data.get('StreamingMovies'),
            'Contract': input_data.get('Contract'),
            'PaperlessBilling': input_data.get('PaperlessBilling'),
            'PaymentMethod': input_data.get('PaymentMethod'),
            'MonthlyCharges': float(input_data.get('MonthlyCharges', 0.0)),
            'TotalCharges': float(input_data.get('TotalCharges', 0.0)),
            'prediction': int(result.get('prediction', 0)),
            'probability': float(result.get('probability', 0.0)),
            'risk_level': result.get('risk_level', 'Low')
        }
        df_new = pd.DataFrame([record])
        df_new.to_csv(HISTORY_FILE, mode='a', header=False, index=False)

    def load_history(self) -> pd.DataFrame:
        if not os.path.exists(HISTORY_FILE):
            self.initialize_history_file()
        try:
            df = pd.read_csv(HISTORY_FILE)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values(by='timestamp', ascending=False)
            return df
        except Exception:
            self.initialize_history_file()
            return pd.read_csv(HISTORY_FILE)

    def delete_record(self, timestamp_str: str) -> bool:
        df = self.load_history()
        if df.empty:
            return False
        df_filtered = df[df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S') != timestamp_str]
        if len(df_filtered) < len(df):
            df_filtered.to_csv(HISTORY_FILE, index=False)
            return True
        return False

    def clear_all(self) -> None:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        self.initialize_history_file()
