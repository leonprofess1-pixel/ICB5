import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import koreanize_matplotlib # Matplotlib에서 한글 폰트를 자동으로 설정합니다.

def main():
    """
    wage.csv 데이터셋에 대한 EDA를 수행하고, 결과물(통계 텍스트 파일, 시각화 이미지)을 저장합니다.
    """
    # --- 0. 설정 ---
    # 경로 정의
    data_path = 'FCIC/causal-inference/data/wage.csv'
    output_dir = 'FCIC/causal-inference/'
    image_dir = os.path.join(output_dir, 'images')

    # 이미지 및 결과 폴더 생성
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # 데이터 로드
    df = pd.read_csv(data_path)
    
    # 'logwage' 컬럼 생성 (wage가 0보다 큰 경우에만 로그 변환)
    df['logwage'] = np.log(df['wage'].loc[df['wage'] > 0])

    # --- 1. 기본적인 데이터 탐색 및 저장 ---
    with open(os.path.join(output_dir, 'df_info.txt'), 'w', encoding='utf-8') as f:
        df.info(buf=f)

    with open(os.path.join(output_dir, 'df_describe.txt'), 'w', encoding='utf-8') as f:
        f.write(df.describe().to_string())
        
    with open(os.path.join(output_dir, 'df_head.txt'), 'w', encoding='utf-8') as f:
        f.write(df.head().to_string())

    with open(os.path.join(output_dir, 'df_isnull.txt'), 'w', encoding='utf-8') as f:
        f.write(df.isnull().sum().to_string())

    # --- 2. 단변량 분석 시각화 ---

    # Plot 1: 임금 분포 (Histogram)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['wage'], kde=True, bins=30)
    plt.title('임금 분포 (Wage Distribution)')
    plt.xlabel('임금 (Wage)')
    plt.ylabel('빈도 (Frequency)')
    plt.grid(True)
    plt.savefig(os.path.join(image_dir, '1_wage_distribution.png'))
    plt.close()

    # Plot 2: 로그 변환 임금 분포 (Histogram)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['logwage'], kde=True, bins=30)
    plt.title('로그 변환 임금 분포 (Log Wage Distribution)')
    plt.xlabel('로그 임금 (Log Wage)')
    plt.ylabel('빈도 (Frequency)')
    plt.grid(True)
    plt.savefig(os.path.join(image_dir, '2_logwage_distribution.png'))
    plt.close()
    
    # Plot 3: 나이 분포 (Histogram)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['age'], kde=True, bins=25)
    plt.title('나이 분포 (Age Distribution)')
    plt.xlabel('나이 (Age)')
    plt.ylabel('빈도 (Frequency)')
    plt.grid(True)
    plt.savefig(os.path.join(image_dir, '3_age_distribution.png'))
    plt.close()

    # Plot 4: 교육 수준 분포 (Bar Chart)
    plt.figure(figsize=(12, 7))
    sns.countplot(data=df, y='educ', order=df['educ'].value_counts().index)
    plt.title('교육 수준(년수) 분포 (Education Years Distribution)')
    plt.xlabel('인원 수 (Count)')
    plt.ylabel('교육 수준(년수) (Education Years)')
    plt.grid(True, axis='x')
    plt.savefig(os.path.join(image_dir, '4_education_distribution.png'))
    plt.close()
    with open(os.path.join(output_dir, 'crosstab_education.txt'), 'w', encoding='utf-8') as f:
        f.write(pd.crosstab(index=df['educ'], columns='count').to_string())

    # Plot 5: 결혼 상태 분포 (Bar Chart)
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='married', order=df['married'].value_counts().index)
    plt.title('결혼 상태 분포 (Marital Status Distribution)')
    plt.xlabel('결혼 상태 (0=미혼, 1=기혼)')
    plt.ylabel('인원 수 (Count)')
    plt.grid(True, axis='y')
    plt.savefig(os.path.join(image_dir, '5_marital_distribution.png'))
    plt.close()
    with open(os.path.join(output_dir, 'crosstab_marital.txt'), 'w', encoding='utf-8') as f:
        f.write(pd.crosstab(index=df['married'], columns='count').to_string())

    # Plot 6: 인종(흑인) 분포 (Bar Chart)
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='black', order=df['black'].value_counts().index)
    plt.title('인종(흑인) 분포 (Race(Black) Distribution)')
    plt.xlabel('인종 (0=기타, 1=흑인)')
    plt.ylabel('인원 수 (Count)')
    plt.grid(True, axis='y')
    plt.savefig(os.path.join(image_dir, '6_race_distribution.png'))
    plt.close()
    with open(os.path.join(output_dir, 'crosstab_race.txt'), 'w', encoding='utf-8') as f:
        f.write(pd.crosstab(index=df['black'], columns='count').to_string())

    # Plot 7: 남부 지역 거주 분포 (Bar Chart)
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='south', order=df['south'].value_counts().index)
    plt.title('남부 지역 거주 분포 (South Region Distribution)')
    plt.xlabel('남부 지역 거주 여부 (0=아니오, 1=예)')
    plt.ylabel('인원 수 (Count)')
    plt.grid(True, axis='y')
    plt.savefig(os.path.join(image_dir, '7_south_distribution.png'))
    plt.close()
    with open(os.path.join(output_dir, 'crosstab_south.txt'), 'w', encoding='utf-8') as f:
        f.write(pd.crosstab(index=df['south'], columns='count').to_string())

    # --- 3. 이변량/다변량 분석 시각화 ---
    
    # Plot 8: 나이와 임금의 관계 (Scatter Plot with Regression Line)
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='age', y='wage', scatter_kws={'alpha':0.3}, line_kws={'color': 'red'})
    plt.title('나이와 임금의 관계 (Age vs. Wage)')
    plt.xlabel('나이 (Age)')
    plt.ylabel('임금 (Wage)')
    plt.grid(True)
    plt.savefig(os.path.join(image_dir, '8_age_vs_wage_scatter.png'))
    plt.close()
    
    # Plot 9: 교육 수준(년수)에 따른 임금 분포 (Box Plot)
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=df, x='educ', y='wage')
    plt.title('교육 수준(년수)에 따른 임금 분포 (Wage Distribution by Education Years)')
    plt.xlabel('교육 수준(년수) (Education Years)')
    plt.ylabel('임금 (Wage)')
    plt.grid(True, axis='y')
    plt.savefig(os.path.join(image_dir, '9_wage_by_education_boxplot.png'))
    plt.close()

    # Plot 10: IQ 점수와 임금의 관계 (Scatter Plot with Regression Line)
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='IQ', y='wage', scatter_kws={'alpha':0.3}, line_kws={'color': 'red'})
    plt.title('IQ와 임금의 관계 (IQ vs. Wage)')
    plt.xlabel('IQ 점수 (IQ Score)')
    plt.ylabel('임금 (Wage)')
    plt.grid(True)
    plt.savefig(os.path.join(image_dir, '10_iq_vs_wage_scatter.png'))
    plt.close()

    # Plot 11: 경력과 임금의 관계 (Scatter Plot with Regression Line)
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='exper', y='wage', scatter_kws={'alpha':0.3}, line_kws={'color': 'red'})
    plt.title('경력과 임금의 관계 (Experience vs. Wage)')
    plt.xlabel('경력(년수) (Experience in Years)')
    plt.ylabel('임금 (Wage)')
    plt.grid(True)
    plt.savefig(os.path.join(image_dir, '11_exper_vs_wage_scatter.png'))
    plt.close()

    # Plot 12: 상관관계 히트맵 (Correlation Heatmap)
    # 기술적으로 object 타입이지만 실제로는 범주형인 변수를 제외
    numeric_cols = df.select_dtypes(include=np.number).columns
    corr = df[numeric_cols].corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('수치형 변수 간 상관관계 (Correlation Matrix of Numeric Features)')
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, '12_correlation_heatmap.png'))
    plt.close()

    print(f"분석이 완료되었습니다. 총 12개의 그래프가 {image_dir}에 저장되었습니다.")
    print(f"통계 요약 파일들이 {output_dir}에 저장되었습니다.")

if __name__ == '__main__':
    main()