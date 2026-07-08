import os
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Any, Optional
from app.utils.config import CLEANED_DATA_PATH

class AnalyticsService:

    @staticmethod
    @st.cache_data
    def load_dataset() -> pd.DataFrame:
        if not os.path.exists(CLEANED_DATA_PATH):
            raise FileNotFoundError(f"Cleaned dataset not found at: {CLEANED_DATA_PATH}. Run preprocessing first.")
        df = pd.read_csv(CLEANED_DATA_PATH)
        
        # If Churn is represented numerically, map it back to Yes/No for visual displays
        if 'Churn' in df.columns:
            if df['Churn'].dtype in [np.int64, np.int32, float]:
                df['Churn'] = df['Churn'].map({1: 'Yes', 0: 'No'})
        return df

    def __init__(self):
        self.df = self.load_dataset()

    def get_summary_stats(self, filtered_df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        data = filtered_df if filtered_df is not None else self.df
        if data.empty:
            return {
                'total_customers': 0,
                'churn_rate': 0.0,
                'avg_tenure': 0.0,
                'avg_monthly_charges': 0.0,
                'total_monthly_revenue': 0.0
            }
        
        total_customers = len(data)
        
        if 'Churn' in data.columns:
            churn_count = len(data[data['Churn'] == 'Yes'])
        else:
            churn_count = 0
            
        churn_rate = churn_count / total_customers if total_customers > 0 else 0.0
        avg_tenure = float(data['tenure'].mean())
        avg_monthly = float(data['MonthlyCharges'].mean())
        total_monthly_rev = float(data['MonthlyCharges'].sum())
        
        return {
            'total_customers': total_customers,
            'churn_rate': churn_rate,
            'avg_tenure': avg_tenure,
            'avg_monthly_charges': avg_monthly,
            'total_monthly_revenue': total_monthly_rev
        }

    def filter_data(self, contract_types: Optional[list] = None, internet_services: Optional[list] = None, senior_citizen: Optional[str] = None) -> pd.DataFrame:
        filtered_df = self.df.copy()
        if contract_types:
            filtered_df = filtered_df[filtered_df['Contract'].isin(contract_types)]
        if internet_services:
            filtered_df = filtered_df[filtered_df['InternetService'].isin(internet_services)]
        if senior_citizen:
            if senior_citizen == 'Senior Citizen Only':
                filtered_df = filtered_df[filtered_df['SeniorCitizen'] == 1]
            elif senior_citizen == 'Non-Senior Only':
                filtered_df = filtered_df[filtered_df['SeniorCitizen'] == 0]
        return filtered_df
