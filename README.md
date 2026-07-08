# 📊 End-to-End Customer Churn Prediction System

A professional Machine Learning portfolio project designed to predict customer churn in the telecommunications industry, evaluate risk factors, and recommend business countermeasures in real time.

---

## 📋 Table of Contents
- [Project Overview & Problem Statement](#project-overview--problem-statement)
- [Business Impact Analysis](#business-impact-analysis)
- [Dataset Profile](#dataset-profile)
- [Project Architecture & Directory Structure](#project-architecture--directory-structure)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Model Comparison & Results](#model-comparison--results)
- [Streamlit Multi-Page Web Application](#streamlit-multi-page-web-application)
- [Installation & How to Run](#installation--how-to-run)
- [Future Enhancements](#future-enhancements)
- [License & Authors](#license--authors)

---

## 📋 Project Overview & Problem Statement
Customer churn (attrition) occurs when customers cancel their subscriptions or stop doing business with a firm. In the highly competitive telecommunications sector, the cost of acquiring a new customer is **5 to 25 times higher** than retaining an existing one.

This project implements a complete, production-grade Machine Learning pipeline that:
1. Programmatically retrieves and cleans historical billing records.
2. Conducts Exploratory Data Analysis (EDA) to map key churn indicators.
3. Trains and benchmarks classification models (`Logistic Regression`, `Decision Trees`, `Random Forests`).
4. Generates diagnostics (Confusion Matrix, ROC Curve, Precision-Recall Curve).
5. Deploys the best classifier as an interactive Streamlit multi-page web dashboard.
6. Integrates query logging, diagnostic reports, and isolated pytest assertions.

---

## 📈 Business Impact Analysis
To showcase the financial value of this AI system to stakeholders, we model a standard telecommunications operator with a base of **10,000 customers**:

* **Baseline Churn Rate**: 26.5% (2,650 churned accounts/year).
* **Average Customer Lifetime Value (CLV)**: $1,000.
* **Annual Revenue Loss**: 2,650 customers × $1,000 = **$2,650,000**.

### Implementing Our Model (Logistic Regression)
* **Recall (55.88%)**: Out of 2,650 churners, our model flags **1,480 customers** as high risk.
* **Retention Success (50%)**: If targeted offers retain just half of those flagged, we save **740 customers**.
* **Saved Revenue**: 740 customers × $1,000 = **+$740,000**.
* **Type I Error Overhead (FP = 7.67%)**: 767 loyal customers are flagged as churners. If we offer each a $50 loyalty credit, the campaign cost is 767 × $50 = **-$38,350**.
* **Net Annual ROI**: $740,000 - $38,350 = **+$701,650 saved annually**!

---

## 🏷️ Dataset Profile
The system utilizes the classic **IBM Watson Telco Customer Churn dataset** (7,043 rows, 21 columns) containing:
* **Demographics**: Gender, Senior Citizen status, Partners, and Dependents.
* **Services**: Phone service, multiple lines, internet provider type, security, backups, device protection, streaming TV, and streaming movies.
* **Account Info**: Tenure (months active), contract type (month-to-month, annual, two-year), payment method, monthly charges, and total charges.

---

## 📂 Project Architecture & Directory Structure
The repository is refactored into a decoupled modular structure separating page presentations, logic services, widgets, and utilities:

```text
customer-churn-prediction/
├── app/
│   ├── components/           # Reusable styled UI widgets & layout functions
│   │   ├── cards.py          # Custom metric, verdict, and step wizards
│   │   ├── sidebar.py        # Static sidebar with developer profiles & specs
│   │   └── styles.py         # Premium dark-theme & glassmorphism CSS
│   ├── services/             # Core business logic layer
│   │   ├── analytics_service.py # Cohort filtering & loading
│   │   ├── history_service.py   # Prediction logging & CSV logs database manager
│   │   └── prediction_service.py # Pipeline caching & inference contributions
│   ├── utils/                # Shared helper functions
│   │   ├── config.py         # Centralized parameters & data directories
│   │   ├── export.py         # CSV, Text diagnostics, and FPDF2 PDF exports
│   │   └── validators.py     # Inputs boundary constraints validations
│   ├── pages/                # Multi-page routing views
│   │   ├── 1_predictor.py    # Predictor Wizard
│   │   ├── 2_analytics.py    # Cohort visualizations dashboard
│   │   ├── 3_model_performance.py # Precision-Recall, ROC, Confusion heatmaps
│   │   ├── 4_insights.py     # Action playbooks & segmentations
│   │   └── 5_admin.py        # Log administration command console
│   ├── home_content.py       # Landing page specifications template
│   └── main.py               # Main application routing entrypoint
├── data/
│   ├── raw/                  # Original raw dataset
│   └── processed/            # Preprocessed & cleaned CSV (ready for ML)
├── models/                   # Serialized model, scaler, and layout components (.pkl)
│   ├── model.pkl             # Best Model (Logistic Regression)
│   ├── scaler.pkl            # Standard Scaler
│   ├── feature_names.pkl     # Dummy column names
│   └── label_encoder.pkl     # Binary categories mappings
├── reports/                  # Generated figures & evaluation diagnostics
├── spec/                     # Architecture & Case Study specification documentation
├── src/                      # Data engineering & model training scripts
│   ├── download_data.py      # Dataset acquisition
│   ├── preprocess.py         # Data cleaning & type conversion
│   ├── model_training.py     # Training and model benchmarking
│   └── model_evaluation.py   # Diagnostics and figures generator
├── tests/                    # Preprocessing & inference unit tests
├── requirements.txt          # Package dependencies
└── README.md                 # Main portfolio documentation
```

---

## ⚙️ Machine Learning Pipeline

### 1. Data Cleaning
- Handled empty string spaces in `TotalCharges` (coerced type conversion to float, introducing 11 NaNs).
- Imputed those 11 NaNs to `0.0` as they represented new customers with `tenure = 0` (who haven't been billed yet).
- Dropped unique identifiers (`customerID`) to prevent model overfitting.

### 2. Feature Engineering
- **Label Encoding**: Binary categories (`gender`, `Partner`, `Dependents`, `PhoneService`, `PaperlessBilling`) mapped to 0/1.
- **One-Hot Encoding**: Applied pandas get_dummies with `drop_first=True` on multi-class objects (`Contract`, `InternetService`, `PaymentMethod`, etc.) to prevent collinearity.
- **Scaling**: Standardized numerical features (`tenure`, `MonthlyCharges`, `TotalCharges`) using `StandardScaler` (fit on training data only).

### 3. Model Training & Diagnostics
Three classifiers were benchmarked using an 80/20 train/test split:
- **Logistic Regression** (Standardized)
- **Decision Tree** (Shallow depth `max_depth=6` to prevent overfitting)
- **Random Forest** (Bootstrap forest `max_depth=10`)

---

## 📊 Model Comparison & Results

During test-set validation, the benchmarked classifiers yielded:

| Model Name | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **80.62%** | 65.93% | **55.88%** | **60.49%** | **0.8422** |
| **Decision Tree** | 80.06% | **66.67%** | 49.73% | 56.97% | 0.8219 |
| **Random Forest** | 80.34% | 66.44% | 52.41% | 58.59% | 0.8401 |

* **Model Selection**: **Logistic Regression** was chosen due to its high F1-Score and ROC-AUC, offering the best balance for catching churners without excessive false alarms.

---

## 🖥️ Streamlit Multi-Page Web Application
The deployed interface provides:
* **🏠 Home**: Overview, project scopes, technical specifications, and centralized KPI widgets.
* **🔮 Churn Predictor**: Step-by-step wizard forms, input validation rules, probability scoring, localized Plotly driver charts, and one-click PDF, CSV, or Text reports exporters.
* **📊 Analytics**: Dynamic cohort segmentations, distribution histograms, contract ratio comparisons, billing boxplots, payment methods, and variable correlation heatmaps.
* **📈 Model Performance**: Interactive confusion matrix heatmaps, ROC curves, and Precision-Recall trade-off plots.
* **💡 Business Insights**: Stakeholder-centric playbooks outlining risk migration strategies.
* **🔐 Admin Console**: Credential-authenticated log query center featuring search tools and log purging controls.

---

## 🛠️ Installation & How to Run

### 1. Clone & Setup Environment
```bash
git clone https://github.com/naveenpixel1/customer-churn-prediction.git
cd customer-churn-prediction
python -m venv venv
venv\Scripts\activate
```

### 2. Install Packages
```bash
pip install -r requirements.txt
```

### 3. Re-run Pipeline (Optional)
```bash
python src/download_data.py
python src/preprocess.py
python src/model_training.py
python src/model_evaluation.py
```

### 4. Execute Test Suite
```bash
pytest
```

### 5. Launch Streamlit Application
```bash
streamlit run app/main.py
```

---

## 🔮 Future Enhancements
* **Hyperparameter Tuning**: Run GridSearch / Optuna to optimize Random Forest weights.
* **Advanced Ensembles**: Integrate XGBoost, LightGBM, and CatBoost models.
* **SMOTE (Oversampling)**: Implement Synthetic Minority Over-sampling Technique to resolve minority class imbalance.

---

## 👨‍💻 Author & License
* **Developer**: **Naveen Kumar .D**
* **Year**: 2026
* **License**: MIT License
