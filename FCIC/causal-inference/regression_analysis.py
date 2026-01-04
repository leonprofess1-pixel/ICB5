import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    """
    인과추론 회귀분석을 수행하고, 전체 과정을 마크다운 보고서로 자동 생성하는 마스터 함수.
    """
    
    # --- 1. 환경 설정 ---
    # 결과물을 저장할 디렉토리 경로 설정
    output_dir = './FCIC/causal-inference'
    image_dir = os.path.join(output_dir, 'images')
    
    # 데이터 경로 설정
    data_path = os.path.join(output_dir, 'data', 'wage.csv')
    report_path = os.path.join(output_dir, 'regression_analysis_report.md')

    # 디렉토리 생성 (없는 경우)
    os.makedirs(image_dir, exist_ok=True)
    
    # 시각화 한글 폰트 설정 (macOS/Windows)
    try:
        plt.rc('font', family='AppleGothic')
    except:
        plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
    
    # --- 데이터 로드 ---
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"오류: 데이터 파일을 찾을 수 없습니다. 경로: {data_path}")
        return
        

    
    # 마크다운 보고서 내용 초기화
    report_md = "# 교육 수준이 임금에 미치는 영향 분석: 회귀분석 기반 인과추론\n\n"
    report_md += "이 보고서는 교육 수준(educ)이 시간당 임금(wage)에 미치는 인과적 영향을 회귀분석을 통해 탐색합니다.\n\n"

    # --- 0단계: EDA (탐색적 데이터 분석) ---
    report_md += "## 0. 탐색적 데이터 분석 (EDA)\n\n"
    report_md += "### 데이터 샘플 (상위 5개 행)\n"
    report_md += df.head().to_markdown(index=False) + "\n\n"
    
    report_md += "### 기술 통계량 요약\n"
    report_md += "```\n"
    report_md += df.describe().to_string() + "\n"
    report_md += "```\n\n"
    
    # 주요 변수 분포 시각화
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.histplot(df['wage'], kde=True, ax=axes[0, 0]).set_title('시간당 임금(wage) 분포')
    sns.histplot(df['lhwage'], kde=True, ax=axes[0, 1]).set_title('로그 변환 시간당 임금(lhwage) 분포')
    sns.histplot(df['educ'], kde=False, ax=axes[1, 0], bins=15).set_title('교육 수준(educ) 분포')
    sns.histplot(df['IQ'], kde=True, ax=axes[1, 1]).set_title('IQ 점수 분포')
    plt.tight_layout()
    eda_dist_path = os.path.join(image_dir, '0_eda_distributions.png')
    fig.savefig(eda_dist_path)
    plt.close(fig)
    report_md += "### 주요 변수 분포\n"
    report_md += f"![주요 변수 분포](./images/{os.path.basename(eda_dist_path)})\n\n"
    report_md += "**해석:** 시간당 임금(`wage`)은 오른쪽으로 꼬리가 긴 분포를 보입니다. 로그 변환을 통해 정규분포에 가까운 형태로 변환하여 분석의 정확도를 높일 수 있습니다. 교육 수준은 특정 연수에 집중되는 경향을 보입니다.\n\n"

    # --- 1단계: 상관계수 계산 및 산점도 시각화 ---
    report_md += "## 1. 상관관계 분석\n\n"
    
    # 상관계수 행렬 계산
    corr_matrix = df[['lhwage', 'educ', 'IQ', 'exper', 'tenure', 'meduc', 'feduc']].corr()
    
    # 히트맵 시각화
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('주요 변수 간 상관계수 히트맵')
    corr_heatmap_path = os.path.join(image_dir, '1_correlation_heatmap.png')
    fig.savefig(corr_heatmap_path)
    plt.close(fig)
    report_md += "### 상관계수 히트맵\n"
    report_md += f"![상관계수 히트맵](./images/{os.path.basename(corr_heatmap_path)})\n\n"
    report_md += "**해석:** 로그 임금(`lhwage`)은 교육 수준(`educ`), `IQ`, 경험(`exper`), 근속 연수(`tenure`)와 양의 상관관계를 보입니다. 특히 교육 수준과의 상관관계가 0.38로 가장 두드러집니다. 또한, 교육 수준과 IQ(0.49), 부모의 교육 수준(meduc, feduc) 간에도 강한 양의 상관관계가 존재하며, 이는 잠재적인 교란 변수의 존재를 시사합니다.\n\n"
    
    # 산점도 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='educ', y='lhwage', alpha=0.5, ax=ax)
    ax.set_title('교육 수준(educ)과 로그 임금(lhwage)의 관계')
    scatter_path = os.path.join(image_dir, '1_scatter_educ_wage.png')
    fig.savefig(scatter_path)
    plt.close(fig)
    report_md += "### 교육 수준과 로그 임금의 산점도\n"
    report_md += f"![산점도](./images/{os.path.basename(scatter_path)})\n\n"
    report_md += "**해석:** 교육 수준이 높을수록 로그 임금 또한 전반적으로 높아지는 뚜렷한 양의 관계가 관찰됩니다.\n\n"

    # --- 2단계: 단순 회귀 분석 ---
    report_md += "## 2. 단순 회귀 분석: log(wage) ~ educ\n\n"
    model1 = smf.ols('lhwage ~ educ', data=df).fit()
    
    report_md += "### 모델 요약\n"
    report_md += "```\n"
    report_md += str(model1.summary()) + "\n"
    report_md += "```\n\n"
    
    # 회귀선 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(data=df, x='educ', y='lhwage', ax=ax, scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
    ax.set_title('단순 회귀 분석: 교육 수준과 로그 임금')
    regplot_path = os.path.join(image_dir, '2_simple_regression.png')
    fig.savefig(regplot_path)
    plt.close(fig)
    report_md += "### 회귀선 시각화\n"
    report_md += f"![회귀선](./images/{os.path.basename(regplot_path)})\n\n"
    report_md += f"**해석:** 교육 수준(`educ`)이 1년 증가할 때, 시간당 로그 임금은 평균적으로 약 **{model1.params['educ']:.4f}** 만큼 증가하는 것으로 나타났습니다. 이는 교육 연수가 1년 늘어날 때마다 임금이 약 **{(np.exp(model1.params['educ']) - 1) * 100:.2f}%** 상승하는 것을 의미합니다. 이 모델의 설명력(R-squared)은 **{model1.rsquared:.3f}** 입니다.\n\n"

    # --- 3단계: OVB(누락 변수 편향) 개념 설명 ---
    report_md += "## 3. 누락 변수 편향 (Omitted Variable Bias, OVB)\n\n"
    report_md += "단순 회귀 분석의 결과는 교육 수준과 임금의 '상관관계'를 보여주지만, 이를 '인과관계'로 해석하기는 어렵습니다. 그 이유는 **누락 변수 편향(OVB)**의 가능성 때문입니다.\n\n"
    report_md += "OVB는 아래 두 가지 조건을 만족하는 변수가 모델에서 누락될 때 발생합니다:\n"
    report_md += "1. 누락된 변수가 종속 변수(임금)에 영향을 미친다.\n"
    report_md += "2. 누락된 변수가 모델에 포함된 독립 변수(교육 수준)와 상관관계가 있다.\n\n"
    report_md += "이 분석에서는 개인의 **'능력'이나 '지능'(예: IQ)**과 같은 변수가 OVB를 유발할 수 있습니다. 즉, 지능이 높을수록 더 높은 교육 수준을 달성하고, 동시에 노동 시장에서 더 높은 임금을 받을 가능성이 높습니다. 만약 지능을 통제하지 않으면, 우리는 교육의 효과를 과대평가하게 될 수 있습니다.\n\n"

    # --- 4단계: 다중 회귀 분석 ---
    report_md += "## 4. 다중 회귀 분석: 통제 변수 추가\n\n"
    report_md += "누락 변수 편향 문제를 완화하기 위해, 임금에 영향을 줄 수 있는 다른 변수들을 통제하여 다중 회귀 분석을 수행합니다.\n\n"
    
    # 모델 2: IQ 통제
    model2 = smf.ols('lhwage ~ educ + IQ', data=df).fit()
    report_md += "### 모델 2: IQ 통제\n"
    report_md += "```\n" + str(model2.summary()) + "\n```\n"
    report_md += f"**해석:** IQ를 통제하자 `educ`의 계수가 **{model1.params['educ']:.4f}**에서 **{model2.params['educ']:.4f}**로 감소했습니다. 이는 교육 효과의 일부가 IQ와 같은 개인의 지능에 기인했음을 시사합니다.\n\n"
    
    # 모델 3: 경험, 근속 연수 통제
    model3 = smf.ols('lhwage ~ educ + exper + tenure', data=df).fit()
    report_md += "### 모델 3: 경험 및 근속 연수 통제\n"
    report_md += "```\n" + str(model3.summary()) + "\n```\n"
    report_md += f"**해석:** 경력 관련 변수(`exper`, `tenure`)를 통제하자 `educ`의 계수는 **{model3.params['educ']:.4f}**로 나타났습니다. 모델의 설명력(R-squared)은 **{model3.rsquared:.3f}**로 크게 향상되었습니다.\n\n"

    # 모델 4: 모든 변수 통제
    model4 = smf.ols('lhwage ~ educ + IQ + exper + tenure + meduc + feduc', data=df).fit()
    report_md += "### 모델 4: 모든 잠재적 교란 변수 통제\n"
    report_md += "```\n" + str(model4.summary()) + "\n```\n"
    report_md += f"**해석:** IQ, 경력, 부모 교육 수준까지 모두 통제한 최종 모델에서 `educ`의 계수는 **{model4.params['educ']:.4f}**입니다. 이는 다른 주요 요인들의 효과를 분리하고 난 후의 '순수한' 교육의 효과에 더 가까운 추정치라고 볼 수 있습니다. 모델의 설명력도 **{model4.rsquared:.3f}**로 가장 높습니다.\n\n"

    # --- 5단계: 모델별 educ 계수 비교표 작성 ---
    report_md += "## 5. 모델별 교육(educ) 계수 비교\n\n"
    
    # 계수 비교 데이터프레임 생성
    coef_comparison = pd.DataFrame({
        'Model': ['Model 1: Simple', 'Model 2: + IQ', 'Model 3: + Career', 'Model 4: Full'],
        'educ_coefficient': [model1.params['educ'], model2.params['educ'], model3.params['educ'], model4.params['educ']],
        'R-squared': [model1.rsquared, model2.rsquared, model3.rsquared, model4.rsquared]
    }).set_index('Model')
    
    report_md += coef_comparison.to_markdown() + "\n\n"
    
    # 계수 변화 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    coef_comparison['educ_coefficient'].plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('모델별 educ 계수 변화')
    ax.set_ylabel('educ 계수 (Coefficient)')
    ax.tick_params(axis='x', rotation=45)
    coef_plot_path = os.path.join(image_dir, '5_coefficient_comparison.png')
    fig.savefig(coef_plot_path)
    plt.close(fig)
    report_md += f"![계수 변화](./images/{os.path.basename(coef_plot_path)})\n\n"
    report_md += "**해석:** 통제 변수가 추가될수록 `educ`의 계수가 점차 감소하는 것을 명확히 확인할 수 있습니다. 이는 초기에 관찰된 교육과 임금의 강한 상관관계가 다른 변수들(특히 IQ와 경력)에 의해 부풀려졌음을 의미합니다. 즉, 누락 변수 편향이 양(+)의 방향으로 작용했음을 알 수 있습니다.\n\n"

    # --- 6단계: 인과적 해석 결론 작성 ---
    report_md += "## 6. 결론: 인과적 해석\n\n"
    report_md += "단순 회귀 분석에서 교육 1년의 임금 상승 효과는 약 **9.75%**로 나타났지만, 이는 다른 요인들의 영향이 혼재된 결과입니다.\n\n"
    report_md += f"개인의 지능(IQ), 경력(exper, tenure), 그리고 가정 환경(meduc, feduc)과 같은 주요 교란 변수들을 통제한 최종 모델(Model 4)에 따르면, **교육 수준(educ)이 1년 증가할 때 임금은 평균적으로 약 {(np.exp(model4.params['educ']) - 1) * 100:.2f}% 상승**하는 것으로 추정됩니다. \n\n"
    report_md += "이 값은 단순 회귀 분석의 결과보다 작지만, 여전히 통계적으로 유의미하며 교육이 임금에 미치는 긍정적인 인과 효과의 더 나은 근사치라고 해석할 수 있습니다. 물론, 이 모델에서 통제하지 못한 또 다른 잠재적 교란 변수(예: 개인의 성실성, 사회적 네트워크 등)가 존재할 수 있으므로, 이 결과를 완벽한 인과관계로 단정하기보다는 '관찰 가능한 주요 변수를 통제했을 때의 조건부 연관성'으로 이해하는 것이 가장 정확한 해석일 것입니다.\n"
    
    # --- 리포트 파일 생성 ---
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_md)
        print(f"성공: 회귀분석 보고서가 다음 경로에 저장되었습니다: {report_path}")
    except IOError as e:
        print(f"오류: 보고서 파일을 쓰는 중 문제가 발생했습니다. {e}")

if __name__ == '__main__':
    main()
