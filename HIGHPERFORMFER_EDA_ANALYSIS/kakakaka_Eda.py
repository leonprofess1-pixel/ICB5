
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 한국어 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def analyze_high_performers(data_path='../HR-Employee-Attrition.csv', output_dir='.'):
    """
    고성과자 이탈 요인 분석 함수
    kakakaka.html의 분석 로직을 재현하고, 시각화 결과를 저장합니다.
    """
    # --- 1. 데이터 로드 및 전처리 ---
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"오류: 데이터 파일을 찾을 수 없습니다. 경로를 확인하세요: {data_path}")
        return

    # 고성과자 (PerformanceRating == 4) 필터링
    hp_df = df[df['PerformanceRating'] == 4].copy()
    print(f"--- 전체 직원: {len(df)}명 | 고성과자(평점 4점): {len(hp_df)}명 ---")

    # 이탈률 계산
    total_hp = len(hp_df)
    attrition_count = hp_df['Attrition'].value_counts()['Yes']
    attrition_rate = (attrition_count / total_hp) * 100
    print(f"고성과자 이탈률: {attrition_rate:.1f}% ({attrition_count}명 / {total_hp}명)\n")


    # --- 2. JSG (직무 스트레스 그룹) 분석 ---
    print("--- 01. JSG (직무 스트레스 그룹) 분석 ---")
    
    # JSG 파생변수 생성: 만족도(JobSatisfaction <= 2 -> LowSat)와 초과근무(OverTime) 조합
    hp_df['JSG'] = np.where(hp_df['JobSatisfaction'] <= 2, 'LowSat', 'HighSat') + '_' + np.where(hp_df['OverTime'] == 'Yes', 'OT', 'NoOT')

    # 그룹별 이탈률 계산
    jsg_attrition = hp_df.groupby('JSG')['Attrition'].value_counts(normalize=True).unstack().fillna(0)
    jsg_attrition['Attrition_Rate(%)'] = jsg_attrition['Yes'] * 100
    
    print("그룹별 이탈률:")
    print(jsg_attrition[['Attrition_Rate(%)']].sort_values(by='Attrition_Rate(%)', ascending=False))
    print("-> '만족도 낮음 & 초과근무 있음' 그룹의 이탈률이 압도적으로 높음을 확인.\n")


    # --- 3. CSI (경력 정체 지수) 심층 진단 ---
    print("--- 02. CSI (경력 정체 지수) 심층 진단 ---")
    
    # CSI 변수 (YearsSinceLastPromotion)
    hp_df['CSI'] = hp_df['YearsSinceLastPromotion']
    
    # 이탈자/재직자 간 CSI 비교
    csi_comparison = hp_df.groupby('Attrition')['CSI'].agg(['mean', 'median', 'std'])
    print("이탈 여부에 따른 CSI(승진 정체 기간) 비교:")
    print(csi_comparison)
    print("-> 이탈자 그룹의 평균 CSI가 재직자보다 현저히 높음 (성장 정체 시사).\n")
    

    # --- 4. K-means 군집 분석 (TRP & CSI 기반) ---
    print("--- 03. 전략적 군집 현황 (K-means Clustering) ---")

    # TRP(총 보상 인식) 파생변수 생성
    # PercentSalaryHike(11~25), StockOptionLevel(0~3)을 정규화하여 합산
    max_hike = df['PercentSalaryHike'].max()
    min_hike = df['PercentSalaryHike'].min()
    max_stock = df['StockOptionLevel'].max()
    
    hp_df['TRP'] = ((hp_df['PercentSalaryHike'] - min_hike) / (max_hike - min_hike)) + \
                   (hp_df['StockOptionLevel'] / max_stock)
    
    # K-means 모델 생성 및 학습
    features = hp_df[['CSI', 'TRP']].copy()
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    hp_df['Cluster'] = kmeans.fit_predict(features)
    
    # 군집별 특성 확인
    cluster_summary = hp_df.groupby('Cluster')[['CSI', 'TRP', 'MonthlyIncome']].mean()
    cluster_summary['Count'] = hp_df['Cluster'].value_counts()
    # 각 클러스터의 이탈률 계산
    cluster_attrition = hp_df.groupby('Cluster')['Attrition'].value_counts(normalize=True).unstack().fillna(0)
    cluster_summary['Attrition_Rate(%)'] = cluster_attrition['Yes'] * 100
    
    print("군집별 특성 및 이탈률:")
    print(cluster_summary.sort_values(by='CSI', ascending=False))
    print("-> CSI가 높고 TRP가 낮은 군집에서 이탈률이 높은 경향성을 파악할 수 있음.\n")

    # --- 5. 시각화 및 저장 ---
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # 군집 분석 시각화 (Scatter Plot)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=hp_df, x='CSI', y='TRP', hue='Cluster', palette='viridis', s=100, alpha=0.8)
    
    # 각 군집의 중심점 표시
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=250, marker='*', label='군집 중심')

    plt.title('전략적 군집 분석 (CSI vs TRP)', fontsize=16)
    plt.xlabel('CSI (경력 정체 지수, Year)', fontsize=12)
    plt.ylabel('TRP (총 보상 인식, Normalized)', fontsize=12)
    plt.legend(title='Cluster')
    plt.grid(True)
    
    # 시각화 결과 저장
    plot_path = os.path.join(output_dir, 'cluster_analysis.png')
    plt.savefig(plot_path)
    print(f"군집 분석 시각화 결과가 '{plot_path}'에 저장되었습니다.")
    plt.close()


if __name__ == '__main__':
    # 스크립트를 프로젝트 루트에서 실행한다고 가정합니다.
    # 데이터셋 경로는 'HR-Employee-Attrition.csv'
    # 결과물(이미지)은 스크립트가 있는 폴더에 저장
    analyze_high_performers(
        data_path='HR-Employee-Attrition.csv',
        output_dir='./HIGHPERFORMFER_EDA_ANALYSIS'
    )
