import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create directory for images if it doesn't exist
output_dir = 'HR-employee-attrition_v2/images_v3'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- 1. 데이터 로드 및 전처리 ---
# 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
try:
    df = pd.read_csv('HR-Employee-Attrition.csv')
except FileNotFoundError:
    print("오류: 'HR-Employee-Attrition.csv' 파일을 찾을 수 없습니다. 현재 디렉토리에 파일이 있는지 확인해주세요.")
    exit()

# 고성과자 정의 (PerformanceRating == 4)
# PerformanceRating 분포 확인
# print(df['PerformanceRating'].value_counts())
high_performers = df[df['PerformanceRating'] == 4].copy()
high_performers_attrition_yes = high_performers[high_performers['Attrition'] == 'Yes'].copy()

# --- 2. 시각화 (10종) ---

# Plot 1: Clustered Bar Chart - 직무 레벨과 환경 만족도에 따른 이탈 현황
# 데이터 집계
df_agg = high_performers.groupby(['JobLevel', 'EnvironmentSatisfaction', 'Attrition']).size().unstack(fill_value=0)
if 'Yes' not in df_agg.columns: df_agg['Yes'] = 0
if 'No' not in df_agg.columns: df_agg['No'] = 0
df_agg['Total'] = df_agg['Yes'] + df_agg['No']
df_agg['AttritionRate'] = df_agg['Yes'] / df_agg['Total']
df_agg = df_agg.reset_index()

# 시각화
plt.figure(figsize=(14, 8))
# Using seaborn for ease of creating a clustered bar chart, but without applying its style
import seaborn as sns
sns.set_style("whitegrid", {'axes.grid' : False}) # no seaborn style
sns.barplot(x='JobLevel', y='AttritionRate', hue='EnvironmentSatisfaction', data=df_agg, palette='viridis')
plt.title('고성과자 직무 레벨 및 환경 만족도별 이탈률', fontsize=16)
plt.xlabel('직무 레벨', fontsize=12)
plt.ylabel('이탈률', fontsize=12)
plt.legend(title='환경 만족도')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(f'{output_dir}/1_clustered_bar_satisfaction_joblevel.png')
plt.close()


# Plot 2: Stacked Bar Chart - 직무에 따른 이탈 현황
job_role_attrition = high_performers.groupby(['JobRole', 'Attrition']).size().unstack(fill_value=0)
job_role_attrition_ratio = job_role_attrition.div(job_role_attrition.sum(axis=1), axis=0)
job_role_attrition_ratio.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='coolwarm')
plt.title('고성과자 직무별 이탈 비율', fontsize=16)
plt.xlabel('직무', fontsize=12)
plt.ylabel('비율', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='이탈 여부')
plt.tight_layout()
plt.savefig(f'{output_dir}/2_stacked_bar_jobrole_attrition.png')
plt.close()

# Plot 3: Box Plot - 직무별 월급 분포 (이탈 여부로 구분)
plt.figure(figsize=(14, 8))
sns.boxplot(x='JobRole', y='MonthlyIncome', hue='Attrition', data=high_performers, palette="pastel")
plt.title('고성과자 직무별 월급 분포 (이탈 여부별)', fontsize=16)
plt.xlabel('직무', fontsize=12)
plt.ylabel('월급', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/3_boxplot_income_jobrole_attrition.png')
plt.close()


# Plot 4: Scatter Plot - 총 근무 연수와 월급 (이탈 여부로 구분)
plt.figure(figsize=(10, 7))
sns.scatterplot(data=high_performers, x='TotalWorkingYears', y='MonthlyIncome', hue='Attrition', alpha=0.7, palette=['#488f31', '#de425b'])
plt.title('고성과자의 총 근무 연수와 월급 (이탈 여부별)', fontsize=16)
plt.xlabel('총 근무 연수', fontsize=12)
plt.ylabel('월급', fontsize=12)
plt.legend(title='이탈 여부')
plt.grid(True)
plt.savefig(f'{output_dir}/4_scatter_years_income_attrition.png')
plt.close()

# Plot 5: Donut Chart - 초과근무 여부에 따른 이탈 비율
overtime_counts = high_performers_attrition_yes['OverTime'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(overtime_counts, labels=overtime_counts.index, autopct='%1.1f%%', startangle=90, pctdistance=0.85, colors=['lightcoral', 'skyblue'], wedgeprops=dict(width=0.3))
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('이탈한 고성과자들의 초과근무 비율', fontsize=16)
plt.ylabel('')
plt.savefig(f'{output_dir}/5_donut_overtime_attrition.png')
plt.close()


# Plot 6: Histogram - 승진까지의 기간 분포 (이탈 여부로 구분)
plt.figure(figsize=(10, 7))
sns.histplot(data=high_performers, x='YearsSinceLastPromotion', hue='Attrition', multiple='stack', kde=True, palette='BuGn')
plt.title('고성과자 승진 소요 기간 분포 (이탈 여부별)', fontsize=16)
plt.xlabel('마지막 승진 후 기간 (년)', fontsize=12)
plt.ylabel('인원수', fontsize=12)
plt.savefig(f'{output_dir}/6_histogram_promotion_attrition.png')
plt.close()

# Plot 7: Heatmap - 숫자형 변수 간 상관관계 (이탈한 고성과자)
numeric_cols = high_performers_attrition_yes.select_dtypes(include=np.number).columns
# 변수 너무 많으면 보기 힘드므로 일부 선택
selected_cols = ['Age', 'MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'YearsSinceLastPromotion', 'PercentSalaryHike', 'JobLevel', 'JobSatisfaction', 'EnvironmentSatisfaction']
corr_matrix = high_performers_attrition_yes[selected_cols].corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('이탈한 고성과자들의 주요 변수 간 상관관계', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(f'{output_dir}/7_heatmap_correlation_attrition.png')
plt.close()

# Plot 8: Horizontal Bar Chart - 급여 인상률과 직무 만족도
plt.figure(figsize=(12, 8))
sns.barplot(x="PercentSalaryHike", y="JobSatisfaction", hue="Attrition", data=high_performers, orient='h', palette='husl')
plt.title('고성과자의 급여 인상률과 직무 만족도별 이탈 현황', fontsize=16)
plt.xlabel('평균 급여 인상률 (%)', fontsize=12)
plt.ylabel('직무 만족도', fontsize=12)
plt.legend(title='이탈 여부', loc='lower right')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.savefig(f'{output_dir}/8_hbar_salaryhike_satisfaction.png')
plt.close()

# Plot 9: Area Chart - 연령대별 누적 이탈자 수
age_attrition = high_performers_attrition_yes.groupby('Age').size().reset_index(name='count')
plt.figure(figsize=(12, 7))
plt.fill_between(age_attrition['Age'], age_attrition['count'], color="skyblue", alpha=0.4)
plt.plot(age_attrition['Age'], age_attrition['count'], color="Slateblue", alpha=0.6, linewidth=2)
plt.title('고성과자 연령대별 이탈자 수', fontsize=16)
plt.xlabel('연령', fontsize=12)
plt.ylabel('이탈자 수', fontsize=12)
plt.grid(True)
plt.savefig(f'{output_dir}/9_area_age_attrition.png')
plt.close()

# Plot 10: Treemap (using matplotlib bar chart as a substitute) - 이탈 고성과자 직무 분포
job_role_counts = high_performers_attrition_yes['JobRole'].value_counts()
plt.figure(figsize=(12, 8))
# Using a simple bar chart as a substitute for treemap
job_role_counts.plot(kind='bar', color=plt.cm.viridis(np.linspace(0, 1, len(job_role_counts))))
plt.title('이탈한 고성과자들의 직무 분포 (Treemap 대체)', fontsize=16)
plt.xlabel('직무', fontsize=12)
plt.ylabel('이탈자 수', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/10_treemap_jobrole_attrition.png')
plt.close()


print(f"분석 그래프가 {output_dir} 폴더에 10개 저장되었습니다.")