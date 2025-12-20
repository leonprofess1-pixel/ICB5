
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def main():
    # 데이터 로드
    file_path = './HR-employee-attrition_v2/HR-Employee-Attrition.csv'
    df = pd.read_csv(file_path)

    # 이미지 저장 폴더 생성
    image_folder = './HR-employee-attrition_v2/images'
    os.makedirs(image_folder, exist_ok=True)

    # --- 1. 근속 연수별 퇴사자/비퇴사자 누적 분포 (Stacked Area Chart) ---
    attrition_by_years = df.groupby(['TotalWorkingYears', 'Attrition']).size().unstack(fill_value=0)
    cumulative_attrition = attrition_by_years.cumsum()

    plt.figure(figsize=(12, 7))
    plt.stackplot(cumulative_attrition.index, 
                  cumulative_attrition['No'], cumulative_attrition['Yes'], 
                  labels=['비퇴사', '퇴사'], 
                  colors=['skyblue', 'salmon'])
    plt.title('총 근무 연수별 누적 직원 수 (퇴사 여부별)', fontsize=16)
    plt.xlabel('총 근무 연수 (Total Working Years)', fontsize=12)
    plt.ylabel('누적 직원 수', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(image_folder, '1_working_years_stacked_area.png'))
    plt.close()

    # --- 2. 월 소득과 총 근무 연수 (Scatter Plot) ---
    plt.figure(figsize=(10, 6))
    for attrition_status in df['Attrition'].unique():
        subset = df[df['Attrition'] == attrition_status]
        plt.scatter(subset['TotalWorkingYears'], subset['MonthlyIncome'], alpha=0.6, label=f'퇴사: {attrition_status}')
    plt.title('월 소득과 총 근무 연수의 관계 (퇴사 여부별)', fontsize=16)
    plt.xlabel('총 근무 연수 (Total Working Years)', fontsize=12)
    plt.ylabel('월 소득 (Monthly Income)', fontsize=12)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.savefig(os.path.join(image_folder, '2_income_vs_working_years_scatter.png'))
    plt.close()

    # --- 3. 연령 분포 (Histogram) ---
    plt.figure(figsize=(10, 6))
    plt.hist(df[df['Attrition'] == 'No']['Age'], bins=30, alpha=0.7, label='비퇴사', color='skyblue')
    plt.hist(df[df['Attrition'] == 'Yes']['Age'], bins=30, alpha=0.7, label='퇴사', color='salmon')
    plt.title('연령 분포 (퇴사 여부별)', fontsize=16)
    plt.xlabel('연령 (Age)', fontsize=12)
    plt.ylabel('직원 수', fontsize=12)
    plt.legend()
    plt.savefig(os.path.join(image_folder, '3_age_distribution_histogram.png'))
    plt.close()

    # --- 4. 직무 만족도별 퇴사자 수 (Stacked Bar Chart) ---
    satisfaction_attrition = df.groupby(['JobSatisfaction', 'Attrition']).size().unstack()
    satisfaction_attrition.plot(kind='bar', stacked=True, figsize=(10, 7), colormap='coolwarm')
    plt.title('직무 만족도와 퇴사 여부', fontsize=16)
    plt.xlabel('직무 만족도 (1: 낮음, 4: 높음)', fontsize=12)
    plt.ylabel('직원 수', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='퇴사 여부')
    plt.savefig(os.path.join(image_folder, '4_job_satisfaction_stacked_bar.png'))
    plt.close()
    
    # --- 5. 수치형 변수 상관관계 (Heatmap) ---
    numeric_cols = df.select_dtypes(include=np.number)
    # Attrition은 숫자형이 아니므로 변환 필요
    df_corr = df.copy()
    df_corr['Attrition'] = df_corr['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
    numeric_cols = df_corr.select_dtypes(include=np.number)
    corr = numeric_cols.corr()
    
    plt.figure(figsize=(20, 15))
    heatmap = plt.pcolor(corr, cmap='RdYlBu')
    plt.colorbar(heatmap)
    plt.title('수치형 변수 간 상관관계 히트맵', fontsize=18)
    plt.xticks(np.arange(0.5, len(corr.columns), 1), corr.columns, rotation=90)
    plt.yticks(np.arange(0.5, len(corr.index), 1), corr.index)
    plt.tight_layout()
    plt.savefig(os.path.join(image_folder, '5_correlation_heatmap.png'))
    plt.close()

    # --- 6. 퇴사자 결혼 상태 (Donut Chart) ---
    attrition_yes = df[df['Attrition'] == 'Yes']
    attrition_marital = attrition_yes['MaritalStatus'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(attrition_marital, labels=attrition_marital.index, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.3))
    plt.title('퇴사자의 결혼 상태 분포 (Donut Chart)', fontsize=16)
    plt.axis('equal') 
    plt.savefig(os.path.join(image_folder, '6_marital_status_donut.png'))
    plt.close()

    # --- 7. 연령대별 평균 월급 (Line Chart) ---
    avg_income_by_age = df.groupby(['Age', 'Attrition'])['MonthlyIncome'].mean().unstack()
    avg_income_by_age.plot(kind='line', figsize=(12, 7), marker='o')
    plt.title('연령대별 평균 월 소득 (퇴사 여부별)', fontsize=16)
    plt.xlabel('연령 (Age)', fontsize=12)
    plt.ylabel('평균 월 소득', fontsize=12)
    plt.grid(True)
    plt.legend(title='퇴사 여부')
    plt.savefig(os.path.join(image_folder, '7_avg_income_by_age_line.png'))
    plt.close()
    
    # --- 8. 교육 분야별 퇴사자 수 (Horizontal Bar Chart) ---
    education_attrition = attrition_yes['EducationField'].value_counts().sort_values()
    plt.figure(figsize=(10, 8))
    education_attrition.plot(kind='barh', color='cornflowerblue')
    plt.title('퇴사자의 교육 분야 분포', fontsize=16)
    plt.xlabel('퇴사자 수', fontsize=12)
    plt.ylabel('교육 분야', fontsize=12)
    for index, value in enumerate(education_attrition):
        plt.text(value, index, str(value))
    plt.tight_layout()
    plt.savefig(os.path.join(image_folder, '8_education_field_hbar.png'))
    plt.close()

    # --- 9. 직급과 환경 만족도별 퇴사율 분석 (Clustered Bar Chart) ---
    grouped_data = df.groupby(['JobLevel', 'EnvironmentSatisfaction', 'Attrition']).size().unstack().fillna(0)
    grouped_data['Total'] = grouped_data.get('No', 0) + grouped_data.get('Yes', 0)
    grouped_data['AttritionRate'] = (grouped_data.get('Yes', 0) / grouped_data['Total']) * 100
    
    pivot_table = grouped_data['AttritionRate'].unstack()

    pivot_table.plot(kind='bar', figsize=(14, 8), width=0.8)
    plt.title('직급 및 환경 만족도별 퇴사율 (Clustered Bar Chart)', fontsize=16)
    plt.xlabel('직급 (Job Level)', fontsize=12)
    plt.ylabel('퇴사율 (%)', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='환경 만족도 (1: 낮음, 4: 높음)', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(image_folder, '9_joblevel_envsatisfaction_attrition_clustered_bar.png'))
    plt.close()

    # --- 10. 직무 역할, 퇴사 여부에 따른 월 소득 분포 (Box Plot) ---
    plt.figure(figsize=(14, 8))
    ax = plt.subplot()
    sorted_roles = df.groupby('JobRole')['MonthlyIncome'].median().sort_values().index
    
    positions = np.array(range(len(sorted_roles))) * 2
    
    bplot1_data = [df[(df.JobRole == role) & (df.Attrition == 'No')]['MonthlyIncome'] for role in sorted_roles]
    bplot2_data = [df[(df.JobRole == role) & (df.Attrition == 'Yes')]['MonthlyIncome'] for role in sorted_roles]

    bplot1 = ax.boxplot(bplot1_data, positions=positions - 0.4, widths=0.6, patch_artist=True, boxprops=dict(facecolor="lightblue"))
    bplot2 = ax.boxplot(bplot2_data, positions=positions + 0.4, widths=0.6, patch_artist=True, boxprops=dict(facecolor="lightcoral"))

    ax.set_title('직무 역할, 퇴사 여부에 따른 월 소득 분포 (Box Plot)', fontsize=16)
    ax.set_ylabel('월 소득', fontsize=12)
    ax.set_xticks(positions, sorted_roles, rotation=90)
    ax.legend([bplot1["boxes"][0], bplot2["boxes"][0]], ['비퇴사', '퇴사'], loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(image_folder, '10_jobrole_income_boxplot.png'))
    plt.close()

    print("분석 스크립트 실행 완료. 10개의 그래프가 'HR-employee-attrition_v2/images/' 폴더에 저장되었습니다.")

if __name__ == '__main__':
    main()
