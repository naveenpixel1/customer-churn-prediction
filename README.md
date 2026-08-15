# 📊 End-to-End Customer Churn Prediction & MLOps System

A professional Machine Learning & MLOps portfolio project designed to predict customer churn in the telecommunications industry, engineer interaction features, tune tree ensembles via `GridSearchCV`, calculate Customer Lifetime Value (CLV), evaluate risk factors, and deploy an interactive multi-page web application containerized with Docker.

---

## 📋 Table of Contents
- [Project Overview & Problem Statement](#project-overview--problem-statement)
- [System Architecture](#system-architecture)
- [Dataset Profile](#dataset-profile)
- [Feature Engineering & Preprocessing](#feature-engineering--preprocessing)
- [Machine Learning & Hyperparameter Tuning](#machine-learning--hyperparameter-tuning)
- [Model Comparison & Results](#model-comparison--results)
- [Streamlit Multi-Page Web Application](#streamlit-multi-page-web-application)
- [MLOps Containerization & How to Run](#mlops-containerization--how-to-run)
- [License & Author](#license--author)

---

## 📋 Project Overview & Problem Statement
Customer churn (attrition) occurs when customers cancel their subscriptions or stop doing business with a firm. In the telecommunications sector, acquiring a new customer is **5 to 25 times higher** than retaining an existing one.

This project implements a complete, production-grade Machine Learning pipeline that:
1. Programmatically retrieves and cleans historical Telco billing records.
2. Conducts Feature Engineering (`Tenure_To_Monthly_Ratio`, `TotalCharges_Per_Month`, `Service_Count`, `Has_Anchor_Service`).
3. Trains and benchmarks classification models (`Logistic Regression`, `Decision Trees`, `Random Forest`, `XGBoost`) using `GridSearchCV` hyperparameter tuning and class imbalance handling.
4. Generates instance-level explanations, ROC-AUC, Precision-Recall trade-off curves, and Confusion matrices.
5. Deploys the best classifier as an interactive Streamlit web dashboard complete with KPI sparkline trend graphs.
6. Calculates Customer Lifetime Value (CLV) and prioritizes at-risk accounts into actionable intervention tiers.
7. Containerizes the application stack using Docker and Docker Compose for production deployment.

---

## 🏗️ System Architecture

```text
               +----------------------------------+
               |  IBM Watson Telco Churn Dataset  |
               +----------------------------------+
                                |
                                v
               +----------------------------------+
               |  Feature Engineering & Cleaning  |
               |  (preprocess.py / Scaling / Dummies) |
               +----------------------------------+
                                |
                                v
               +----------------------------------+
               |  GridSearchCV Model Optimization |
               |  (Logistic, Tree, Forest, XGBoost) |
               +----------------------------------+
                                |
                                v
               +----------------------------------+
               |  Model Artifact Serialization    |
               |  (models/model.pkl & scaler.pkl) |
               +----------------------------------+
                                |
                                v
               +----------------------------------+
               | Streamlit Application & Docker   |
               | (Port 8501 / Multi-Page Dashboard)|
               +----------------------------------+
```

---

## 🏷️ Dataset Profile
The system utilizes the classic **IBM Watson Telco Customer Churn dataset** (7,043 rows, 21 original columns, 24 engineered features) containing:
* **Demographics**: Gender, Senior Citizen status, Partners, and Dependents.
* **Services**: Phone service, multiple lines, internet provider type, security, backups, device protection, streaming TV, and streaming movies.
* **Account Info**: Tenure (months active), contract type (month-to-month, annual, two-year), payment method, monthly charges, and total charges.

---

## ⚙️ Feature Engineering & Preprocessing

### 1. Data Cleaning
- Handled empty string spaces in `TotalCharges` (coerced type conversion to float, introducing 11 NaNs).
- Imputed those 11 NaNs to `0.0` as they represented new customers with `tenure = 0` (who haven't been billed yet).
- Dropped unique identifiers (`customerID`) to prevent overfitting.

### 2. Derived Interaction Features
- **`Tenure_To_Monthly_Ratio`**: `tenure / (MonthlyCharges + 1e-5)` to quantify customer loyalty per unit price.
- **`TotalCharges_Per_Month`**: `TotalCharges / (tenure + 1.0)` capturing historical billing velocity.
- **`Service_Count`**: Sum of active add-on features (`OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`).
- **`Has_Anchor_Service`**: Binary flag indicating active `OnlineSecurity` or `TechSupport`.

---

## 📊 Model Comparison & Results

During stratified 80/20 test-set validation with `GridSearchCV` hyperparameter tuning, the benchmarked classifiers yielded:

| Model Name | Best Hyperparameters | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | `C=10.0, class_weight='balanced'` | **80.62%** | 65.93% | **55.88%** | **61.75%** | **0.8457** |
| **XGBoost** | `n_estimators=100, max_depth=3, lr=0.05` | 80.41% | **66.20%** | 53.21% | 59.00% | 0.8441 |
| **Random Forest** | `n_estimators=150, max_depth=8` | 80.34% | 66.44% | 52.41% | 58.59% | 0.8410 |
| **Decision Tree** | `max_depth=6, min_samples_split=5` | 80.06% | 66.67% | 49.73% | 56.97% | 0.8219 |

---

## 🖥️ Streamlit Multi-Page Web Application
The deployed interface provides:
* **🏠 Home**: Overview, project scopes, technical specifications, and KPI sparkline trend graphs.
* **🔮 Churn Predictor**: Step-by-step wizard forms, input validation rules, probability scoring, CLV calculation, Priority Action Tiers, and Plotly driver charts.
* **📊 Analytics**: Dynamic cohort segmentations, distribution histograms, contract ratio comparisons, billing boxplots, payment methods, and variable correlation heatmaps.
* **📈 Model Performance**: Interactive cohort-segmented confusion matrix heatmaps, ROC curves, Precision-Recall trade-off plots, and Feature Importances.
* **💡 Business Insights**: Strategic action playbooks and revenue risk migration strategies.
* **🔐 Admin Console**: Log administration command console.

---

## 🐳 MLOps Containerization & How to Run

### Option 1: Run via Docker Compose (Recommended)
```bash
docker compose up --build
```
Access the application in your browser at `http://localhost:8501`.

### Option 2: Run via Docker CLI
```bash
docker build -t customer-churn-app .
docker run -p 8501:8501 customer-churn-app
```

### Option 3: Local Virtual Environment
```bash
# 1. Clone repo & setup virtual environment
git clone https://github.com/naveenpixel1/customer-churn-prediction.git
cd customer-churn-prediction
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute retraining pipeline (Optional)
python src/retrain_pipeline.py

# 4. Run test suite
pytest

# 5. Launch Streamlit dashboard
streamlit run app/main.py
```

---

## 👨‍💻 Author & License
* **Developer**: **Naveen Kumar .D**
* **Year**: 2026
* **License**: MIT License
