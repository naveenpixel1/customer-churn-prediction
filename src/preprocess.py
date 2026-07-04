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
    1. Inspects shape and data types.
    2. Identifies and removes duplicate rows.
    3. Identifies missing values.
    4. Fixes incorrect data types (TotalCharges).
    5. Imputes missing TotalCharges values (new customers with tenure=0 -> TotalCharges=0).
    6. Drops irrelevant identifiers (customerID).
    """
    print("\n--- Starting Data Cleaning Phase ---")
    print(f"Original shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 1. Check for Duplicate Rows
    duplicates = df.duplicated().sum()
    print(f"Duplicate rows detected: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"Removed {duplicates} duplicate rows. New shape: {df.shape}")
    
    # 2. Check for Initial Missing Values
    null_counts = df.isnull().sum().sum()
    print(f"Initial missing values (before parsing types): {null_counts}")

    # 3. Fix Incorrect Data Types (TotalCharges)
    # TotalCharges is loaded as an object (string) because of empty strings (" ").
    # We use pd.to_numeric with errors='coerce' to turn empty strings into NaN.
    print("\nCasting 'TotalCharges' column to float numeric type...")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # 4. Handle Missing Values
    # Check how many NaNs were introduced in TotalCharges
    total_charges_nans = df['TotalCharges'].isnull().sum()
    print(f"Missing values found in 'TotalCharges' after coercion: {total_charges_nans}")
    
    if total_charges_nans > 0:
        # Check if the missing values correspond to customers with tenure = 0
        zero_tenure_customers = df[df['tenure'] == 0]
        print(f"Customers with 0 tenure: {len(zero_tenure_customers)}")
        
        # Impute missing TotalCharges with 0.0
        df['TotalCharges'] = df['TotalCharges'].fillna(0.0)
        print("Imputed missing 'TotalCharges' with 0.0 for new customers (tenure = 0).")

    # 5. Double check for any other missing values
    remaining_nans = df.isnull().sum().sum()
    print(f"Remaining missing values in dataset: {remaining_nans}")

    # 6. Drop customerID
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])
        print("Dropped 'customerID' column as it has no predictive power.")

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
