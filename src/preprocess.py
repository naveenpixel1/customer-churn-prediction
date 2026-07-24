import os
import pandas as pd
import numpy as np

def load_data(file_path: str) -> pd.DataFrame:
    """Loads the CSV dataset into a Pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at: {file_path}")
    print(f"Loading dataset from: {file_path}")
    df = pd.read_csv(file_path)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Telco Churn DataFrame:
    1. Trims whitespace from all string/object columns.
    2. Identifies and removes duplicate rows.
    3. Handles TotalCharges numerical parsing and conditional imputation:
       - tenure == 0 -> TotalCharges = 0.0
       - tenure > 0 -> TotalCharges = tenure * MonthlyCharges if available, else median.
    4. Handles any remaining missing values in numeric (median) or categorical (mode) columns.
    5. Drops unique identifier column (customerID).
    """
    df = df.copy()
    print("\n--- Starting Hardened Data Cleaning Phase ---")
    print(f"Original shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 1. Trim string whitespace across object columns
    object_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in object_cols:
        df[col] = df[col].astype(str).str.strip()
        
    # 2. Check for Duplicate Rows
    duplicates = df.duplicated().sum()
    print(f"Duplicate rows detected: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"Removed {duplicates} duplicate rows. New shape: {df.shape}")
        
    # 3. Handle TotalCharges numeric coercion and conditional imputation
    if 'TotalCharges' in df.columns:
        print("\nCasting 'TotalCharges' column to float numeric type...")
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        
        tc_nans = df['TotalCharges'].isnull()
        if tc_nans.sum() > 0:
            print(f"Coerced {tc_nans.sum()} missing values in 'TotalCharges'.")
            
            # Impute tenure == 0 with 0.0
            zero_tenure_mask = tc_nans & (df['tenure'] == 0)
            if zero_tenure_mask.sum() > 0:
                df.loc[zero_tenure_mask, 'TotalCharges'] = 0.0
                print(f"Imputed {zero_tenure_mask.sum()} 'TotalCharges' missing values with 0.0 for new customers (tenure = 0).")
            
            # Impute tenure > 0 with tenure * MonthlyCharges
            pos_tenure_mask = tc_nans & (df['tenure'] > 0)
            if pos_tenure_mask.sum() > 0:
                if 'MonthlyCharges' in df.columns:
                    df.loc[pos_tenure_mask, 'TotalCharges'] = df.loc[pos_tenure_mask, 'tenure'] * df.loc[pos_tenure_mask, 'MonthlyCharges']
                else:
                    median_tc = df['TotalCharges'].median()
                    df.loc[pos_tenure_mask, 'TotalCharges'] = median_tc
                print(f"Imputed {pos_tenure_mask.sum()} 'TotalCharges' missing values for active customers (tenure > 0).")

    # 4. General Missing Value Imputation Fallback
    num_cols = df.select_dtypes(include=['number']).columns
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            med_val = df[col].median()
            df[col] = df[col].fillna(med_val)
            print(f"Imputed missing values in numeric column '{col}' with median: {med_val}")

    cat_cols = df.select_dtypes(include=['object', 'category', 'string']).columns

    for col in cat_cols:
        if col != 'customerID' and df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Missing'
            df[col] = df[col].fillna(mode_val)
            print(f"Imputed missing values in categorical column '{col}' with mode: {mode_val}")

    # 5. Drop customerID
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])
        print("Dropped 'customerID' column as it has no predictive power.")

    remaining_nans = df.isnull().sum().sum()
    print(f"Remaining missing values in dataset: {remaining_nans}")
    print("--- Data Cleaning Complete ---")
    print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """Saves the cleaned DataFrame to the processed directory."""
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"\nSuccessfully saved cleaned dataset to: {output_path}")

def main() -> None:
    raw_path = os.path.join("data", "raw", "WA_Fn-UseC_-Telco-Customer-Churn.csv")
    processed_path = os.path.join("data", "processed", "churn_cleaned.csv")
    
    # Run pipeline
    df = load_data(raw_path)
    df_cleaned = clean_data(df)
    save_processed_data(df_cleaned, processed_path)

if __name__ == "__main__":
    main()
