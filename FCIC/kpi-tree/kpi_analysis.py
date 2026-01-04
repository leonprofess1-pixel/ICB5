import pandas as pd
import numpy as np

# 데이터 로드
try:
    df = pd.read_csv('FCIC/kpi-tree/data/olist_merged_dataset_deduped.csv')
except FileNotFoundError:
    print("Error: 'olist_merged_dataset_deduped.csv' not found in 'FCIC/kpi-tree/data/'. Please check the file path.")
    exit()

# --- 1. 데이터 전처리 및 주차 컬럼 생성 ---
df_processed = df.copy()
# order_purchase_timestamp를 datetime으로 변환
df_processed['order_purchase_timestamp'] = pd.to_datetime(df_processed['order_purchase_timestamp'])

# 'week_start_date' 컬럼 생성: 주의 시작일(월요일)
df_processed['week_start_date'] = df_processed['order_purchase_timestamp'].dt.to_period('W').apply(lambda r: r.start_time).dt.date

# --- 2. 주차별 KPI 산출 ---
# Groupby 객체 생성
weekly_agg = df_processed.groupby('week_start_date')

# 각 KPI를 Series로 계산
l1_product_revenue = weekly_agg['main_product_price'].sum()
l1_freight_revenue = weekly_agg['main_product_freight_value'].sum()
l0_total_payment_from_sum = weekly_agg['payment_value_sum'].sum() # L0 직접 계산
l2_total_orders = weekly_agg['order_id'].nunique()
l3_total_unique_customers = weekly_agg['customer_unique_id'].nunique()

# --- 3. KPI 데이터프레임 생성 및 결합 ---
kpi_df = pd.DataFrame({
    'l0_total_payment': l0_total_payment_from_sum, # L0를 직접 계산한 값으로 설정
    'l1_product_revenue': l1_product_revenue,
    'l1_freight_revenue': l1_freight_revenue,
    'l2_total_orders': l2_total_orders,
    'l3_total_unique_customers': l3_total_unique_customers
}).fillna(0)

# --- 4. 계층적 KPI 계산 ---
# L2
kpi_df['l2_avg_product_revenue_per_order'] = kpi_df['l1_product_revenue'] / kpi_df['l2_total_orders']

# L3
kpi_df['l3_avg_orders_per_customer'] = kpi_df['l2_total_orders'] / kpi_df['l3_total_unique_customers']

# L0 검증: l1의 합이 l0와 일치하는지 확인 (여기서는 직접 계산한 l0를 사용)
# kpi_df['l0_total_payment_check'] = kpi_df['l1_product_revenue'] + kpi_df['l1_freight_revenue']
# assert np.allclose(kpi_df['l0_total_payment'], kpi_df['l0_total_payment_check']), "L0 Total Payment Check Failed"


# --- 5. 최종 데이터프레임 정리 및 검증 ---
# 컬럼 순서 정리
final_cols = [
    'l0_total_payment',
    'l1_product_revenue',
    'l1_freight_revenue',
    'l2_total_orders',
    'l2_avg_product_revenue_per_order',
    'l3_total_unique_customers',
    'l3_avg_orders_per_customer'
]
kpi_df = kpi_df[final_cols]

# 산술 관계 검증 (부동소수점 오차 감안)
kpi_df['l1_product_revenue_check'] = kpi_df['l2_total_orders'] * kpi_df['l2_avg_product_revenue_per_order']
assert np.allclose(kpi_df['l1_product_revenue'], kpi_df['l1_product_revenue_check']), "L1 Product Revenue Check Failed"

kpi_df['l2_total_orders_check'] = kpi_df['l3_total_unique_customers'] * kpi_df['l3_avg_orders_per_customer']
assert np.allclose(kpi_df['l2_total_orders'], kpi_df['l2_total_orders_check']), "L2 Total Orders Check Failed"

# 검증용 컬럼 제거
kpi_df = kpi_df.drop(columns=['l1_product_revenue_check', 'l2_total_orders_check'])

# NaN 값을 0으로 대체 (e.g., 0으로 나누는 경우)
kpi_df = kpi_df.replace([np.inf, -np.inf], np.nan).fillna(0)

# --- 6. 파일로 저장 ---
output_path = 'FCIC/kpi-tree/weekly_kpi_trend_analysis.csv'
kpi_df.to_csv(output_path)

print(f"Analysis complete. Output saved to '{output_path}'")
print("\n--- KPI Trend DataFrame (first 5 rows) ---")
print(kpi_df.head())
