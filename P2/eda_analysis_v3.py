import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

try:
    from wordcloud import WordCloud
except ImportError:
    print("WordCloud 라이브러리가 설치되어 있지 않습니다. 'pip install wordcloud'로 설치해주세요.")
    WordCloud = None
import matplotlib.cm as cm


# --- Configuration ---
plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

DATA_DIR = 'P2/data/raw'
IMAGE_DIR = 'P2/images_v2'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- Data Loading ---
def load_data():
    print("데이터셋을 로드합니다...")
    # 캐시된 데이터가 있는지 확인
    cache_path = os.path.join(DATA_DIR, 'processed', 'preprocessed_data.pkl')
    if os.path.exists(cache_path):
        print("캐시된 전처리 데이터를 로드합니다.")
        data = pd.read_pickle(cache_path)
        return data['dfs'], data['full_df'], data['orders'], data['merged_df']

    print("원본 데이터셋을 로드합니다...")
    dfs = {
        'customers': pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv')),
        'orders': pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv')),
        'items': pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv')),
        'payments': pd.read_csv(os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv')),
        'reviews': pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv')),
        'products': pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv')),
        'sellers': pd.read_csv(os.path.join(DATA_DIR, 'olist_sellers_dataset.csv')),
        'translation': pd.read_csv(os.path.join(DATA_DIR, 'product_category_name_translation.csv'))
    }
    full_df, orders, merged_df = preprocess_data(dfs)
    
    # 전처리된 데이터 캐시 저장
    processed_dir = os.path.join(DATA_DIR, 'processed')
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    pd.to_pickle({
        'dfs': dfs, 'full_df': full_df, 'orders': orders, 'merged_df': merged_df
    }, cache_path)
    
    return dfs, full_df, orders, merged_df


# --- Preprocessing ---
def preprocess_data(dfs):
    print("데이터를 전처리합니다...")
    orders = dfs['orders'].copy()
    items = dfs['items'].copy()
    products = dfs['products'].copy()
    translation = dfs['translation'].copy()
    sellers = dfs['sellers'].copy()
    customers = dfs['customers'].copy()
    reviews = dfs['reviews'].copy()
    payments = dfs['payments'].copy()
    
    # 1. Date Conversion
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 
                 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')
        
    # 2. Product Category Translation
    products = products.merge(translation, on='product_category_name', how='left')
    products['product_category_name_english'] = products['product_category_name_english'].fillna('unknown')
    
    # 3. Master DataFrame Creation
    df = orders.merge(items, on='order_id')
    df = df.merge(products, on='product_id')
    df = df.merge(sellers, on='seller_id')
    df = df.merge(customers, on='customer_id')
    df = df.merge(reviews, on='order_id')
    df = df.merge(payments, on='order_id')

    # 배송일 계산
    df['delivery_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
    
    # full_df, orders, merged_df 생성 (기존 스크립트 호환성 유지)
    # Note: 이 스크립트에서는 단일 'df'를 주로 사용합니다.
    full_df = df.copy() 
    merged_df = df.copy()

    return full_df, orders, merged_df

# --- 기존 분석 함수들 (생략) ---
# analyze_revenue_trend, analyze_delivery_performance 등 기존 함수들은 여기에 그대로 존재한다고 가정합니다.

# --- 신규 분석 함수 ---

def analyze_delivery_by_state_and_score(merged_df):
    """
    3개 변수 복합 분석: 배송 취약 지역별 배송 기간과 고객 평점의 관계 분석
    """
    print("신규 분석: 배송 취약 지역의 배송 기간 및 평점 관계를 분석합니다...")
    
    # 배송일이 30일 이상인 데이터를 이상치로 간주하고 필터링 (시각화 개선)
    df_filtered = merged_df[(merged_df['delivery_days'] >= 0) & (merged_df['delivery_days'] <= 60)]
    
    # 평균 배송일이 가장 긴 하위 5개 주 선정
    slowest_states = df_filtered.groupby('customer_state')['delivery_days'].mean().nlargest(5).index
    
    df_slowest = df_filtered[df_filtered['customer_state'].isin(slowest_states)]

    fig, axes = plt.subplots(1, 5, figsize=(20, 5), sharey=True)
    
    for i, state in enumerate(slowest_states):
        ax = axes[i]
        state_data = df_slowest[df_slowest['customer_state'] == state]
        
        # Boxplot으로 시각화
        data_to_plot = [state_data[state_data['review_score'] == s]['delivery_days'].dropna() for s in range(1, 6)]
        bp = ax.boxplot(data_to_plot, labels=[1, 2, 3, 4, 5], patch_artist=True, showfliers=False, widths=0.6)

        # 색상 커스터마이징
        colors = ['#FF6666', '#FFCC66', '#FFFF66', '#CCFF66', '#66FF66']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            
        ax.set_title(f'State: {state}', fontsize=14)
        ax.set_xlabel('Review Score')
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    axes[0].set_ylabel('Delivery Time (Days)')
    plt.suptitle('배송 취약 5개 주의 평점별 배송 기간 분포', fontsize=18)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(IMAGE_DIR, '18_delivery_review_by_slow_states.png'))
    plt.close()


def analyze_customer_clustering(merged_df):
    """
    고객 군집 분석 (RFM과 유사한 접근)
    - Recency: 최근 주문일 (분석 시점 기준)
    - Frequency: 주문 횟수
    - Monetary: 총 지출액
    - + Avg Review Score 추가
    """
    print("신규 분석: 고객 군집 분석을 수행합니다...")

    # 고객별 데이터 집계
    customer_df = merged_df.groupby('customer_unique_id').agg(
        total_spend=('payment_value', 'sum'),
        order_count=('order_id', 'nunique'),
        avg_review_score=('review_score', 'mean'),
        last_order_date=('order_purchase_timestamp', 'max')
    ).dropna()

    # Recency 계산
    analysis_date = merged_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    customer_df['recency'] = (analysis_date - customer_df['last_order_date']).dt.days

    # 군집 분석에 사용할 특성 선택
    features = customer_df[['total_spend', 'order_count', 'avg_review_score', 'recency']]
    
    # 이상치 제거 (상위 1% 제거)
    for col in features.columns:
        q_99 = features[col].quantile(0.99)
        features = features[features[col] < q_99]

    # 데이터 스케일링
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # K-Means 군집 분석 (4개 군집으로)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    customer_df_clustered = features.copy()
    customer_df_clustered['cluster'] = kmeans.fit_predict(scaled_features)

    # PCA를 통한 시각화
    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(scaled_features)
    customer_df_clustered['pca1'] = pca_features[:, 0]
    customer_df_clustered['pca2'] = pca_features[:, 1]
    
    # 시각화
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(customer_df_clustered['pca1'], customer_df_clustered['pca2'], 
                          c=customer_df_clustered['cluster'], cmap='viridis', alpha=0.6)
    plt.title('고객 군집 분석 (PCA)', fontsize=16)
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend(handles=scatter.legend_elements()[0], labels=['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3'], title="Clusters")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(IMAGE_DIR, '19_customer_clusters.png'))
    plt.close()

    # 군집별 특성 분석
    cluster_summary = customer_df_clustered.groupby('cluster').agg({
        'total_spend': ['mean', 'count'],
        'order_count': 'mean',
        'avg_review_score': 'mean',
        'recency': 'mean'
    })
    print("\n--- 고객 군집별 특성 ---")
    print(cluster_summary)
    return cluster_summary

# --- Main Execution ---
def main():
    # 데이터 로드 및 전처리
    dfs, full_df, orders, merged_df = load_data()
    
    # --- 여기에 기존 분석 함수들을 호출할 수 있습니다 ---
    # 예: analyze_revenue_trend(full_df)
    
    # --- 신규 분석 실행 ---
    analyze_delivery_by_state_and_score(merged_df)
    cluster_summary = analyze_customer_clustering(merged_df)

    print("\n신규 분석이 완료되었습니다. 2개의 새로운 이미지가 P2/images_v2에 저장되었습니다.")
    print("군집 분석 결과는 보고서 생성에 활용됩니다.")


if __name__ == "__main__":
    main()
