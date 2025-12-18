import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os
import numpy as np

# Create a directory to save images
if not os.path.exists('HR-employee-attrition/images'):
    os.makedirs('HR-employee-attrition/images')

# Load the dataset
df = pd.read_csv('HR-employee-attrition/HR-Employee-Attrition.csv')

# Start Markdown report
report = """---
title: 'HR 직원 퇴사 분석 EDA'
author: '분석 담당자: Gemini'
date: '2025-12-17'
---

# HR 직원 퇴사 분석 EDA

## 1. 데이터 개요

### 데이터 샘플
"""
report += df.head().to_markdown()

report += """

### 데이터 정보
"""
# Get info as string
import io
buffer = io.StringIO()
df.info(buf=buffer)
report += buffer.getvalue()


report += """

### 기술 통계
"""
report += df.describe().to_markdown()

report += """

## 2. 데이터 시각화 및 분석

"""

# 1. Attrition distributio
plt.figure(figsize=(8, 6))
attrition_counts = df['Attrition'].value_counts()
attrition_counts.plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('퇴사 여부 분포')
plt.xlabel('퇴사 여부')
plt.ylabel('직원 수')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/attrition_distribution.png')
plt.close()

report += """### 1. 퇴사 여부 분포

![퇴사 여부 분포](../HR-employee-attrition/images/attrition_distribution.png)

"""
report += attrition_counts.to_frame().to_markdown()
report += """

"""

# 2. Attrition by Department
plt.figure(figsize=(10, 6))
attrition_by_dept = pd.crosstab(df['Department'], df['Attrition'])
attrition_by_dept.plot(kind='bar', stacked=True)
plt.title('부서별 퇴사 여부')
plt.xlabel('부서')
plt.ylabel('직원 수')
plt.xticks(rotation=45)
plt.legend(title='퇴사 여부')
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/attrition_by_department.png')
plt.close()

report += """### 2. 부서별 퇴사 여부

![부서별 퇴사 여부](../HR-employee-attrition/images/attrition_by_department.png)

"""
report += attrition_by_dept.to_markdown()
report += """

"""

# 3. Attrition by Job Role
plt.figure(figsize=(12, 8))
attrition_by_job_role = pd.crosstab(df['JobRole'], df['Attrition'])
attrition_by_job_role.plot(kind='bar', stacked=True, figsize=(14,8))
plt.title('직무별 퇴사 여부')
plt.xlabel('직무')
plt.ylabel('직원 수')
plt.xticks(rotation=90)
plt.legend(title='퇴사 여부')
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/attrition_by_job_role.png')
plt.close()

report += """### 3. 직무별 퇴사 여부

![직무별 퇴사 여부](../HR-employee-attrition/images/attrition_by_job_role.png)

"""
report += attrition_by_job_role.to_markdown()
report += """

"""

# 4. Attrition by Gender
plt.figure(figsize=(8, 6))
attrition_by_gender = pd.crosstab(df['Gender'], df['Attrition'])
attrition_by_gender.plot(kind='bar', stacked=True)
plt.title('성별별 퇴사 여부')
plt.xlabel('성별')
plt.ylabel('직원 수')
plt.xticks(rotation=0)
plt.legend(title='퇴사 여부')
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/attrition_by_gender.png')
plt.close()

report += """### 4. 성별별 퇴사 여부

![성별별 퇴사 여부](../HR-employee-attrition/images/attrition_by_gender.png)

"""
report += attrition_by_gender.to_markdown()
report += """

"""

# 5. Attrition by Education Field
plt.figure(figsize=(12, 8))
attrition_by_edu_field = pd.crosstab(df['EducationField'], df['Attrition'])
attrition_by_edu_field.plot(kind='bar', stacked=True, figsize=(12,7))
plt.title('교육 분야별 퇴사 여부')
plt.xlabel('교육 분야')
plt.ylabel('직원 수')
plt.xticks(rotation=45)
plt.legend(title='퇴사 여부')
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/attrition_by_education_field.png')
plt.close()

report += """### 5. 교육 분야별 퇴사 여부

![교육 분야별 퇴사 여부](../HR-employee-attrition/images/attrition_by_education_field.png)

"""
report += attrition_by_edu_field.to_markdown()
report += """

"""
# 6. Monthly Income Distribution
plt.figure(figsize=(10, 6))
plt.hist(df['MonthlyIncome'], bins=30, color='skyblue', edgecolor='black')
plt.title('월 수입 분포')
plt.xlabel('월 수입')
plt.ylabel('직원 수')
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/monthly_income_distribution.png')
plt.close()

report += """### 6. 월 수입 분포

![월 수입 분포](../HR-employee-attrition/images/monthly_income_distribution.png)

월 수입 분포를 확인하여 직원들의 급여 수준을 파악합니다.

"""

# 7. Monthly Income vs. Attrition
plt.figure(figsize=(10, 6))
df.boxplot(column='MonthlyIncome', by='Attrition', figsize=(8,6))
plt.title('퇴사 여부에 따른 월 수입')
plt.xlabel('퇴사 여부')
plt.ylabel('월 수입')
plt.suptitle('')
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/monthly_income_vs_attrition.png')
plt.close()

report += """### 7. 퇴사 여부에 따른 월 수입

![퇴사 여부에 따른 월 수입](../HR-employee-attrition/images/monthly_income_vs_attrition.png)

퇴사 여부 그룹 간의 월 수입 분포를 비교하여 급여 수준이 퇴사에 미치는 영향을 분석합니다.

"""

# 8. Job Level vs. Attrition
plt.figure(figsize=(10, 6))
joblevel_attrition = pd.crosstab(df['JobLevel'], df['Attrition'])
joblevel_attrition.plot(kind='bar', stacked=True)
plt.title('직급별 퇴사 여부')
plt.xlabel('직급')
plt.ylabel('직원 수')
plt.xticks(rotation=0)
plt.legend(title='퇴사 여부')
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/job_level_vs_attrition.png')
plt.close()

report += """### 8. 직급별 퇴사 여부

![직급별 퇴사 여부](../HR-employee-attrition/images/job_level_vs_attrition.png)

"""
report += joblevel_attrition.to_markdown()
report += """

"""
# 9. Years at Company vs. Attrition
plt.figure(figsize=(10, 6))
df.boxplot(column='YearsAtCompany', by='Attrition', figsize=(8,6))
plt.title('퇴사 여부에 따른 근속 년수')
plt.xlabel('퇴사 여부')
plt.ylabel('근속 년수')
plt.suptitle('')
plt.grid(axis='y', linestyle='--')
plt.savefig('HR-employee-attrition/images/years_at_company_vs_attrition.png')
plt.close()

report += """### 9. 퇴사 여부에 따른 근속 년수

![퇴사 여부에 따른 근속 년수](../HR-employee-attrition/images/years_at_company_vs_attrition.png)

퇴사 여부 그룹 간의 근속 년수 분포를 비교하여 근속 기간이 퇴사에 미치는 영향을 분석합니다.

"""
# 10. Correlation Heatmap
# Select only numeric columns for correlation matrix
numeric_df = df.select_dtypes(include=['number'])
plt.figure(figsize=(16, 12))
import seaborn as sns
# As per user request, do not set seaborn style
# sns.set(style='white')
corr = numeric_df.corr()
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.title('수치형 변수들의 상관관계 히트맵')
plt.savefig('HR-employee-attrition/images/correlation_heatmap.png')
plt.close()


report += """### 10. 수치형 변수들의 상관관계 히트맵

![상관관계 히트맵](../HR-employee-attrition/images/correlation_heatmap.png)

수치형 변수들 간의 상관관계를 히트맵으로 시각화하여 변수 간의 관계를 파악합니다.

"""

# Save the report to a markdown file
with open('HR-employee-attrition/HR_EDA_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("EDA report and images have been generated successfully.")
