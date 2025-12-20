import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
import warnings
import squarify

warnings.filterwarnings('ignore')

# 한글 폰트 설정
def setup_korean_font():
    """운영체제에 맞는 한글 폰트를 설정합니다."""
    font_list = fm.findSystemFonts()
    korean_font = None

    if os.name == 'posix':
        for font in font_list:
            if 'AppleSDGothicNeo' in font or 'NanumGothic' in font:
                korean_font = os.path.basename(font).split('.')[0]
                break
        if not korean_font:
             for font in font_list:
                if 'Malgun' in font:
                    korean_font = os.path.basename(font).split('.')[0]
                    break
    elif os.name == 'nt':
        for font in font_list:
            if 'malgun' in font.lower():
                korean_font = os.path.basename(font).split('.')[0]
                break
    
    if korean_font:
        plt.rcParams['font.family'] = korean_font
    else:
        print("경고: 적절한 한글 폰트를 찾지 못했습니다. 일부 텍스트가 깨져 보일 수 있습니다.")
    
    plt.rcParams['axes.unicode_minus'] = False

setup_korean_font()

# 데이터 로드
try:
    df = pd.read_csv('HR-employee-attrition_v2/HR-Employee-Attrition.csv')
except FileNotFoundError:
    print("오류: 'HR-employee-attrition_v2/HR-Employee-Attrition.csv' 파일을 찾을 수 없습니다.")
    exit()

# 결과 이미지 저장 디렉토리 생성
output_dir = 'HR-employee-attrition_v2/images_v3'
os.makedirs(output_dir, exist_ok=True)

# 고성과자 정의
high_performer_threshold = df['PerformanceRating'].quantile(0.75)
hp_df = df[df['PerformanceRating'] >= high_performer_threshold]

# 이직 여부 분리
hp_attrition_yes = hp_df[hp_df['Attrition'] == 'Yes']
hp_attrition_no = hp_df[hp_df['Attrition'] == 'No']

# --- 1. Clustered Bar Chart: 고성과자 직무 만족도 및 직급별 이직 현황 ---
plt.figure(figsize=(14, 8))
satisfaction_order = [1, 2, 3, 4]
job_level_order = sorted(hp_df['JobLevel'].unique())
x = np.arange(len(job_level_order))
width = 0.2

for i, s in enumerate(satisfaction_order):
    attrition_counts = []
    for level in job_level_order:
        count = len(hp_attrition_yes[(hp_attrition_yes['JobLevel'] == level) & (hp_attrition_yes['JobSatisfaction'] == s)])
        attrition_counts.append(count)
    plt.bar(x + (i - 1.5) * width, attrition_counts, width, label=f'만족도 {s}')

plt.xlabel('직급 (Job Level)', fontsize=12)
plt.ylabel('이직자 수', fontsize=12)
plt.title('고성과자 직급 및 직무 만족도별 이직자 수', fontsize=16)
plt.xticks(x, job_level_order)
plt.legend(title='직무 만족도')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '1_clustered_bar_satisfaction_joblevel.png'))
plt.close()

# --- 2. Stacked Bar Chart: 고성과자 직무별 이직자/잔류자 현황 ---
job_role_attrition = hp_df.groupby(['JobRole', 'Attrition']).size().unstack(fill_value=0)
job_role_attrition_sorted = job_role_attrition.sort_values('Yes', ascending=False)
job_role_attrition_sorted.plot(kind='barh', stacked=True, figsize=(12, 8), colormap='coolwarm_r')
plt.xlabel('직원 수', fontsize=12)
plt.ylabel('직무 (Job Role)', fontsize=12)
plt.title('고성과자 직무별 이직/잔류 현황', fontsize=16)
plt.legend(title='이직 여부', labels=['잔류', '이직'])
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '2_stacked_bar_jobrole_attrition.png'))
plt.close()

# --- 3. Box Plot: 고성과자 이직 여부에 따른 월 수입 분포 (직무별) ---
plt.figure(figsize=(18, 10))
sorted_roles = hp_attrition_yes.groupby('JobRole')['MonthlyIncome'].median().sort_values(ascending=False).index
data_to_plot = []
for role in sorted_roles:
    data_to_plot.append(hp_df[(hp_df['JobRole'] == role) & (hp_df['Attrition'] == 'Yes')]['MonthlyIncome'])
    data_to_plot.append(hp_df[(hp_df['JobRole'] == role) & (hp_df['Attrition'] == 'No')]['MonthlyIncome'])

bp = plt.boxplot(data_to_plot, patch_artist=True, vert=True)
plt.xlabel('직무 (Job Role)', fontsize=12)
plt.ylabel('월 수입 (Monthly Income)', fontsize=12)
plt.title('고성과자 직무별/이직여부에 따른 월 수입 분포', fontsize=16)
xtick_labels = [f'{role}\n(이직)' for role in sorted_roles] + [f'{role}\n(잔류)' for role in sorted_roles]
plt.xticks(np.arange(1, len(xtick_labels) + 1), [f'{role}\n({attr})' for role in sorted_roles for attr in ['이직', '잔류']], rotation=90)

colors = ['#ff9999', '#66b3ff'] * len(sorted_roles)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)

from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color='#ff9999', lw=4, label='이직'),
                   Line2D([0], [0], color='#66b3ff', lw=4, label='잔류')]
plt.legend(handles=legend_elements, title='이직 여부')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '3_boxplot_income_jobrole_attrition.png'))
plt.close()


# --- 4. Scatter Plot: 고성과자 근속년수 vs 월 수입 (이직 여부) ---
plt.figure(figsize=(12, 8))
plt.scatter(hp_attrition_no['YearsAtCompany'], hp_attrition_no['MonthlyIncome'], alpha=0.6, label='잔류', c='blue')
plt.scatter(hp_attrition_yes['YearsAtCompany'], hp_attrition_yes['MonthlyIncome'], alpha=0.8, label='이직', c='red', marker='x')
plt.xlabel('총 근속 년수 (Years At Company)', fontsize=12)
plt.ylabel('월 수입 (Monthly Income)', fontsize=12)
plt.title('고성과자 총 근속년수와 월 수입의 관계 (이직 여부별)', fontsize=16)
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '4_scatter_years_income_attrition.png'))
plt.close()

# --- 5. Donut Chart: 고성과 이직자의 초과근무 비율 ---
overtime_counts = hp_attrition_yes['OverTime'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(overtime_counts, labels=overtime_counts.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85, colors=['#ff6666', '#66b3ff'])
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('고성과 이직자의 초과근무 비율', fontsize=16)
plt.axis('equal')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '5_donut_overtime_attrition.png'))
plt.close()

# --- 6. Histogram: 고성과 이직자의 승진 후 경과 년수 분포 ---
plt.figure(figsize=(10, 6))
plt.hist(hp_attrition_yes['YearsSinceLastPromotion'], bins=15, color='purple', alpha=0.7)
plt.xlabel('마지막 승진 후 경과 년수', fontsize=12)
plt.ylabel('이직자 수', fontsize=12)
plt.title('고성과 이직자의 마지막 승진 후 경과 년수 분포', fontsize=16)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '6_histogram_promotion_attrition.png'))
plt.close()

# --- 7. Heatmap: 고성과 이직자 주요 수치 데이터 상관관계 ---
numeric_cols = hp_attrition_yes.select_dtypes(include=np.number).columns.tolist()
selected_cols = ['Age', 'DailyRate', 'MonthlyIncome', 'PercentSalaryHike', 'TotalWorkingYears', 
                 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
                 'JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance']
corr_matrix = hp_attrition_yes[selected_cols].corr()

fig, ax = plt.subplots(figsize=(12, 10))
im = ax.imshow(corr_matrix, cmap='coolwarm')
ax.set_xticks(np.arange(len(corr_matrix.columns)))
ax.set_yticks(np.arange(len(corr_matrix.columns)))
ax.set_xticklabels(corr_matrix.columns)
ax.set_yticklabels(corr_matrix.columns)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        text = ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                       ha="center", va="center", color="w")

ax.set_title("고성과 이직자 주요 수치 데이터 상관관계", fontsize=16)
fig.tight_layout()
plt.savefig(os.path.join(output_dir, '7_heatmap_correlation_attrition.png'))
plt.close()

# --- 8. Horizontal Bar Chart: 이직 여부에 따른 평균 급여 인상률 및 환경 만족도 ---
avg_metrics = hp_df.groupby('Attrition')[['PercentSalaryHike', 'EnvironmentSatisfaction']].mean()
fig, ax1 = plt.subplots(figsize=(10, 6))
avg_metrics['PercentSalaryHike'].plot(kind='barh', ax=ax1, color='skyblue', position=0, width=0.4)
ax1.set_xlabel('평균 급여 인상률 (%)', color='skyblue')
ax1.tick_params(axis='x', labelcolor='skyblue')
ax1.set_ylabel('이직 여부')
ax1.set_yticklabels(['잔류', '이직'])

ax2 = ax1.twiny()
avg_metrics['EnvironmentSatisfaction'].plot(kind='barh', ax=ax2, color='salmon', position=1, width=0.4)
ax2.set_xlabel('평균 업무 환경 만족도', color='salmon')
ax2.tick_params(axis='x', labelcolor='salmon')

plt.title('고성과자 이직 여부에 따른 평균 급여 인상률 및 환경 만족도', fontsize=15)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '8_hbar_salaryhike_satisfaction.png'))
plt.close()

# --- 9. Area Chart: 고성과자 연령대별 이직자 수 ---
age_bins = [18, 25, 35, 45, 55, 65]
age_labels = ['18-25', '26-35', '36-45', '46-55', '56-65']
hp_attrition_yes['AgeGroup'] = pd.cut(hp_attrition_yes['Age'], bins=age_bins, labels=age_labels, right=False)
age_attrition_counts = hp_attrition_yes['AgeGroup'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
age_attrition_counts.plot(kind='area', color='lightcoral', alpha=0.6)
plt.xlabel('연령대', fontsize=12)
plt.ylabel('이직자 수', fontsize=12)
plt.title('고성과자 연령대별 이직자 수', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '9_area_age_attrition.png'))
plt.close()

# --- 10. Treemap: 고성과 이직자 직무 분포 ---
job_role_counts = hp_attrition_yes['JobRole'].value_counts()
plt.figure(figsize=(12, 8))
colors = [plt.cm.Spectral(i/float(len(job_role_counts))) for i in range(len(job_role_counts))]
squarify.plot(sizes=job_role_counts.values, label=job_role_counts.index, alpha=.8, color=colors)
plt.title('고성과 이직자의 직무 분포', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '10_treemap_jobrole_attrition.png'))
plt.close()

print(f"분석이 완료되었습니다. 10개의 그래프가 '{output_dir}' 폴더에 저장되었습니다.")