import pandas as pd

def analyze_attrition_data():
    """
    Calculates key metrics for the HR Attrition report.
    """
    file_path = './HR-employee-attrition_v2/HR-Employee-Attrition.csv'
    df = pd.read_csv(file_path)

    total_employees = len(df)
    attrition_count = df['Attrition'].value_counts()['Yes']
    overall_attrition_rate = (attrition_count / total_employees) * 100
    
    print("--- Executive Summary Metrics ---")
    print(f"Total Employees: {total_employees}")
    print(f"Total Attrition Count: {attrition_count}")
    print(f"Overall Attrition Rate: {overall_attrition_rate:.1f}%")
    print("-" * 30)

    print("\n--- 1. Total Working Years Analysis ---")
    early_career_attrition_df = df[df['TotalWorkingYears'] <= 7]
    early_career_attrition_rate = (len(early_career_attrition_df[early_career_attrition_df['Attrition'] == 'Yes']) / len(early_career_attrition_df)) * 100
    attrition_by_year_1 = len(df[(df['TotalWorkingYears'] == 1) & (df['Attrition'] == 'Yes')])
    total_by_year_1 = len(df[df['TotalWorkingYears'] == 1])
    rate_by_year_1 = (attrition_by_year_1 / total_by_year_1) * 100
    print(f"Attrition Rate (<=7 years service): {early_career_attrition_rate:.1f}%")
    print(f"Attrition Rate (1st year): {rate_by_year_1:.1f}% ({attrition_by_year_1} out of {total_by_year_1})")
    
    print("\n--- 2. Income and Career Analysis ---")
    income_stats = df.groupby('Attrition')['MonthlyIncome'].mean()
    working_years_stats = df.groupby('Attrition')['TotalWorkingYears'].mean()
    print(f"Avg Monthly Income (Leaver): ${income_stats['Yes']:.0f}")
    print(f"Avg Monthly Income (Stayer): ${income_stats['No']:.0f}")
    print(f"Avg Total Working Years (Leaver): {working_years_stats['Yes']:.1f}")
    print(f"Avg Total Working Years (Stayer): {working_years_stats['No']:.1f}")

    print("\n--- 3. Age Analysis ---")
    age_25_34 = df[(df['Age'] >= 25) & (df['Age'] <= 34)]
    age_25_34_attrition_rate = (len(age_25_34[age_25_34['Attrition'] == 'Yes']) / len(age_25_34)) * 100
    avg_age = df.groupby('Attrition')['Age'].mean()
    print(f"Attrition Rate (25-34 age group): {age_25_34_attrition_rate:.1f}%")
    print(f"Avg Age (Leaver): {avg_age['Yes']:.1f}")
    print(f"Avg Age (Stayer): {avg_age['No']:.1f}")

    print("\n--- 4. Job Satisfaction Analysis ---")
    satisfaction_rates = df.groupby('JobSatisfaction')['Attrition'].value_counts(normalize=True).unstack().fillna(0) * 100
    print(f"Attrition Rate (Satisfaction Lvl 1): {satisfaction_rates.loc[1, 'Yes']:.1f}%")
    print(f"Attrition Rate (Satisfaction Lvl 4): {satisfaction_rates.loc[4, 'Yes']:.1f}%")

    print("\n--- 6. Marital Status Analysis ---")
    marital_rates = df.groupby('MaritalStatus')['Attrition'].value_counts(normalize=True).unstack().fillna(0) * 100
    print(f"Attrition Rate (Single): {marital_rates.loc['Single', 'Yes']:.1f}%")
    print(f"Attrition Rate (Married): {marital_rates.loc['Married', 'Yes']:.1f}%")
    
    print("\n--- 7. Income Gap at Age 30 ---")
    income_gap_30 = df[df['Age'] == 30].groupby('Attrition')['MonthlyIncome'].mean()
    if 'Yes' in income_gap_30 and 'No' in income_gap_30:
        print(f"Income Gap at 30 (Avg Stayer - Avg Leaver): ${income_gap_30['No'] - income_gap_30['Yes']:.0f}")
    
    print("\n--- 8. Attrition by Education Field ---")
    education_rates = df.groupby('EducationField')['Attrition'].value_counts(normalize=True).unstack().fillna(0) * 100
    print(f"Attrition Rate (Technical Degree): {education_rates.loc['Technical Degree', 'Yes']:.1f}%")
    print(f"Attrition Rate (Marketing): {education_rates.loc['Marketing', 'Yes']:.1f}%")

    print("\n--- 9. JobLevel & EnvSatisfaction Analysis ---")
    jl1_es1 = df[(df['JobLevel'] == 1) & (df['EnvironmentSatisfaction'] == 1)]
    if not jl1_es1.empty:
        jl1_es1_attrition_rate = (len(jl1_es1[jl1_es1['Attrition'] == 'Yes']) / len(jl1_es1)) * 100
        print(f"Attrition Rate (JobLevel 1 & EnvSatisfaction 1): {jl1_es1_attrition_rate:.1f}%")

    print("\n--- 10. Income Gap for Sales Representative ---")
    sales_rep_income = df[df['JobRole'] == 'Sales Representative'].groupby('Attrition')['MonthlyIncome'].median()
    if 'Yes' in sales_rep_income and 'No' in sales_rep_income:
        print(f"Income Gap (Median, Sales Rep): ${sales_rep_income['No'] - sales_rep_income['Yes']:.0f}")

if __name__ == '__main__':
    analyze_attrition_data()