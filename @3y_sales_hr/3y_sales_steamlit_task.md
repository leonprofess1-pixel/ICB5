# [작업 지시서] 근속 3년 이하 Sales 직원 이탈 요인 분석 Streamlit 대시보드

## 1. 프로젝트 목표
근속 3년 이하 Sales 부서 직원의 이탈 현황에 대한 심층 분석 보고서 내용을 기반으로, 경영진과 HR 담당자가 이탈의 핵심 동인을 직관적으로 파악하고 데이터 기반의 의사결정을 내릴 수 있는 **インタラクティブ 대시보드**를 개발한다.

## 2. 핵심 요구사항
- **전문가 수준의 심층 분석 시각화**: 10가지 이상의 다각적이고 복합적인 분석 차트를 포함한다.
- **インタラクティブ 탐색**: 사용자가 직접 필터를 적용하여 특정 직원 그룹의 데이터를 탐색할 수 있는 기능을 제공한다.
- **실행 가능한 인사이트 제공**: 각 시각화 자료에 대해 명확한 비즈니스 인사이트와 구체적인 액션 플랜을 제시한다.
- **체계적인 구조**: 사이드바 내비게이션과 탭을 활용하여 사용자가 원하는 정보에 쉽게 접근할 수 있도록 설계한다.

---

## 3. 대시보드 구조 설계

### 3.1. 메인 레이아웃
- **사이드바 (Navigation)**: 대시보드의 주요 분석 테마별로 페이지를 구분한다.
  - 📄 **요약 및 개요 (Summary)**
  - 💰 **보상 및 재무 (Compensation & Finance)**
  - 📈 **업무 및 성장 (Work & Growth)**
  - 😊 **만족도 및 참여도 (Satisfaction & Engagement)**
  - 🔍 **데이터 직접 탐색 (Data Explorer)**
  - 🎯 **종합 제언 (Final Recommendations)**
- **메인 콘텐츠 영역**: 사이드바에서 선택된 페이지의 내용을 표시한다. 각 페이지는 탭(`st.tabs`)을 사용하여 여러 분석을 체계적으로 보여준다.

### 3.2. 데이터
- **원본 데이터**: `HR-Employee-Attrition.csv`
- **분석 대상**: `Department`가 'Sales'이고 `YearsAtCompany`가 3 이하인 직원.
- **데이터 로딩**: Streamlit의 `@st.cache_data`를 사용하여 데이터 로딩을 캐싱한다.

---

## 4. 페이지별 상세 명세

### 📄 요약 및 개요 (Summary)
- **목표**: 대시보드의 전체 내용을 요약하고 가장 중요한 지표를 한눈에 보여준다.
- **콘텐츠**:
  1. **페이지 제목**: `st.title("Sales 부서 저연차 직원 이탈 분석 대시보드")`
  2. **핵심 성과 지표 (KPIs)**: `st.metric`을 사용
     - **전체 직원 수**: 분석 대상 직원 수
     - **이탈 직원 수**: 이탈한 직원 수
     - **이탈률**: 이탈률 (%)
  3. **Executive Summary**: `st.expander` 사용
     - **핵심 발견**: "낮은 보상", "성장 정체", "업무 불만족"이 3대 핵심 이탈 동인임을 명시.
     - **핵심 제안**: "Sales Rep. 초임 연봉 현실화", "명확한 커리어패스 제시"를 핵심 제안으로 강조.
  4. **전체 이탈 현황 (Pie Chart)**: `plotly.express.pie`
     - 이탈자와 잔류자의 비율을 보여주는 도넛 차트.
     - **인사이트**: 3명 중 1명이 떠나는 상황의 심각성 강조.

### 💰 보상 및 재무 (Compensation & Finance)
- **목표**: 보상 수준이 이탈에 미치는 다각적인 영향을 분석한다.
- **콘텐츠 (Tabs)**:
  1. **Tab 1: 직무별 월 소득 분포 (Violin Plot)**
     - **시각화**: `px.violin`을 사용하여 `JobRole`별 `MonthlyIncome` 분포를 이탈 여부(`Attrition`)에 따라 분리하여 시각화.
     - **인사이트**: 'Sales Representative' 직급의 소득이 이탈의 핵심 원인임을 명확히 보여준다.
     - **액션 플랜**: 'Sales Rep.' 초임 연봉 테이블 현실화, 경쟁사 분석을 통한 연봉 경쟁력 확보.
  2. **Tab 2: 소득 대비 연봉 인상률 (Scatter Plot)**
     - **시각화**: `px.scatter` 사용. x축 `MonthlyIncome`, y축 `PercentSalaryHike`, 색상 `Attrition`, 크기 `PerformanceRating`.
     - **인사이트**: 소득이 낮으면서 연봉 인상률도 낮은 그룹에서 이탈이 활발함. 특히, 성과(`PerformanceRating`)가 좋아도 인상률이 낮으면 이탈 가능성 상승.
     - **액션 플랜**: 성과 평가와 연계된 차등적 연봉 인상률 정책 수립. 고성과-저인상 그룹 집중 면담.
  3. **Tab 3: 이탈에 영향을 미치는 재무 요인 (Waterfall Chart)**
     - **시각화**: `plotly.graph_objects.Waterfall` 사용. 시작값(전체 직원)에서 '저소득 이탈', '낮은 연봉 인상률 이탈' 등 주요 재무 요인에 따른 감소를 시각화.
     - **인사이트**: 이탈 결정에 '절대 소득'이 가장 큰 영향을 미치며, '상대적 박탈감(낮은 인상률)'이 그 뒤를 이음.
     - **액션 플랜**: 이탈 방지 예산 배분 시, 기본급 인상 및 성과 기반 인센티브 강화에 최우선 순위 부여.

### 📈 업무 및 성장 (Work & Growth)
- **목표**: 업무 환경, 강도, 성장 기회가 이탈에 미치는 영향을 분석한다.
- **콘텐츠 (Tabs)**:
  1. **Tab 1: 승진과 직무 레벨 (Bar & Box Plot)**
     - **시각화**: `px.bar`로 `YearsSinceLastPromotion` 그룹별 이탈률을 표시하고, `px.box`로 `JobLevel`별 근속년수(`YearsAtCompany`)를 함께 시각화.
     - **인사이트**: 승진 정체(특히 0년차)는 강력한 이탈 신호. 낮은 직무 레벨에 오래 머무를수록 이탈 위험 급증.
     - **액션 플랜**: 입사 2년차 대상 역량 평가 및 Fast-Track 승진 검토. 직무 레벨별 명확한 승진 기준(역량, 성과, 기간) 공표.
  2. **Tab 2: 야근과 출장의 이중고 (Heatmap)**
     - **시각화**: `px.density_heatmap`. x축 `OverTime`, y축 `BusinessTravel`, z축(색상)은 이탈률.
     - **인사이트**: '잦은 출장'과 '잦은 야근'이 겹치는 그룹에서 이탈률이 폭발적으로 증가.
     - **액션 플랜**: 불필요한 출장 및 야근 감소 방안 마련. 해당 그룹에 대한 추가 보상(시간외수당, 출장수당 현실화) 또는 대체 휴무 제공.
  3. **Tab 3: 교육 기회와 성과 (Sunburst Chart)**
     - **시각화**: `px.sunburst` 사용. 계층 구조: `Attrition` -> `PerformanceRating` -> `TrainingTimesLastYear`. 값은 직원 수.
     - **인사이트**: 이탈한 그룹, 특히 성과가 낮은 그룹은 교육 횟수가 현저히 적음. 교육 투자가 성과 및 잔류 의사에 영향을 미칠 가능성 시사.
     - **액션 플랜**: 저성과자 대상 역량 강화 교육 프로그램 의무화. 개인별 경력 개발 계획(IDP)과 연계한 맞춤형 교육 제공.

### 😊 만족도 및 참여도 (Satisfaction & Engagement)
- **목표**: 직원의 만족도, 관계, 참여도가 이탈에 미치는 복합적 영향을 분석한다.
- **콘텐츠 (Tabs)**:
  1. **Tab 1: 다차원 만족도 분석 (Histogram)**
     - **시각화**: `px.histogram` 사용. `EnvironmentSatisfaction`, `JobSatisfaction`, `RelationshipSatisfaction`을 합산한 '종합 만족도' 점수 분포를 이탈 여부에 따라 비교.
     - **인사이트**: 특정 만족도 하나보다는 전반적인 경험의 질이 중요. 종합 만족도 2.5점 이하에서 이탈률 급증.
     - **액션 플랜**: 직원 경험(EX) 전담 조직 신설. 분기별 만족도 설문 및 결과 기반 개선 활동 추진.
  2. **Tab 2: 업무 만족도 vs. 업무 참여도 (2D Density Plot)**
     - **시각화**: `px.density_contour`. x축 `JobSatisfaction`, y축 `JobInvolvement`, 색상으로 이탈/잔류 그룹 구분.
     - **인사이트**: '업무 참여도'는 높지만 '업무 만족도'가 낮은, 즉 '열정적으로 일하지만 불만 가득한' 그룹이 가장 위험한 이탈 후보군.
     - **액션 플랜**: 해당 그룹 대상 심층 인터뷰를 통해 불만족 핵심 원인(보상, 인정, 비전 등) 파악 및 해결.
  3. **Tab 3: 성과 평가와 만족도 (Faceted Scatter Plot)**
     - **시각화**: `px.scatter`, x축 `PerformanceRating`, y축 `JobSatisfaction`, `Attrition`으로 색상 구분. `Gender`나 `JobRole`로 facet(분할)하여 비교.
     - **인사이트**: 고성과자(Rating 4) 그룹 내에서도 업무 만족도가 낮은 직원들이 존재하며, 이들이 이탈. 성과와 만족도가 반드시 비례하지 않음.
     - **액션 플랜**: 고성과자 그룹에 대한 비재무적 보상(인정, 도전적 과제 부여, 리더십 기회) 강화.

### 🔍 데이터 직접 탐색 (Data Explorer)
- **목표**: 사용자가 직접 데이터를 필터링하고 원하는 직원 목록을 확인할 수 있는 기능을 제공한다.
- **콘텐츠**:
  1. **필터링 옵션 (Sidebar)**:
     - **직무 (JobRole)**: `st.multiselect`
     - **이탈 여부 (Attrition)**: `st.multiselect`
     - **월 소득 (MonthlyIncome)**: `st.slider`
     - **업무 만족도 (JobSatisfaction)**: `st.multiselect`
     - **성과 등급 (PerformanceRating)**: `st.multiselect`
  2. **데이터 테이블**: `st.dataframe`을 사용하여 필터링된 결과를 표시. 총 몇 명의 직원이 조회되었는지 요약 정보 제공.

### 🎯 종합 제언 (Final Recommendations)
- **목표**: 모든 분석 결과를 종합하여, 즉시 실행 가능한 구체적인 액션 플랜을 우선순위와 함께 제시한다.
- **콘텐츠**: `st.markdown`을 사용하여 테이블 형식으로 제시.
  - **영역**: "보상 및 인정", "성장 및 경력", "업무 환경 및 문화"
  - **핵심 문제**: 각 영역의 가장 시급한 문제점 요약.
  - **우선순위**: 상/중/하로 구분.
  - **제안 액션**: 구체적이고 측정 가능한 액션 아이템.
  - **기대 효과**: 액션 실행 시 기대되는 정성적/정량적 효과.

---

## 5. 구현 가이드 (Python Code Skeleton)

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. 기본 설정 및 데이터 로딩
st.set_page_config(page_title="Sales 부서 이탈 분석", layout="wide")

@st.cache_data
def load_data():
    df_raw = pd.read_csv("3y_sales_hr/HR-Employee-Attrition.csv")
    df = df_raw[(df_raw['Department'] == 'Sales') & (df_raw['YearsAtCompany'] <= 3)].copy()
    df['Attrition_Kor'] = df['Attrition'].apply(lambda x: '이탈' if x == 'Yes' else '잔류')
    # ... 추가 파생 변수 생성 ...
    return df

df = load_data()
IMG_DIR = "3y_sales_hr/images_v3" # 새로운 분석에 따른 이미지 폴더 (가정)
os.makedirs(IMG_DIR, exist_ok=True)

# 2. 사이드바
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["요약 및 개요", "보상 및 재무", "업무 및 성장", "만족도 및 참여도", "데이터 직접 탐색", "종합 제언"])

# 3. 페이지별 함수 정의
def show_summary(df):
    st.title("Sales 부서 저연차 직원 이탈 분석")
    # ... KPI, Executive Summary, Pie Chart 구현 ...

def show_compensation(df):
    st.title("보상 및 재무 분석")
    tab1, tab2, tab3 = st.tabs(["직무별 월 소득", "소득 대비 연봉 인상률", "재무 요인 Waterfall"])
    with tab1:
        # ... Violin Plot 구현 ...
    with tab2:
        # ... Scatter Plot 구현 ...
    with tab3:
        # ... Waterfall Chart 구현 ...

def show_work_growth(df):
    st.title("업무 및 성장 분석")
    # ... Tabs 및 Bar, Heatmap, Sunburst 차트 구현 ...

def show_satisfaction(df):
    st.title("만족도 및 참여도 분석")
    # ... Tabs 및 Histogram, Density, Scatter 차트 구현 ...

def show_explorer(df):
    st.title("데이터 직접 탐색")
    # ... Sidebar 필터 및 데이터프레임 표시 기능 구현 ...

def show_recommendations():
    st.title("종합 제언")
    # ... Markdown 테이블로 종합 제언 표시 ...

# 4. 페이지 라우팅
page_functions = {
    "요약 및 개요": show_summary,
    "보상 및 재무": show_compensation,
    "업무 및 성장": show_work_growth,
    "만족도 및 참여도": show_satisfaction,
    "데이터 직접 탐색": show_explorer,
    "종합 제언": show_recommendations
}

# 선택된 페이지 함수 호출 (데이터프레임을 인자로 전달)
if page in ["요약 및 개요", "데이터 직접 탐색"]:
    page_functions[page](df)
elif page == "종합 제언":
    page_functions[page]()
else:
    page_functions[page](df)
```

이 작업 지시서는 실제 대시보드 개발에 필요한 모든 요구사항, 구조, 상세 명세를 포함하고 있으며, 데이터 분석 전문가의 관점에서 심도 있는 분석 항목과 시각화 방안을 제시합니다.
