
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import sys

def install_and_import_md_pdf():
    """markdown-pdf 라이브러리를 설치하고, 없으면 예외를 발생시킵니다."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown-pdf"])
        print("Successfully installed markdown-pdf")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install markdown-pdf: {e}")
        print("Please install it manually: pip install markdown-pdf")
        return False
    return True

def set_korean_font():
    """운영체제에 맞는 한글 폰트를 설정합니다."""
    try:
        if sys.platform == "win32":
            font_name = "Malgun Gothic"
        elif sys.platform == "darwin":
            font_name = "AppleGothic"
        else: # Linux
            font_name = "NanumGothic"
        plt.rc("font", family=font_name)
        plt.rc("axes", unicode_minus=False)
        print(f"Font set to {font_name}")
    except Exception as e:
        print(f"Could not set Korean font: {e}")
        print("Graphs will be generated in English.")

def main():
    """메인 분석 및 리포트 생성 함수"""
    # --- 0. 환경 설정 ---
    
    # 한글 폰트 설정
    set_korean_font()

    # 경로 설정
    base_dir = "FCIC/causal-inference"
    image_dir = os.path.join(base_dir, "images")
    data_path = os.path.join(base_dir, "data/wage.csv")
    report_md_path = os.path.join(base_dir, "causal_analysis_report.md")
    report_pdf_path = os.path.join(base_dir, "causal_analysis_report.pdf")

    # 폴더 생성
    os.makedirs(image_dir, exist_ok=True)
    print(f"Directories '{base_dir}' and '{image_dir}' are ready.")

    # --- 1. 데이터 로드 ---
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Data file not found at {data_path}")
        return

    # 리포트 파일 열기
    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("# 교육(educ)이 임금(wage)에 미치는 영향 분석 보고서\n\n")
        f.write("이 보고서는 교육 연수가 임금에 미치는 인과 효과를 교란 변수를 통제하여 분석합니다.\n\n")

        # --- 2. EDA (탐색적 데이터 분석) ---
        f.write("## 1. 탐색적 데이터 분석 (EDA)\n\n")
        f.write("### 1.1. 데이터 샘플 확인\n")
        f.write("데이터의 상위 5개 행은 다음과 같습니다.\n\n")
        f.write("```\n")
        f.write(df.head().to_string())
        f.write("\n```\n\n")

        f.write("### 1.2. 기술 통계량\n")
        f.write("주요 변수들의 기술 통계량은 다음과 같습니다.\n\n")
        f.write("```\n")
        f.write(df.describe().to_string())
        f.write("\n```\n\n")
        
        f.write("### 1.3. 주요 변수 분포 시각화\n")
        
        # 임금 분포
        plt.figure(figsize=(10, 6))
        sns.histplot(df['wage'], kde=True)
        plt.title("임금(wage) 분포")
        plt.xlabel("임금")
        plt.ylabel("빈도")
        img_path = os.path.join(image_dir, "1_wage_distribution.png")
        plt.savefig(img_path)
        plt.close()
        f.write("#### 임금(wage) 분포\n")
        f.write(f"![wage_dist](./images/1_wage_distribution.png)\n")
        f.write("- 임금 데이터는 오른쪽으로 꼬리가 긴 분포를 보입니다.\n\n")

        # 교육연차 분포
        plt.figure(figsize=(10, 6))
        sns.histplot(df['educ'], discrete=True)
        plt.title("교육연차(educ) 분포")
        plt.xlabel("교육연차")
        plt.ylabel("빈도")
        img_path = os.path.join(image_dir, "2_educ_distribution.png")
        plt.savefig(img_path)
        plt.close()
        f.write("#### 교육연차(educ) 분포\n")
        f.write(f"![educ_dist](./images/2_educ_distribution.png)\n")
        f.write("- 12년(고등학교 졸업)과 16년(대학교 졸업)에서 가장 빈도가 높게 나타납니다.\n\n")

        # --- 3. 교육과 임금의 단순 관계 분석 (교란변수 미통제) ---
        f.write("## 2. 교육과 임금의 단순 관계 분석\n\n")
        f.write("먼저 교란 변수를 통제하지 않고 교육 연수와 임금의 관계를 살펴보겠습니다.\n\n")

        # 교육 수준별 평균 임금
        educ_wage = df.groupby('educ')['wage'].mean().reset_index()

        plt.figure(figsize=(12, 7))
        sns.barplot(data=educ_wage, x='educ', y='wage', color='skyblue')
        plt.title("교육 연수별 평균 임금 (단순 비교)")
        plt.xlabel("교육 연수 (educ)")
        plt.ylabel("평균 임금 (wage)")
        img_path = os.path.join(image_dir, "3_educ_wage_naive.png")
        plt.savefig(img_path)
        plt.close()
        
        f.write("### 2.1. 교육 연수별 평균 임금 시각화\n")
        f.write(f"![educ_wage_naive](./images/3_educ_wage_naive.png)\n\n")
        f.write("### 2.2. 교육 연수별 평균 임금 데이터\n")
        f.write("```\n")
        f.write(educ_wage.to_string())
        f.write("\n```\n\n")
        f.write("**해석:** 교육 연수가 길어질수록 평균 임금이 증가하는 뚜렷한 양의 상관관계를 보입니다. 하지만 이 관계에는 다른 변수들이 영향을 미쳤을 수 있습니다.\n\n")

        # --- 4. 교란 변수 탐색 ---
        f.write("## 3. 교란 변수(Confounder) 탐색\n\n")
        f.write("교육과 임금에 공통적으로 영향을 미칠 수 있는 변수(교란 변수)를 탐색합니다. 여기서는 **경험(exper)**, **인종(black)**, **결혼상태(married)** 등을 중심으로 살펴보겠습니다.\n\n")

        # 상관관계 히트맵
        plt.figure(figsize=(12, 10))
        corr = df[['wage', 'educ', 'exper', 'married', 'black']].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("주요 변수 간 상관관계 히트맵")
        img_path = os.path.join(image_dir, "4_correlation_heatmap.png")
        plt.savefig(img_path)
        plt.close()
        f.write("### 3.1. 상관관계 히트맵\n")
        f.write(f"![corr_heatmap](./images/4_correlation_heatmap.png)\n")
        f.write("- `wage`는 `educ`(0.41), `exper`(0.11)와 양의 상관관계를 보입니다.\n")
        f.write("- `educ`와 `exper`는 강한 음의 상관관계(-0.27)를 보입니다. 이는 교육 기간이 길어지면 노동 시장 진입이 늦어져 초기 경험이 짧아지기 때문일 수 있습니다.\n")
        f.write("- 이 관계는 `exper`가 교란 변수로 작용할 가능성을 시사합니다.\n\n")

        # 경험(exper)과 임금(wage)의 관계
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='exper', y='wage', alpha=0.3)
        plt.title("경험과 임금의 관계")
        plt.xlabel("경험 (exper)")
        plt.ylabel("임금 (wage)")
        img_path = os.path.join(image_dir, "5_exper_wage_scatter.png")
        plt.savefig(img_path)
        plt.close()
        f.write("### 3.2. 경험과 임금의 관계\n")
        f.write(f"![exper_wage](./images/5_exper_wage_scatter.png)\n")
        f.write("- 경험이 많을수록 임금이 증가하는 경향이 보입니다.\n\n")

        # 결혼 여부에 따른 임금
        married_wage = df.groupby('married')['wage'].mean().reset_index()
        plt.figure(figsize=(8, 5))
        sns.barplot(data=married_wage, x='married', y='wage')
        plt.title("결혼 여부에 따른 평균 임금")
        plt.xlabel("결혼 여부 (0=미혼, 1=기혼)")
        plt.ylabel("평균 임금")
        img_path = os.path.join(image_dir, "6_married_wage_bar.png")
        plt.savefig(img_path)
        plt.close()
        f.write("### 3.3. 결혼 여부에 따른 평균 임금\n")
        f.write(f"![married_wage](./images/6_married_wage_bar.png)\n")
        f.write("```\n")
        f.write(married_wage.to_string())
        f.write("\n```\n")
        f.write("- 기혼(1)이 미혼(0)보다 평균 임금이 높습니다.\n\n")

        # 인종에 따른 임금
        black_wage = df.groupby('black')['wage'].mean().reset_index()
        plt.figure(figsize=(8, 5))
        sns.barplot(data=black_wage, x='black', y='wage')
        plt.title("인종에 따른 평균 임금")
        plt.xlabel("인종 (0=기타, 1=흑인)")
        plt.ylabel("평균 임금")
        img_path = os.path.join(image_dir, "7_black_wage_bar.png")
        plt.savefig(img_path)
        plt.close()
        f.write("### 3.4. 인종에 따른 평균 임금\n")
        f.write(f"![black_wage](./images/7_black_wage_bar.png)\n")
        f.write("```\n")
        f.write(black_wage.to_string())
        f.write("\n```\n")
        f.write("- 흑인이 아닌 그룹(0)이 흑인(1)보다 평균 임금이 높습니다. 이는 `black` 변수도 교란 요인일 수 있음을 시사합니다.\n\n")


        # --- 5. 교란 변수 통제 후 인과 효과 분석 (공정한 비교) ---
        f.write("## 4. 교란 변수 통제 후 인과 효과 분석\n\n")
        f.write("가장 큰 교란 변수로 추정되는 **경험(exper)**을 통제하여 교육의 효과를 다시 측정합니다. '경험'이 비슷한 사람들끼리 그룹을 나누어(Stratification), 각 그룹 내에서 교육의 효과를 분석합니다.\n\n")

        # 경험(exper) 변수를 범주형으로 변환 (데이터 범위에 맞게 수정)
        max_exper = df['exper'].max()
        bins = [0, 5, 10, 15, 20, max_exper + 1]
        labels = ['0-5년', '6-10년', '11-15년', '16-20년', '21년 이상']
        df['exper_group'] = pd.cut(df['exper'], bins=bins, labels=labels, right=False)

        f.write("### 4.1. 경험 그룹별 교육-임금 관계 분석\n")
        
        # 각 경험 그룹별로 시각화 및 분석
        # 수정된 labels 리스트를 사용
        for i, group in enumerate(labels):
            f.write(f"#### 경험 그룹: {group}\n")
            
            group_df = df[df['exper_group'] == group]
            if group_df.empty:
                f.write(f"- 해당 그룹에 데이터가 없습니다.\n\n")
                continue
            
            educ_wage_stratified = group_df.groupby('educ')['wage'].mean().reset_index()

            plt.figure(figsize=(10, 6))
            sns.barplot(data=educ_wage_stratified, x='educ', y='wage', color='coral')
            plt.title(f"교육 연수별 평균 임금 (경험: {group})")
            plt.xlabel("교육 연수 (educ)")
            plt.ylabel("평균 임금 (wage)")
            plt.ylim(0, df['wage'].max()) # y축 통일
            img_path = os.path.join(image_dir, f"8_{i+1}_educ_wage_{group}.png")
            plt.savefig(img_path)
            plt.close()

            f.write(f"![educ_wage_{group}](./images/8_{i+1}_educ_wage_{group}.png)\n")
            f.write("```\n")
            f.write(educ_wage_stratified.to_string())
            f.write("\n```\n")
            f.write(f"**해석:** '{group}' 경험 그룹 내에서는 교육 연수가 임금에 미치는 영향이 전체 데이터로 봤을 때보다 약화되거나, 특정 구간에서는 역전되는 현상도 관찰됩니다. 이는 경험이라는 변수가 임금에 큰 영향을 미치고 있음을 보여줍니다.\n\n")


        # --- 6. 결론 ---
        f.write("## 5. 결론\n\n")
        f.write("### 5.1. 분석 요약\n")
        f.write("단순히 교육 연수와 임금의 관계를 분석했을 때, 교육 수준이 높을수록 임금이 높아지는 강한 양의 상관관계가 나타났습니다. 하지만 이는 '경험'이라는 교란 변수의 효과가 혼재된 결과일 가능성이 높습니다.\n\n")
        f.write("이에 '경험' 수준이 비슷한 사람들끼리 그룹을 나누어 '공정한 비교'를 수행한 결과, 각 그룹 내에서 교육이 임금에 미치는 영향은 단순 분석 결과보다 상당히 약화되었습니다. 특히, 특정 경험 그룹에서는 교육 수준이 높아져도 임금이 크게 오르지 않는 현상도 발견되었습니다.\n\n")
        f.write("### 5.2. 최종 결론\n")
        f.write("결론적으로, **교육 연수가 임금에 미치는 순수한 인과 효과는 처음 관찰된 것만큼 크지 않을 수 있습니다.** 임금은 교육 수준뿐만 아니라, 경력(경험), 인종, 결혼 여부 등 다양한 사회경제적 요인들의 복합적인 상호작용의 결과입니다. 따라서 정책 수립이나 의사 결정 시 이러한 교란 변수들을 충분히 고려하여 인과 관계를 신중하게 해석해야 합니다.\n\n")

    print(f"Markdown report generated: {report_md_path}")

    # --- 7. PDF 변환 ---
    print("\n--- Converting Markdown to PDF ---")
    if install_and_import_md_pdf():
        try:
            # markdown-pdf CLI 도구 사용
            # The tool might not be in the PATH, so we call it via python's module execution
            subprocess.run(
                f'npx --yes markdown-pdf "{report_md_path}" -o "{report_pdf_path}"',
                shell=True, check=True
            )
            print(f"Successfully converted to PDF: {report_pdf_path}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error during PDF conversion: {e}")
            print("Please ensure Node.js and npx are installed and in your PATH.")
            print("You can also convert the markdown file manually.")
    else:
        print("Skipping PDF conversion due to installation failure.")


if __name__ == "__main__":
    main()
