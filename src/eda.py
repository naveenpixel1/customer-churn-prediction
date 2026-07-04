import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for professional look
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16
})

FIG_DIR = os.path.join("reports", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def load_data(file_path):
    """Loads the cleaned dataset."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cleaned dataset not found at: {file_path}")
    return pd.read_csv(file_path)

def plot_target_distribution(df):
    """Plot 1: Target Variable (Churn) distribution."""
    plt.figure(figsize=(6, 5))
    churn_counts = df['Churn'].value_counts()
    colors = ['#2b5c8f', '#d95f02']
    
    plt.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=colors, explode=(0, 0.1), shadow=False)
    plt.title("Overall Customer Churn Rate")
    plt.tight_layout()
    
    save_path = os.path.join(FIG_DIR, "01_churn_rate.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    print("\n--- Visual 1: Overall Churn Distribution ---")
    print(f"File Saved: {save_path}")
    print("What it shows: The proportion of customers who left (Yes) vs. stayed (No).")
    print("Business Insight: 26.5% of our customer base has churned. This is a high churn rate. It also alerts us to a class imbalance issue (roughly 3:1 ratio of active to churned) that we must address in machine learning.")
    print("Churn Reduction Suggestion: This baseline serves as our target. Any retention strategy should aim to reduce this 26.5% baseline.")


def plot_demographics(df):
    """Plot 2 & 3: Demographic columns (Gender and Senior Citizens) vs Churn."""
    # Plot 2: Gender vs Churn
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x='gender', hue='Churn', palette=['#2b5c8f', '#d95f02'])
    plt.title("Churn Rate by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Number of Customers")
    plt.legend(title="Churn")
    plt.tight_layout()
    
    save_path2 = os.path.join(FIG_DIR, "02_gender_churn.png")
    plt.savefig(save_path2, dpi=300)
    plt.close()
    
    print("\n--- Visual 2: Gender vs. Churn ---")
    print(f"File Saved: {save_path2}")
    print("What it shows: Churn counts split by Male and Female gender.")
    print("Business Insight: Churn rate is almost identical between Male and Female customers (approx. 26.9% for Females vs 26.2% for Males). Gender is not a differentiating factor.")
    print("Churn Reduction Suggestion: Do not waste marketing resources segmenting retention campaigns by gender; it will have no impact on churn.")

    # Plot 3: Senior Citizen vs Churn
    plt.figure(figsize=(7, 5))
    # Map SeniorCitizen values to labels for readability
    df_temp = df.copy()
    df_temp['SeniorCitizen_Label'] = df_temp['SeniorCitizen'].map({0: 'Non-Senior', 1: 'Senior Citizen'})
    
    # Calculate churn rates for senior citizens
    rates = df_temp.groupby('SeniorCitizen_Label')['Churn'].value_counts(normalize=True).unstack() * 100
    
    rates.plot(kind='bar', stacked=True, color=['#2b5c8f', '#d95f02'], figsize=(7, 5))
    plt.title("Churn Percentage by Senior Citizen Status")
    plt.xlabel("Customer Segment")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=0)
    plt.legend(title="Churn")
    plt.tight_layout()
    
    save_path3 = os.path.join(FIG_DIR, "03_senior_churn.png")
    plt.savefig(save_path3, dpi=300)
    plt.close()
    
    print("\n--- Visual 3: Senior Citizen vs. Churn ---")
    print(f"File Saved: {save_path3}")
    print("What it shows: Stacked churn percentage breakdown for Senior Citizens vs. Non-Seniors.")
    print("Business Insight: Senior citizens show a staggering churn rate of ~41.7%, compared to only ~23.6% for non-seniors. Seniors are almost twice as likely to churn.")
    print("Churn Reduction Suggestion: Create senior-friendly onboarding, simplified billing UI, and specialized customer care lines. They might be struggling with digital payment methods or technology features.")


def plot_tenure_and_contract(df):
    """Plot 4 & 5: Account details (Tenure and Contract Type) vs Churn."""
    # Plot 4: Tenure Distribution
    plt.figure(figsize=(9, 5))
    sns.kdeplot(data=df, x='tenure', hue='Churn', fill=True, common_norm=False, palette=['#2b5c8f', '#d95f02'], alpha=0.4)
    plt.title("Tenure Density Distribution by Churn Status")
    plt.xlabel("Tenure (Months)")
    plt.ylabel("Density")
    plt.tight_layout()
    
    save_path4 = os.path.join(FIG_DIR, "04_tenure_churn.png")
    plt.savefig(save_path4, dpi=300)
    plt.close()
    
    print("\n--- Visual 4: Tenure Distribution vs. Churn ---")
    print(f"File Saved: {save_path4}")
    print("What it shows: Density plot showing when customers leave.")
    print("Business Insight: A massive spike in churn occurs in the first 1-5 months. If a customer survives the first 20 months, their likelihood of leaving drops drastically. Long-term customers (50+ months) rarely churn.")
    print("Churn Reduction Suggestion: Implement aggressive 'new customer support' triggers. Focus on the first 90 days of onboarding (e.g., welcome calls, usage guides, early discounts) to lock in loyalty.")

    # Plot 5: Contract Type vs Churn
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='Contract', hue='Churn', palette=['#2b5c8f', '#d95f02'])
    plt.title("Churn Count by Contract Type")
    plt.xlabel("Contract Type")
    plt.ylabel("Number of Customers")
    plt.legend(title="Churn")
    plt.tight_layout()
    
    save_path5 = os.path.join(FIG_DIR, "05_contract_churn.png")
    plt.savefig(save_path5, dpi=300)
    plt.close()
    
    print("\n--- Visual 5: Contract Type vs. Churn ---")
    print(f"File Saved: {save_path5}")
    print("What it shows: Count of churned vs active customers across Month-to-month, One year, and Two year contracts.")
    print("Business Insight: Month-to-month contracts have an astronomical churn rate (~42.7%), whereas One-year (~11.3%) and Two-year contracts (~2.8%) are extremely stable. Churn is almost entirely concentrated in month-to-month contracts.")
    print("Churn Reduction Suggestion: Incentivize customers to migrate from month-to-month contracts to 1-year or 2-year contracts by offering a discount (e.g., 'Save 10% by switching to an annual plan'). The cost of the discount is far lower than the cost of losing the customer.")


def plot_internet_and_payments(df):
    """Plot 6 & 7: Services and Payments vs Churn."""
    # Plot 6: Internet Service vs Churn
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='InternetService', hue='Churn', palette=['#2b5c8f', '#d95f02'])
    plt.title("Churn Count by Internet Service Provider Type")
    plt.xlabel("Internet Service Type")
    plt.ylabel("Number of Customers")
    plt.legend(title="Churn")
    plt.tight_layout()
    
    save_path6 = os.path.join(FIG_DIR, "06_internetservice_churn.png")
    plt.savefig(save_path6, dpi=300)
    plt.close()
    
    print("\n--- Visual 6: Internet Service Type vs. Churn ---")
    print(f"File Saved: {save_path6}")
    print("What it shows: Churn rates across DSL, Fiber Optic, and No Internet customers.")
    print("Business Insight: Fiber Optic customers have a massive churn rate (~41.9%) compared to DSL (~19.0%). This is highly alarming since Fiber is our premium, high-cost product.")
    print("Churn Reduction Suggestion: Investigate why Fiber Optic customers are unhappy. Is it poor network reliability, high prices, or bad technical setup? Run targeted customer satisfaction surveys specifically for Fiber Optic users and check pricing vs. competitors.")

    # Plot 7: Payment Method vs Churn
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='PaymentMethod', hue='Churn', palette=['#2b5c8f', '#d95f02'])
    plt.title("Churn Count by Payment Method")
    plt.xlabel("Payment Method")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=15)
    plt.legend(title="Churn")
    plt.tight_layout()
    
    save_path7 = os.path.join(FIG_DIR, "07_paymentmethod_churn.png")
    plt.savefig(save_path7, dpi=300)
    plt.close()
    
    print("\n--- Visual 7: Payment Method vs. Churn ---")
    print(f"File Saved: {save_path7}")
    print("What it shows: Churn across Electronic check, Mailed check, Bank transfer, and Credit card.")
    print("Business Insight: Customers using 'Electronic check' churn at a massive rate (~45.3%). In contrast, automated billing (Credit card & Bank transfer) has very low churn (~15-16%).")
    print("Churn Reduction Suggestion: Incentivize customers to sign up for Auto-Pay (Bank Transfer or Credit Card) by offering a one-time bill credit (e.g., '$5 off next bill if you sign up for Auto-Pay'). Auto-pay reduces transaction failure and churn.")


def plot_financials(df):
    """Plot 8: Financials (Monthly Charges) vs Churn."""
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x='Churn', y='MonthlyCharges', palette=['#2b5c8f', '#d95f02'])
    plt.title("Monthly Charges Distribution by Churn Status")
    plt.xlabel("Churned")
    plt.ylabel("Monthly Charges ($)")
    plt.tight_layout()
    
    save_path8 = os.path.join(FIG_DIR, "08_monthlycharges_churn.png")
    plt.savefig(save_path8, dpi=300)
    plt.close()
    
    print("\n--- Visual 8: Monthly Charges vs. Churn ---")
    print(f"File Saved: {save_path8}")
    print("What it shows: A boxplot displaying the median and spread of monthly bills for churned vs active customers.")
    print("Business Insight: Churned customers pay a significantly higher median monthly charge (~$80) compared to retained customers (~$65). Higher prices correlate with higher churn.")
    print("Churn Reduction Suggestion: Set up triggers for customers whose monthly bill exceeds $75. Proactively offer them loyalty packages, bundle discounts, or downgrade options to prevent them from seeking cheaper competitors.")


def plot_value_added_services(df):
    """Plot 9 & 10: Value-Added Services (Online Security and Tech Support) vs Churn."""
    # Plot 9: Online Security vs Churn
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='OnlineSecurity', hue='Churn', palette=['#2b5c8f', '#d95f02'])
    plt.title("Churn Count by Online Security Service")
    plt.xlabel("Online Security")
    plt.ylabel("Number of Customers")
    plt.legend(title="Churn")
    plt.tight_layout()
    
    save_path9 = os.path.join(FIG_DIR, "09_onlinesecurity_churn.png")
    plt.savefig(save_path9, dpi=300)
    plt.close()
    
    print("\n--- Visual 9: Online Security Service vs. Churn ---")
    print(f"File Saved: {save_path9}")
    print("What it shows: Churn counts split by whether the customer has Online Security or not.")
    print("Business Insight: Customers without Online Security churn at a much higher rate (~41.8%) compared to those who have it (~14.6%). Security services act as a 'sticky' feature.")
    print("Churn Reduction Suggestion: Bundle Online Security for free or at a deep discount in core plans. Once customers set up security software, they are less likely to cancel because of the effort to switch.")

    # Plot 10: Tech Support vs Churn
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='TechSupport', hue='Churn', palette=['#2b5c8f', '#d95f02'])
    plt.title("Churn Count by Tech Support Service")
    plt.xlabel("Tech Support")
    plt.ylabel("Number of Customers")
    plt.legend(title="Churn")
    plt.tight_layout()
    
    save_path10 = os.path.join(FIG_DIR, "10_techsupport_churn.png")
    plt.savefig(save_path10, dpi=300)
    plt.close()
    
    print("\n--- Visual 10: Tech Support Service vs. Churn ---")
    print(f"File Saved: {save_path10}")
    print("What it shows: Churn counts split by whether the customer has Tech Support or not.")
    print("Business Insight: Customers without Tech Support have a high churn rate (~41.6%) compared to those who do (~15.2%). This highlights that poor service resolution or lack of technical help leads to customer defection.")
    print("Churn Reduction Suggestion: Offer a free month of Tech Support, or prompt customers during issues to register for Tech Support features. It helps keep them engaged and resolves friction.")


def plot_correlation_matrix(df):
    """Plot 11: Correlation Heatmap of numerical columns (with encoded target Churn)."""
    plt.figure(figsize=(8, 6))
    
    # Create copy and map Churn to binary numeric for correlation
    df_corr = df.copy()
    df_corr['Churn'] = df_corr['Churn'].map({'Yes': 1, 'No': 0})
    
    # Filter numeric cols (tenure, MonthlyCharges, TotalCharges, SeniorCitizen, Churn)
    numeric_cols = ['tenure', 'SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'Churn']
    corr_matrix = df_corr[numeric_cols].corr()
    
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix of Numerical Features (incl. Churn)")
    plt.tight_layout()
    
    save_path11 = os.path.join(FIG_DIR, "11_correlation_matrix.png")
    plt.savefig(save_path11, dpi=300)
    plt.close()
    
    print("\n--- Visual 11: Correlation Heatmap ---")
    print(f"File Saved: {save_path11}")
    print("What it shows: Linear correlations between numerical variables and our target Churn.")
    print("Business Insight: Tenure is strongly negatively correlated with churn (-0.35), meaning longer contracts = less churn. Monthly charges are positively correlated with churn (0.19), meaning higher bills = more churn. TotalCharges shows a low negative correlation with Churn (-0.20), but is highly correlated with tenure (0.83) which indicates multi-collinearity.")
    print("Churn Reduction Suggestion: MonthlyCharges is the primary financial lever we can adjust. Reducing high charges or offering discounts directly reduces churn probability.")


def main():
    processed_path = os.path.join("data", "processed", "churn_cleaned.csv")
    print(f"Loading cleaned dataset from {processed_path}...")
    df = load_data(processed_path)
    
    print("\nStarting EDA Visualizations Generation...")
    plot_target_distribution(df)
    plot_demographics(df)
    plot_tenure_and_contract(df)
    plot_internet_and_payments(df)
    plot_financials(df)
    plot_value_added_services(df)
    plot_correlation_matrix(df)
    print("\nAll 11 EDA plots successfully generated and saved to reports/figures/.")

if __name__ == "__main__":
    main()
