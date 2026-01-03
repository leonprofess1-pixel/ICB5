import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set Korean font for matplotlib
plt.rcParams['font.family'] = 'Malgun Gothic' # For Windows
plt.rcParams['axes.unicode_minus'] = False # To prevent breaking in minus sign

# Define paths
data_path = 'P2/data/price112.csv'
output_dir = 'P2'
images_dir = os.path.join(output_dir, 'images')
report_path = os.path.join(output_dir, 'eda_report.md')

# Create images directory if it doesn't exist
os.makedirs(images_dir, exist_ok=True)

# Load the dataset
try:
    df = pd.read_csv(data_path)
    print("데이터셋 로드 성공!")
    print("\n--- 데이터 정보 (df.info()) ---")
    df.info()
    print("\n--- 데이터 기술 통계량 (df.describe()) ---")
    print(df.describe().to_markdown(numalign="left", stralign="left"))
    print("\n--- 결측치 확인 (df.isnull().sum()) ---")
    print(df.isnull().sum().to_markdown(numalign="left", stralign="left"))
    print("\n--- 데이터 샘플 (df.head()) ---")
    print(df.head().to_markdown(numalign="left", stralign="left"))

    # 월별 데이터를 시계열 형태로 변환 (long format)
    # 날짜 관련 컬럼 식별
    date_columns = [col for col in df.columns if '/' in col]
    
    # id_vars는 그대로 유지하고 싶은 컬럼, value_vars는 melt할 컬럼
    df_long = df.melt(id_vars=['통계표', '계정항목', '단위', '가중치', '변환'],
                      value_vars=date_columns,
                      var_name='월',
                      value_name='물가지수')
    
    # '월' 컬럼을 datetime 객체로 변환 (YYYY/MM 형식)
    # 연도를 4자리로 통일하고 월만 추출하여 월의 마지막 날짜로 변환
    df_long['월'] = pd.to_datetime(df_long['월'], format='%Y/%m')
    
    # 변환된 데이터 정보 확인
    print("\n--- Long Format 데이터 정보 (df_long.info()) ---")
    df_long.info()
    print("\n--- Long Format 데이터 샘플 (df_long.head()) ---")
    # 시계열 분석: 전체 소비자물가지수('총지수')의 월별 추이 시각화
    total_cpi_df = df_long[df_long['계정항목'] == '총지수']
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=total_cpi_df, x='월', y='물가지수', hue='통계표')
    plt.title('전체 소비자물가지수 월별 추이 (총지수)')
    plt.xlabel('월')
    plt.ylabel('물가지수 (2020=100)')
    plt.grid(True)
    plt.tight_layout()
    # 시계열 분석: 주요 '계정항목'별 물가지수 추이 시각화
    # '총지수'를 제외한 계정항목의 가중치 합계를 기준으로 상위 10개 항목 선택
    weighted_avg_by_item = df_long[df_long['계정항목'] != '총지수'].groupby('계정항목')['가중치'].mean().nlargest(10).index
    
    top_items_df = df_long[df_long['계정항목'].isin(weighted_avg_by_item)]
    
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=top_items_df, x='월', y='물가지수', hue='계정항목', marker='o')
    plt.title('주요 계정항목별 물가지수 월별 추이 (상위 10개 항목)')
    plt.xlabel('월')
    plt.ylabel('물가지수 (2020=100)')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '2_top_10_items_monthly_trend.png'))
    plt.close()
    # 시계열 분석: 전월 대비 물가 상승률 계산 및 시각화
    # 각 계정항목별 전월 대비 물가지수 변화율 계산
    df_long['전월_물가지수'] = df_long.groupby('계정항목')['물가지수'].shift(1)
    df_long['물가상승률'] = ((df_long['물가지수'] - df_long['전월_물가지수']) / df_long['전월_물가지수']) * 100
    
    # '총지수'의 물가상승률 시각화
    total_cpi_inflation = df_long[df_long['계정항목'] == '총지수'].dropna(subset=['물가상승률'])
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=total_cpi_inflation, x='월', y='물가상승률', marker='o')
    plt.title('전체 소비자물가지수 전월 대비 물가상승률')
    plt.xlabel('월')
    plt.ylabel('물가상승률 (%)')
    plt.axhline(0, color='red', linestyle='--')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '3_total_cpi_inflation_rate.png'))
    plt.close()
    print(f"'{os.path.join(images_dir, '3_total_cpi_inflation_rate.png')}' 저장 완료.")

    # 상위 5개 계정항목의 물가상승률 시각화
    top_5_items_inflation = df_long[df_long['계정항목'].isin(weighted_avg_by_item[:5])].dropna(subset=['물가상승률'])

    plt.figure(figsize=(14, 8))
    sns.lineplot(data=top_5_items_inflation, x='월', y='물가상승률', hue='계정항목', marker='o')
    plt.title('주요 계정항목별 전월 대비 물가상승률 (상위 5개 항목)')
    plt.xlabel('월')
    plt.ylabel('물가상승률 (%)')
    plt.axhline(0, color='red', linestyle='--')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '4_top_5_items_inflation_rate.png'))
    plt.close()
    # 항목별 분석: '계정항목'별 평균 물가지수 및 변동성 분석
    item_stats = df_long[df_long['계정항목'] != '총지수'].groupby('계정항목')['물가지수'].agg(['mean', 'std']).sort_values(by='mean', ascending=False)
    
    # 평균 물가지수 상위 10개 항목 시각화
    plt.figure(figsize=(12, 7))
    sns.barplot(x=item_stats['mean'].head(10), y=item_stats.index[:10], palette='viridis')
    plt.title('계정항목별 평균 물가지수 (상위 10개)')
    plt.xlabel('평균 물가지수')
    plt.ylabel('계정항목')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '5_avg_price_index_by_item.png'))
    plt.close()
    print(f"'{os.path.join(images_dir, '5_avg_price_index_by_item.png')}' 저장 완료.")

    # 물가지수 변동성 (표준편차) 상위 10개 항목 시각화
    item_std_sorted = item_stats.sort_values(by='std', ascending=False)
    plt.figure(figsize=(12, 7))
    sns.barplot(x=item_std_sorted['std'].head(10), y=item_std_sorted.index[:10], palette='plasma')
    plt.title('계정항목별 물가지수 변동성 (표준편차 상위 10개)')
    plt.xlabel('물가지수 표준편차')
    plt.ylabel('계정항목')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '6_std_price_index_by_item.png'))
    plt.close()
    # 가중치 분석: 가중치 분포 시각화
    plt.figure(figsize=(10, 6))
    sns.histplot(df_long['가중치'], bins=30, kde=True)
    plt.title('계정항목별 가중치 분포')
    plt.xlabel('가중치')
    plt.ylabel('빈도')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '7_weight_distribution.png'))
    plt.close()
    print(f"'{os.path.join(images_dir, '7_weight_distribution.png')}' 저장 완료.")

    # '가중치'가 높은 상위 '계정항목' 분석 (재확인 및 시각화)
    # '총지수'를 제외한 계정항목의 평균 가중치를 기준으로 상위 10개 항목 선택
    # 이미 weighted_avg_by_item 변수에 저장되어 있으므로 이를 활용
    top_10_weighted_items = df_long[df_long['계정항목'] != '총지수'].groupby('계정항목')['가중치'].mean().nlargest(10)

    plt.figure(figsize=(12, 7))
    sns.barplot(x=top_10_weighted_items.values, y=top_10_weighted_items.index, palette='crest')
    plt.title('가중치가 높은 상위 10개 계정항목')
    plt.xlabel('평균 가중치')
    plt.ylabel('계정항목')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '8_top_10_weighted_items.png'))
    plt.close()
    print(f"'{os.path.join(images_dir, '8_top_10_weighted_items.png')}' 저장 완료.")




    print(f"'{os.path.join(images_dir, '8_top_10_weighted_items.png')}' 저장 완료.")

    # --- 군집 분석 (Cluster Analysis) ---
    # --- 군집 분석 (Cluster Analysis) ---
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    # from yellowbrick.cluster import KElbowVisualizer # yellowbrick 제거

    print("\n--- 군집 분석 시작 ---")

    # 군집 분석을 위한 데이터 준비
    # '총지수'를 제외하고 각 계정항목별 평균 물가지수, 표준편차, 평균 물가상승률 계산
    cluster_df = df_long[df_long['계정항목'] != '총지수'].groupby('계정항목').agg(
        mean_물가지수=('물가지수', 'mean'),
        std_물가지수=('물가지수', 'std'),
        mean_물가상승률=('물가상승률', 'mean')
    )

    # 결측치 처리 (물가상승률이나 표준편차 계산이 불가능한 항목 제외)
    # std가 0인 경우 NaN이 될 수 있으므로 0으로 채움
    cluster_df['std_물가지수'] = cluster_df['std_물가지수'].fillna(0)
    # 첫 달 물가상승률이 NaN인 경우 0으로 채움 (변동 없었다고 가정)
    cluster_df['mean_물가상승률'] = cluster_df['mean_물가상승률'].fillna(0)
    
    # 데이터셋에 NaN이 포함되어 있다면 제거 (groupby aggregation에서 발생할 수 있는 소수 항목)
    cluster_df = cluster_df.dropna()


    # 특성 스케일링
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(cluster_df)
    scaled_df = pd.DataFrame(scaled_features, columns=cluster_df.columns, index=cluster_df.index)

    # 최적의 K (군집 수) 결정 - Elbow Method (수동 구현)
    wcss = []
    for i in range(1, 11): # K를 1부터 10까지 시도
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
        kmeans.fit(scaled_df)
        wcss.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
    plt.title('엘보우 메소드 (WCSS)')
    plt.xlabel('군집 수 (K)')
    plt.ylabel('WCSS')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '9_elbow_method.png'))
    plt.close()
    print(f"'{os.path.join(images_dir, '9_elbow_method.png')}' 저장 완료.")

    # 엘보우 플롯을 보고 수동으로 최적 K 결정 (예: 4 또는 3)
    optimal_k = 4 
    print(f"엘보우 메소드 시각화 결과에 따라 임시 최적 K 값 {optimal_k}로 설정.")

    # K-Means 군집 분석 수행
    kmeans = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=300, n_init=10, random_state=42)
    cluster_df['cluster'] = kmeans.fit_predict(scaled_df)

    print("\n--- 군집별 특징 ---")
    # 스케일링된 데이터를 역변환하여 군집 중심점의 실제 값 확인
    cluster_centers = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), 
                                   columns=cluster_df.columns[:-1]) # 마지막 'cluster' 컬럼 제외
    cluster_centers['count'] = cluster_df['cluster'].value_counts().sort_index()
    print(cluster_centers.to_markdown(numalign="left", stralign="left"))

    # 군집 시각화 (산점도)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='mean_물가지수', y='std_물가지수', hue='cluster', data=cluster_df, palette='viridis', s=100, alpha=0.7)
    plt.title('군집 분석 결과: 평균 물가지수 vs 물가지수 표준편차')
    plt.xlabel('평균 물가지수')
    plt.ylabel('물가지수 표준편차')
    plt.legend(title='Cluster')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, '10_cluster_scatter.png'))
    plt.close()
    print(f"'{os.path.join(images_dir, '10_cluster_scatter.png')}' 저장 완료.")

    print("\n--- 군집 분석 완료 ---")

except FileNotFoundError:
    print(f"오류: {data_path} 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
except Exception as e:
    print(f"데이터 처리 중 오류 발생: {e}")
