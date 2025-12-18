
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt

# eda.py의 데이터 로딩 및 정제 함수 재사용
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

# 데이터 로딩 및 캐싱
@st.cache_data
def load_and_clean_data():
    df = load_data('online-retail/online_retail.csv')
    df_cleaned = clean_data(df.copy())
    return df_cleaned

df = load_and_clean_data()

# --- 사이드바 ---
st.sidebar.title("Online Retail EDA Dashboard")

# 국가 선택
if 'Country' not in df.columns:
    st.error("Dataset must contain a 'Country' column.")
    st.stop()

unique_countries = df['Country'].unique()
selected_countries = st.sidebar.multiselect(
    '국가 선택',
    options=unique_countries,
    default=['United Kingdom', 'Germany', 'France', 'EIRE'] if 'United Kingdom' in unique_countries else []
)

# 날짜 범위 선택
min_date = df['InvoiceDate'].min().date()
max_date = df['InvoiceDate'].max().date()
date_range = st.sidebar.slider(
    "날짜 범위 선택",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# 선택된 값으로 데이터 필터링. SettingWithCopyWarning을 피하기 위해 .copy() 사용
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['InvoiceDate'].dt.date >= date_range[0]) &
    (df['InvoiceDate'].dt.date <= date_range[1])
].copy()


# --- 메인 화면 ---
st.title("Online Retail 데이터 분석 대시보드")

tab1, tab2, tab3, tab4 = st.tabs(["데이터 개요", "매출 분석", "고객 및 상품 분석", "사용자 활동 분석"])

with tab1:
    st.header("데이터 개요")
    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        # 데이터 검색
        st.subheader("데이터 검색")
        search_term = st.text_input("상품 설명으로 검색:", "")
        if search_term:
            search_result_df = filtered_df[filtered_df['Description'].str.contains(search_term, case=False, na=False)]
            st.dataframe(search_result_df)
        else:
            st.dataframe(filtered_df.head(10))

        # 데이터 크기
        st.metric("필터링된 데이터 수", f"{filtered_df.shape[0]:,} 개")
        st.metric("전체 컬럼 수", f"{filtered_df.shape[1]:,} 개")

with tab2:
    st.header("매출 분석")
    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        # 월별 매출 추이
        st.subheader("월별 매출 추이")
        filtered_df['YearMonth'] = filtered_df['InvoiceDate'].dt.to_period('M')
        monthly_sales = filtered_df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
        monthly_sales['YearMonth'] = monthly_sales['YearMonth'].dt.to_timestamp()
        fig_monthly = px.line(monthly_sales, x='YearMonth', y='TotalPrice', title='월별 총 매출')
        st.plotly_chart(fig_monthly)

        # 요일별 매출
        st.subheader("요일별 매출")
        filtered_df['DayOfWeek'] = filtered_df['InvoiceDate'].dt.day_name()
        daily_sales = filtered_df.groupby('DayOfWeek')['TotalPrice'].sum().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()
        fig_daily = px.bar(daily_sales, x='DayOfWeek', y='TotalPrice', title='요일별 총 매출')
        st.plotly_chart(fig_daily)

        # 시간-요일별 히트맵
        st.subheader("시간-요일별 매출 히트맵")
        filtered_df['Hour'] = filtered_df['InvoiceDate'].dt.hour
        day_hour_pivot = filtered_df.pivot_table(index='DayOfWeek', columns='Hour', values='TotalPrice', aggfunc='sum').reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        fig_heatmap = px.imshow(day_hour_pivot, title='시간-요일별 매출 히트맵', labels=dict(x="시간", y="요일", color="총 매출"))
        st.plotly_chart(fig_heatmap)

with tab3:
    st.header("고객 및 상품 분석")
    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        # 매출 상위 10개국
        st.subheader("매출 상위 10개국")
        top_10_countries = filtered_df.groupby('Country')['TotalPrice'].sum().nlargest(10).reset_index()
        fig_country_bar = px.bar(top_10_countries, y='Country', x='TotalPrice', orientation='h', title='매출 상위 10개국').update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_country_bar)

        country_sales = filtered_df.groupby('Country')['TotalPrice'].sum().reset_index()
        fig_country_map = px.choropleth(country_sales, locations='Country', locationmode='country names', color='TotalPrice', hover_name='Country', color_continuous_scale=px.colors.sequential.Plasma, title='국가별 매출 분포')
        st.plotly_chart(fig_country_map)

        # 판매량 상위 10개 상품
        st.subheader("판매량 상위 10개 상품")
        top_10_products = filtered_df.groupby('Description')['Quantity'].sum().nlargest(10).reset_index()
        fig_product_bar = px.bar(top_10_products, y='Description', x='Quantity', orientation='h', title='판매량 상위 10개 상품').update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_product_bar)

        # 단가와 수량의 관계
        st.subheader("단가와 수량의 관계")
        scatter_sample = filtered_df.sample(n=min(1000, len(filtered_df)), random_state=42)
        fig_scatter = px.scatter(scatter_sample, x="UnitPrice", y="Quantity", title="단가와 수량의 산점도", log_x=True, log_y=True)
        st.plotly_chart(fig_scatter)

with tab4:
    st.header("사용자 활동 분석")
    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        # 월간 활성 사용자 (MAU)
        st.subheader("월간 활성 사용자 (MAU)")
        filtered_df['YearMonth'] = filtered_df['InvoiceDate'].dt.to_period('M')
        mau = filtered_df.groupby('YearMonth')['CustomerID'].nunique().reset_index()
        mau['YearMonth'] = mau['YearMonth'].dt.to_timestamp()
        fig_mau = px.bar(mau, x='YearMonth', y='CustomerID', title='월간 활성 사용자 (MAU)')
        st.plotly_chart(fig_mau)
        
        # 월별 고객 리텐션
        st.subheader("월별 고객 리텐션")
        
        retention_df = filtered_df.copy()
        
        def get_month(x): return dt.datetime(x.year, x.month, 1)
        retention_df['InvoiceMonth'] = retention_df['InvoiceDate'].apply(get_month)
        grouping = retention_df.groupby('CustomerID')['InvoiceMonth']
        retention_df['CohortMonth'] = grouping.transform('min')

        def get_date_int(df, column):
            year = df[column].dt.year
            month = df[column].dt.month
            return year, month

        invoice_year, invoice_month = get_date_int(retention_df, 'InvoiceMonth')
        cohort_year, cohort_month = get_date_int(retention_df, 'CohortMonth')

        years_diff = invoice_year - cohort_year
        months_diff = invoice_month - cohort_month
        retention_df['CohortIndex'] = years_diff * 12 + months_diff + 1

        grouping = retention_df.groupby(['CohortMonth', 'CohortIndex'])
        cohort_data = grouping['CustomerID'].apply(pd.Series.nunique).reset_index()
        cohort_counts = cohort_data.pivot_table(index='CohortMonth', columns='CohortIndex', values='CustomerID')
        
        if not cohort_counts.empty:
            cohort_sizes = cohort_counts.iloc[:, 0]
            retention = cohort_counts.divide(cohort_sizes, axis=0)
            retention.index = retention.index.strftime('%Y-%m')

            fig_retention = px.imshow(retention, text_auto=".0%", title='월간 리텐션율', labels=dict(x="코호트 인덱스", y="코호트 월", color="리텐션"))
            st.plotly_chart(fig_retention)
        else:
            st.warning("리텐션 데이터를 계산하기에 충분한 데이터가 없습니다.")

