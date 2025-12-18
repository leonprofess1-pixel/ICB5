# 작업 지시서: 근속 3년 이하 Sales 직원의 이탈률 분석

## 1. 분석 목적
- 근속년수 3년 이하인 Sales Department 직원의 이탈(Attrition) 현황을 심층적으로 분석한다.
- 주요 이탈 원인을 파악하여 비즈니스 인사이트를 도출하고, 이탈률 감소를 위한 구체적인 액션 플랜 수립의 기반을 마련한다.

## 2. 데이터
- **위치:** `3y_sales_hr/HR-Employee-Attrition.csv`

## 3. 핵심 분석 대상
- **부서(Department):** 'Sales'
- **근속년수(YearsAtCompany):** 3년 이하 (<= 3)

## 4. 기술 및 환경 요구사항
- **가상환경:** 프로젝트 루트의 `.venv` 가상환경을 사용한다.
- **한글 처리:** `koreanize-matplotlib` 라이브러리를 사용하여 시각화에 한글을 적용한다.
- **스타일:** `seaborn`의 `set_style()` 과 같은 전역 스타일 설정은 사용하지 않는다.
- **산출물 저장 위치:**
    - 모든 분석 코드(.py) 및 결과물(.md)은 `3y_sales_hr/` 폴더 내에 저장한다.
    - 모든 시각화 이미지 파일(.png)은 `3y_sales_hr/images/` 폴더 내에 저장한다.

## 5. EDA 및 보고서 작성 가이드
- **EDA 스크립트:** 데이터 로드, 전처리, 분석 및 시각화 과정을 담은 Python 스크립트(`eda_sales_attrition.py`)를 `3y_sales_hr/` 폴더에 생성한다.
- **결과 보고서:**
    - 모든 EDA 결과와 분석 내용은 `HR_Sales_Attrition_Report.md` 라는 단일 마크다운 파일로 `3y_sales_hr/` 폴더에 작성한다.
    - **시각화:**
        - 최소 10개 이상의 다양한 그래프를 사용하여 분석 대상 그룹의 특징을 시각화한다.
        - 생성된 모든 그래프는 `3y_sales_hr/images/` 경로에 저장하고, 마크다운 파일에서 해당 이미지를 올바르게 참조해야 한다. (예: `![그래프 설명](./images/graph_name.png)`)
        - 각 시각화 자료에 대해서는 무엇을 나타내는지, 어떤 인사이트를 얻을 수 있는지 상세한 설명을 포함한다.
    - **교차표/피봇테이블:**
        - 막대 그래프(Bar plot)로 표현된 모든 범주형 데이터 분석 결과 하단에는 반드시 해당 데이터의 교차표(crosstab) 또는 피봇 테이블(pivot table)을 첨부하여 정확한 수치를 명시한다.

## 6. 분석 질문 예시 (최소 10개 이상 분석 및 시각화)
1.  **이탈률 분포:** Sales 부서 내 근속 3년 이하 직원의 전체 이탈률(Yes vs. No)은 어떻게 되는가?
2.  **성별에 따른 이탈률:** 남성과 여성 직원의 이탈률에 차이가 있는가?
3.  **직무(JobRole)에 따른 이탈률:** Sales 부서 내 다른 직무(e.g., Sales Executive, Sales Representative) 간 이탈률 차이는 어떠한가?
4.  **학력(EducationField)에 따른 이탈률:** 출신 학문 분야별로 이탈률에 차이가 나타나는가?
5.  **월급(MonthlyIncome) 분포:** 이탈한 그룹과 잔류한 그룹 간의 월급 분포에 차이가 있는가? (Histogram or Boxplot)
6.  **업무 만족도(JobSatisfaction):** 업무 만족도 수준에 따라 이탈률이 어떻게 달라지는가?
7.  **환경 만족도(EnvironmentSatisfaction):** 근무 환경 만족도가 이탈에 영향을 미치는가?
8.  **업무 관련 스트레스(BusinessTravel):** 출장 빈도와 이탈률 간의 관계는 어떠한가?
9.  **승진까지의 기간(YearsSinceLastPromotion):** 마지막 승진 이후 기간이 이탈에 영향을 주는가?
10. **상사와의 관계(RelationshipSatisfaction):** 상사와의 관계 만족도가 이탈률과 관련이 있는가?
11. **총 경력(TotalWorkingYears) 대비 이탈률:** 총 경력이 짧은 직원들의 이탈률이 더 높은 경향이 있는가?
12. **나이(Age) 분포:** 특정 연령대에서 이탈률이 더 높게 나타나는가?

---
이 작업 지시서는 위의 요구사항을 충족하는 분석 보고서 및 관련 산출물을 생성하는 것을 목표로 한다.

---

## Streamlit 대시보드 생성 프롬프트

**목표:** `3y_sales_hr/eda_sales_attrition.py`의 분석 내용을 기반으로, 근속 3년 이하 Sales 부서 직원의 이탈 요인을 탐색할 수 있는 인터랙티브 Streamlit 대시보드를 제작합니다.

**파일명:** `3y_sales_hr/dashboard_sales_attrition.py`

**기술 요구사항:**
- **시각화 라이브러리:** `plotly.express` 또는 `plotly.graph_objects`만 사용해야 합니다. (matplotlib, seaborn 등 다른 라이브러리 사용 금지)
- **데이터:** `3y_sales_hr/HR-Employee-Attrition.csv` 파일을 로드하여 사용합니다.
- **핵심 필터링:** 데이터는 **Department가 'Sales'이고 YearsAtCompany가 3 이하인 직원**을 기본으로 필터링하여 사용합니다.

**대시보드 레이아웃 및 기능:**

1.  **페이지 제목:** "근속 3년 이하 Sales 직원 이탈 현황 대시보드"
2.  **사이드바 (Sidebar):**
    - **제목:** "필터"
    - **다중 선택 필터 (Multiselect):**
        - **직무 (JobRole):** 분석할 직무를 선택할 수 있는 다중 선택 필터를 추가합니다. (기본값: 모든 직무 선택)
        - **성별 (Gender):** 'Male', 'Female'을 선택할 수 있는 다중 선택 필터를 추가합니다. (기본값: 모두 선택)
    - **슬라이더 필터 (Slider):**
        - **나이 (Age):** 분석할 직원의 나이 범위를 조절할 수 있는 슬라이더를 추가합니다.

3.  **메인 화면 구성:**
    - **1행: 핵심 지표 (KPIs)**
        - 필터된 데이터의 **전체 직원 수**, **이탈 직원 수**, **이탈률(%)**을 `st.metric`을 사용하여 3개의 컬럼으로 표시합니다.

    - **2행: 이탈 현황 개요**
        - **컬럼 1: 이탈률 분포 (파이 차트)**
            - `plotly.express.pie`를 사용하여 전체 이탈(Yes/No) 비율을 보여주는 파이 차트를 생성합니다.
        - **컬럼 2: 이탈 사유별 인원 (데이터프레임)**
            - 이탈(Attrition='Yes')한 직원들의 주요 데이터(예: JobRole, MonthlyIncome, JobSatisfaction 등)를 `st.dataframe`으로 표시합니다.

    - **3행 이후: 변수별 심층 분석 (탭으로 구성)**
        - `st.tabs`를 사용하여 "인구통계학적 분석", "직무 관련 분석", "만족도 분석" 3개의 탭을 생성합니다.

        - **[탭 1: 인구통계학적 분석]**
            - **성별에 따른 이탈률 (Grouped Bar Chart):** `px.bar`를 사용하여 성별(x축)에 따른 이탈 여부(색상)를 비교하는 그룹 막대 차트를 생성합니다.
            - **연령대별 이탈 현황 (Histogram):** `px.histogram`을 사용하여 이탈 그룹과 잔류 그룹의 연령 분포를 비교하는 히스토그램을 생성합니다.
            - **학력 수준별 이탈률 (Bar Chart):** `px.bar`를 사용하여 학력(EducationField)에 따른 이탈률을 비교하는 막대 차트를 생성합니다.

        - **[탭 2: 직무 관련 분석]**
            - **직무별 이탈 현황 (Bar Chart):** `px.bar`를 사용하여 직무(JobRole)에 따른 이탈 인원 또는 비율을 보여주는 막대 차트를 생성합니다.
            - **월급과 이탈 여부 (Box Plot):** `px.box`를 사용하여 이탈 그룹과 잔류 그룹의 월급(MonthlyIncome) 분포를 비교하는 박스 플롯을 생성합니다.
            - **총 경력과 이탈 여부 (Violin Plot):** `px.violin`을 사용하여 이탈 그룹과 잔류 그룹의 총 경력(TotalWorkingYears) 분포를 시각화합니다.
            - **출장 빈도와 이탈률 (Sunburst Chart):** `px.sunburst`를 사용하여 출장 빈도(BusinessTravel)와 이탈 여부의 관계를 계층적으로 보여줍니다.

        - **[탭 3: 만족도 분석]**
            - **만족도별 이탈률 (Facet Grid of Bar Charts):** `px.bar`와 `facet_col`을 활용하여 업무 만족도(JobSatisfaction), 환경 만족도(EnvironmentSatisfaction), 관계 만족도(RelationshipSatisfaction) 각각에 대한 이탈률을 한 번에 비교하여 보여줍니다.
            - **상호작용이 가능한 산점도 (Scatter Plot):** `px.scatter`를 사용하여 '월급(MonthlyIncome)'과 '업무 만족도(JobSatisfaction)'의 관계를 보여주는 산점도를 생성하고, 점의 색상을 '이탈 여부(Attrition)'로 지정하여 시각적인 구분을 줍니다.
