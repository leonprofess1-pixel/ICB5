
import pandas as pd

def analyze_high_performer_data():
    """
    Calculates key metrics for the High-Performer Attrition report.
    """
    file_path = './HR-employee-attrition_v2/HR-Employee-Attrition.csv'
    df_full = pd.read_csv(file_path)

    # Filter for high-performers
    df = df_full[df_full['PerformanceRating'].isin([3, 4])].copy()

    total_high_performers = len(df)
    attrition_count = df['Attrition'].value_counts().get('Yes', 0)
    overall_attrition_rate = (attrition_count / total_high_performers) * 100 if total_high_performers > 0 else 0
    
    print("--- High-Performer Summary Metrics ---")
    print(f"Total High-Performers: {total_high_performers}")
    print(f"High-Performer Attrition Count: {attrition_count}")
    print(f"Attrition Rate Among High-Performers: {overall_attrition_rate:.1f}%")
    print("-" * 30)

    # Additional analysis comparing leavers and stayers within the high-performer group
    
    # 1. PercentSalaryHike
    print("\n--- 1. Salary Hike Analysis ---")
    hike_stats = df.groupby('Attrition')['PercentSalaryHike'].mean()
    print(f"Avg Salary Hike (Leaver): {hike_stats.get('Yes', 0):.1f}%")
    print(f"Avg Salary Hike (Stayer): {hike_stats.get('No', 0):.1f}%")

    # 2. Income and Career
    print("\n--- 2. Income and Career Analysis ---")
    income_stats = df.groupby('Attrition')['MonthlyIncome'].mean()
    print(f"Avg Monthly Income (Leaver): ${income_stats.get('Yes', 0):.0f}")
    print(f"Avg Monthly Income (Stayer): ${income_stats.get('No', 0):.0f}")

    # 3. Job Satisfaction vs. Job Involvement
    print("\n--- 3. Satisfaction vs. Involvement ---")
    satisfaction_stats = df.groupby('Attrition')['JobSatisfaction'].mean()
    involvement_stats = df.groupby('Attrition')['JobInvolvement'].mean()
    print(f"Avg Job Satisfaction (Leaver): {satisfaction_stats.get('Yes', 0):.2f}")
    print(f"Avg Job Satisfaction (Stayer): {satisfaction_stats.get('No', 0):.2f}")
    print(f"Avg Job Involvement (Leaver): {involvement_stats.get('Yes', 0):.2f}")
    print(f"Avg Job Involvement (Stayer): {involvement_stats.get('No', 0):.2f}")

    # 4. StockOptionLevel
    print("\n--- 4. Stock Option Analysis ---")
    stock_rates = df.groupby('StockOptionLevel')['Attrition'].value_counts(normalize=True).unstack().fillna(0) * 100
    if 0 in stock_rates.index and 'Yes' in stock_rates.columns:
        print(f"Attrition Rate (StockOptionLevel 0): {stock_rates.loc[0, 'Yes']:.1f}%")
    if 1 in stock_rates.index and 'Yes' in stock_rates.columns:
        print(f"Attrition Rate (StockOptionLevel 1): {stock_rates.loc[1, 'Yes']:.1f}%")
        
    # 5. YearsSinceLastPromotion
    print("\n--- 5. Promotion Analysis ---")
    promotion_stats = df.groupby('Attrition')['YearsSinceLastPromotion'].mean()
    print(f"Avg Years Since Last Promotion (Leaver): {promotion_stats.get('Yes', 0):.2f} years")
    print(f"Avg Years Since Last Promotion (Stayer): {promotion_stats.get('No', 0):.2f} years")

if __name__ == '__main__':
    analyze_high_performer_data()
