import os
import urllib.request

# URL of the dataset
DATA_URL = "https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv"
SAVE_DIR = os.path.join("data", "raw")
SAVE_PATH = os.path.join(SAVE_DIR, "WA_Fn-UseC_-Telco-Customer-Churn.csv")

def download_dataset():
    """Downloads the Telco Customer Churn dataset if it doesn't already exist."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR, exist_ok=True)
        print(f"Created directory: {SAVE_DIR}")
        
    if os.path.exists(SAVE_PATH):
        print(f"Dataset already exists at: {SAVE_PATH}")
        return

    print(f"Downloading dataset from:\n{DATA_URL}")
    try:
        urllib.request.urlretrieve(DATA_URL, SAVE_PATH)
        print(f"Successfully downloaded and saved to: {SAVE_PATH}")
    except Exception as e:
        print(f"Error downloading the dataset: {e}")
        raise e

if __name__ == "__main__":
    download_dataset()
