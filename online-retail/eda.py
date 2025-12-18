
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import io
import datetime as dt
import base64

def embed_plot_to_report():
    """Saves the current plot to a base64 string and returns the markdown image tag."""
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f"![Plot](data:image/png;base64,{img_str})\n\n"

def load_data(file_path):
    """Loads the online retail dataset from a csv file."""
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
    return df

def clean_data(df):
    """Cleans the online retail dataframe."""
    df.dropna(subset=['CustomerID'], inplace=True)
    df['Description'].fillna('No description', inplace=True)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype(int).astype(str)
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    return df

def generate_report(df):
    """Generates an EDA report in markdown format."""
    # Initialize markdown report
    report = """
# Online Retail Dataset EDA Report

## 1. Data Overview
"""

    # Data shape, head, and info
    report += "### Data Shape\n"
    report += f"<p>{df.shape}</p>\n\n"
    report += "### Data Head\n"
    report += df.head().to_markdown() + "\n\n"
    report += "### Data Info\n"
    
    # Redirect info() output to a string
    buffer = io.StringIO()
    df.info(buf=buffer)
    report += "<pre>" + buffer.getvalue() + "</pre>\n\n"
    
    report += """
## 2. Analysis Methods and Criteria

This report analyzes the Online Retail dataset to understand sales patterns and customer behavior. The analysis was conducted using the following methods and criteria:

1.  **Data Loading and Initial Exploration**: The dataset is loaded using the `pandas` library. An initial overview of the data is conducted to understand its structure, including the number of rows and columns, data types of each column, and the first few rows.
2.  **Data Cleaning and Preprocessing**:
    *   **Missing Values**: Rows with missing `CustomerID` are removed as they cannot be attributed to a specific customer. Missing `Description` values are filled with 'No description'.
    *   **Data Types**: `InvoiceDate` is converted to a datetime object for time-series analysis, and `CustomerID` is converted to a string.
    *   **Invalid Data**: Rows with a `Quantity` less than or equal to 0 and a `UnitPrice` less than or equal to 0 are removed to focus the analysis on valid sales transactions.
    *   **Feature Engineering**: A `TotalPrice` column is created by multiplying `Quantity` and `UnitPrice`.
3.  **Exploratory Data Analysis (EDA)**: Various EDA techniques are used to uncover patterns and insights:
    *   **Sales Trends**: Monthly, daily, and hourly sales trends are analyzed to identify peak sales periods.
    *   **Geographical Analysis**: Sales are aggregated by country to identify the top 10 countries by sales.
    *   **Product Analysis**: Products are ranked by the total quantity sold to find the top 10 best-selling items.
    *   **Price and Quantity Distribution**: The distributions of `UnitPrice` and `Quantity` are examined to understand their characteristics.
    *   **Customer-level Analysis**: Total sales per customer are analyzed to understand the distribution of customer spending.
    *   **Correlation Analysis**: A heatmap is used to visualize the correlation between numerical features (`Quantity`, `UnitPrice`, `TotalPrice`).
    *   **User Activity**: Daily Active Users (DAU) and Monthly Active Users (MAU) are calculated to measure user engagement.
    *   **Retention Analysis**: Monthly cohort analysis is performed to calculate customer retention rates over time. This helps in understanding how well the business retains its customers.

4.  **Visualization**: All analyses are accompanied by visualizations created using `matplotlib` and `seaborn` to provide a clear and intuitive understanding of the results. All plots are saved as images and included in this report.
"""
    
    # --- Data Cleaning and Preprocessing ---
    report += "## 3. Data Cleaning and Preprocessing\n"
    
    # Handle missing values
    report += "### Missing Values\n"
    # Re-create original df to show missing values before cleaning
    original_df = load_data('online-retail/online_retail.csv')
    report += "<pre>" + original_df.isnull().sum().to_string() + "</pre>\n\n"
    report += "After handling missing values:\n"
    report += "<pre>" + df.isnull().sum().to_string() + "</pre>\n\n"
    
    # --- Descriptive Statistics ---
    report += "## 4. Descriptive Statistics\n"
    report += df.describe().to_markdown() + "\n\n"

    # --- EDA and Visualization ---
    report += "## 5. Exploratory Data Analysis and Visualization\n"

    # 1. Monthly Sales Trend
    report += "### 1. 월별 매출 추이\n"
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
    monthly_sales = df.groupby('YearMonth')['TotalPrice'].sum()
    monthly_sales.index = monthly_sales.index.to_timestamp()

    plt.figure(figsize=(12, 6))
    sns.lineplot(x=monthly_sales.index, y=monthly_sales.values)
    plt.title('월별 총 매출')
    plt.xlabel('월')
    plt.ylabel('총 매출')
    plt.grid(True)
    report += embed_plot_to_report()
    report += monthly_sales.to_frame().to_markdown() + "\n\n"

    # 2. Sales by Day of the Week
    report += "### 2. 요일별 매출\n"
    df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
    daily_sales = df.groupby('DayOfWeek')['TotalPrice'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    plt.figure(figsize=(10, 5))
    daily_sales.plot(kind='bar')
    plt.title('요일별 총 매출')
    plt.xlabel('요일')
    plt.ylabel('총 매출')
    report += embed_plot_to_report()
    report += daily_sales.to_frame().to_markdown() + "\n\n"
    
    # 3. Sales by Hour of the Day
    report += "### 3. 시간대별 매출\n"
    df['Hour'] = df['InvoiceDate'].dt.hour
    hourly_sales = df.groupby('Hour')['TotalPrice'].sum()
    
    plt.figure(figsize=(12, 6))
    hourly_sales.plot(kind='bar')
    plt.title('시간대별 총 매출')
    plt.xlabel('시간')
    plt.ylabel('총 매출')
    report += embed_plot_to_report()
    report += hourly_sales.to_frame().to_markdown() + "\n\n"

    # 4. Top 10 Countries by Sales
    report += "### 4. 상위 10개국 매출\n"
    top_10_countries = df.groupby('Country')['TotalPrice'].sum().nlargest(10)
    
    plt.figure(figsize=(12, 6))
    top_10_countries.plot(kind='bar')
    plt.title('상위 10개국 총 매출')
    plt.xlabel('국가')
    plt.ylabel('총 매출')
    report += embed_plot_to_report()
    report += top_10_countries.to_frame().to_markdown() + "\n\n"
    
    # 5. Top 10 Products by Quantity Sold
    report += "### 5. 가장 많이 팔린 상품 10선\n"
    top_10_products = df.groupby('Description')['Quantity'].sum().nlargest(10)
    
    plt.figure(figsize=(12, 6))
    top_10_products.plot(kind='bar')
    plt.title('가장 많이 팔린 상품 10선')
    plt.xlabel('상품 설명')
    plt.ylabel('총 판매 수량')
    report += embed_plot_to_report()
    report += top_10_products.to_frame().to_markdown() + "\n\n"

    # 6. Distribution of Unit Price
    report += "### 6. 단가 분포\n"
    plt.figure(figsize=(10, 6))
    sns.histplot(df['UnitPrice'], bins=50, kde=True)
    plt.title('단가 분포 (로그 스케일)')
    plt.xlabel('단가')
    plt.ylabel('빈도')
    plt.yscale('log')
    report += embed_plot_to_report()

    # 7. Distribution of Quantity
    report += "### 7. 수량 분포\n"
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Quantity'], bins=50, kde=True)
    plt.title('수량 분포 (로그 스케일)')
    plt.xlabel('수량')
    plt.ylabel('빈도')
    plt.yscale('log')
    report += embed_plot_to_report()

    # 8. Total Sales per Customer
    report += "### 8. 고객별 총 매출\n"
    customer_sales = df.groupby('CustomerID')['TotalPrice'].sum()
    plt.figure(figsize=(10, 6))
    sns.histplot(customer_sales, bins=50, kde=True)
    plt.title('고객별 총 매출 분포 (로그 스케일)')
    plt.xlabel('총 매출')
    plt.ylabel('고객 수')
    plt.yscale('log')
    report += embed_plot_to_report()

    # 9. Correlation Heatmap
    report += "### 9. 숫자형 특성간의 상관관계\n"
    corr = df[['Quantity', 'UnitPrice', 'TotalPrice']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('숫자형 특성 상관관계 히트맵')
    report += embed_plot_to_report()

    # 10. Scatter plot of UnitPrice vs Quantity
    report += "### 10. 단가와 수량의 관계\n"
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='UnitPrice', y='Quantity', data=df.sample(n=1000, random_state=42))
    plt.title('단가와 수량의 산점도')
    plt.xlabel('단가')
    plt.ylabel('수량')
    plt.xscale('log')
    plt.yscale('log')
    report += embed_plot_to_report()

    # --- DAU/MAU Analysis ---
    report += "## 5. User Activity Analysis (DAU/MAU)\n"
    
    # DAU
    df['InvoiceDay'] = df['InvoiceDate'].dt.date
    dau = df.groupby('InvoiceDay')['CustomerID'].nunique()
    report += "### 1. 일일 활성 사용자 (DAU)\n"
    report += f"<p>Average DAU: {dau.mean():.2f}</p>\n"
    
    # MAU
    mau = df.groupby('YearMonth')['CustomerID'].nunique()
    report += "### 2. 월간 활성 사용자 (MAU)\n"
    
    plt.figure(figsize=(12, 6))
    mau.plot(kind='bar')
    plt.title('월간 활성 사용자 (MAU)')
    plt.xlabel('월')
    plt.ylabel('고유 사용자 수')
    report += embed_plot_to_report()
    report += mau.to_frame().to_markdown() + "\n\n"

    # --- Time-Day Crosstab ---
    report += "### 11. 시간-요일별 히트맵\n"
    day_hour_pivot = df.pivot_table(index='DayOfWeek', columns='Hour', values='TotalPrice', aggfunc='sum')
    day_hour_pivot = day_hour_pivot.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    plt.figure(figsize=(18, 8))
    sns.heatmap(day_hour_pivot, cmap='viridis', annot=True, fmt=".0f")
    plt.title('시간-요일별 매출 히트맵')
    plt.xlabel('시간')
    plt.ylabel('요일')
    report += embed_plot_to_report()
    report += day_hour_pivot.to_markdown() + "\n\n"
    
    # --- Monthly Retention Analysis ---
    report += "### 12. 월단위 구매 고객 리텐션\n"
    
    def get_month(x): return dt.datetime(x.year, x.month, 1)
    df['InvoiceMonth'] = df['InvoiceDate'].apply(get_month)
    grouping = df.groupby('CustomerID')['InvoiceMonth']
    df['CohortMonth'] = grouping.transform('min')

    def get_date_int(df, column):
        year = df[column].dt.year
        month = df[column].dt.month
        day = df[column].dt.day
        return year, month, day

    invoice_year, invoice_month, _ = get_date_int(df, 'InvoiceMonth')
    cohort_year, cohort_month, _ = get_date_int(df, 'CohortMonth')

    years_diff = invoice_year - cohort_year
    months_diff = invoice_month - cohort_month
    df['CohortIndex'] = years_diff * 12 + months_diff + 1

    grouping = df.groupby(['CohortMonth', 'CohortIndex'])
    cohort_data = grouping['CustomerID'].apply(pd.Series.nunique)
    cohort_data = cohort_data.reset_index()
    cohort_counts = cohort_data.pivot_table(index='CohortMonth', columns='CohortIndex', values='CustomerID')
    
    cohort_sizes = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_sizes, axis=0)
    retention.rename(columns={1: 'Acquisition'}, inplace=True)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(retention, annot=True, fmt='.0%', cmap='viridis')
    plt.title('월간 리텐션율')
    plt.xlabel('코호트 인덱스')
    plt.ylabel('코호트 월')
    report += embed_plot_to_report()
    report += retention.to_markdown() + "\n\n"

    # Save the report to a markdown file
    with open('online-retail/streamlit_task.md', 'w', encoding='utf-8') as f:
        f.write(report)

def main():
    """Main function to run the EDA process."""
    df = load_data('online-retail/online_retail.csv')
    df_cleaned = clean_data(df.copy()) # Use a copy to keep original df intact
    generate_report(df_cleaned)

if __name__ == '__main__':
    main()