
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set font for matplotlib
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def analysis():
    # Create output directory if it doesn't exist
    if not os.path.exists('online-retail/output'):
        os.makedirs('online-retail/output')

    # Load the dataset
    df = pd.read_csv('../online_retail.csv.zip', encoding='ISO-8859-1')

    # --- Data Cleaning and Preprocessing ---

    # Drop rows with missing CustomerID
    df.dropna(subset=['CustomerID'], inplace=True)

    # Convert CustomerID to integer
    df['CustomerID'] = df['CustomerID'].astype(int)

    # Remove returns (InvoiceNo starting with 'C')
    df = df[~df['InvoiceNo'].str.startswith('C', na=False)]

    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Calculate TotalPrice
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    # Extract YearMonth for monthly analysis
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')

    # --- ARPU Calculation ---

    # Group by YearMonth to calculate monthly revenue and unique customers
    monthly_data = df.groupby('YearMonth').agg(
        MonthlyRevenue=('TotalPrice', 'sum'),
        MonthlyActiveUsers=('CustomerID', 'nunique')
    )

    # Calculate ARPU
    monthly_data['ARPU'] = monthly_data['MonthlyRevenue'] / monthly_data['MonthlyActiveUsers']

    # Reset index to make YearMonth a column
    monthly_data = monthly_data.reset_index()
    monthly_data['YearMonth'] = monthly_data['YearMonth'].astype(str)


    # --- Visualization ---

    # 1. Line Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='YearMonth', y='ARPU', data=monthly_data, marker='o')
    plt.title('월별 가입자당 평균 매출 (ARPU)')
    plt.xlabel('월')
    plt.ylabel('ARPU')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('online-retail/output/arpu_line_plot.png')
    plt.close()

    # 2. Bar Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x='YearMonth', y='ARPU', data=monthly_data, palette='viridis')
    plt.title('월별 가입자당 평균 매출 (ARPU)')
    plt.xlabel('월')
    plt.ylabel('ARPU')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('online-retail/output/arpu_bar_plot.png')
    plt.close()

    return monthly_data

if __name__ == '__main__':
    arpu_data = analysis()
    print("ARPU data calculation and visualization complete.")
    print(arpu_data)
    

