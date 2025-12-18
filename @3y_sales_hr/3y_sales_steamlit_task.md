# [작업 지시서] Sales 부서 저연차 이탈 요인 심층 분석 및 대시보드 개발

## 1. 프로젝트 목표
근속 3년 이하 Sales 부서의 높은 이탈률(34.1%)에 대한 원인을 다각적으로 심층 분석하고, 경영진과 HR 부서가 데이터에 기반하여 **즉각적인 개선 조치**를 취할 수 있도록 지원하는 **전략적 의사결정 지원 대시보드**를 개발한다.

## 2. 핵심 요구사항
- **전문가 수준의 분석**: 단순 현상 나열을 넘어, 변수 간의 복합적인 상호작용을 분석하여 이탈의 근본적인 '왜'를 밝힌다.
- **스토리텔링 기반의 구조**: '보상', '성장', '업무 환경' 등 명확한 비즈니스 문제 테마를 중심으로 분석 내용을 조직화하여 설득력 있는 내러티브를 제공한다.
- **12가지 이상의 다각적 시각화**: Violin, Scatter, Box, Bar, Heatmap, Histogram, Waterfall, Sunburst, 2D Density, Parallel Categories 등 다양한 차트를 활용하여 데이터를 입체적으로 조망한다.
- **실행 중심의 제언**: 모든 분석은 구체적인 '비즈니스 인사이트'와 즉시 실행 가능한 '액션 플랜'으로 귀결되어야 하며, 최종적으로 우선순위가 포함된 종합 제언을 제시한다.

---

## 3. 대시보드 구조 설계
- **사이드바 내비게이션**: 분석 테마에 따라 페이지를 명확히 구분한다.
  - `📄 요약`
  - `💰 보상 문제 분석`
  - `📈 성장 정체 분석`
  - `🌿 업무 환경 분석`
  - `🔍 종합 진단`
  - `🔎 데이터 직접 탐색`
  - `🎯 최종 제언`
- **데이터**: `HR-Employee-Attrition.csv`에서 `Department`='Sales', `YearsAtCompany`<=3 필터링. `@st.cache_data` 사용.

---

## 4. 페이지별 상세 명세

### 📄 요약
- **목표**: 대시보드의 핵심 결론을 가장 먼저 제시하여, 바쁜 의사결정자가 1분 안에 상황을 파악할 수 있도록 한다.
- **콘텐츠**:
    1. **핵심 지표**: 이탈률(34.1%), 분석 대상 인원, 이탈 인원.
    2. **Executive Summary**:
        - **문제**: 3명 중 1명이 3년 내 퇴사하는 심각한 인력 누수.
        - **핵심 원인**: **(1) 보상 불만**, **(2) 성장 기대감 부재**, **(3) 과도한 업무 부담**이 복합적으로 작용.
        - **Top 제안**: `Sales Representative` 직급의 초임 연봉 현실화 및 성과 기반 인상률 차등 적용.
    3. **이탈 현황 (Pie Chart)**: 이탈/잔류 비율 시각화.

### 💰 보상 문제 분석
- **목표**: '낮은 보상'이 이탈의 가장 큰 동인임을 입증하고, 문제의 깊이를 다각도로 보여준다.
- **콘텐츠 (Tabs)**:
    1. **직무별 소득 격차 (Violin Plot)**: `JobRole`별 `MonthlyIncome` 분포를 `Attrition`으로 비교.
        - **인사이트**: 이탈 문제는 'Sales Representative' 직급에 집중된 '저임금' 문제임.
        - **액션플랜**: 'Sales Rep.' 초임 연봉 시장 상위 25% 수준으로 인상 검토.
    2. **성과 보상의 실패 (Box Plot)**: `PerformanceRating`별 `PercentSalaryHike` 분포를 `Attrition`으로 비교.
        - **인사이트**: 최고 성과(4등급)를 받아도 연봉 인상률은 3등급과 차이가 없으며, 이는 고성과자의 이탈을 유발. '성과에 대한 보상' 시스템이 작동하지 않음.
        - **액션플랜**: 성과 등급별 연봉 인상률 하한선 차등 설정 (e.g., 4등급: 최소 15% 이상).
    3. **야근과 보상 (Box Plot)**: `OverTime` 유무에 따른 `MonthlyIncome` 분포를 `Attrition`으로 비교.
        - **인사이트**: 야근하는 그룹의 소득 중앙값이 야근 안하는 그룹보다 낮음. 즉, '적게 버는 직원이 야근까지 하고' 있으며, 이 그룹에서 이탈이 심각.
        - **액션플랜**: 야근 수당 현실화 및 포괄임금제 재검토.

### 📈 성장 정체 분석
- **목표**: 직원들이 '성장의 한계'를 느끼고 떠나는 과정을 시각적으로 보여준다.
- **콘텐츠 (Tabs)**:
    1. **승진의 정체 (Bar Chart)**: `YearsSinceLastPromotion` 그룹별 이탈률을 시각화.
        - **인사이트**: 승진 없이 1년만 지나도 이탈률이 급증. 승진 경험 부재가 퇴사의 결정적 계기가 됨.
        - **액션플랜**: 입사 2년차 자동 승진 심사(역량 미달 시에만 탈락) 제도 도입.
    2. **경력과 직급의 미스매치 (Scatter Plot)**: X축 `TotalWorkingYears`, Y축 `JobLevel`, 색상 `Attrition`.
        - **인사이트**: 총 경력(타사 경력 포함)이 많음에도 낮은 직무 레벨(1, 2)에 머물러 있는 '과소평가' 그룹에서 이탈이 두드러짐.
        - **액션플랜**: 경력직 채용 시, 총 경력을 고려한 직무 레벨 및 연봉 재산정 프로세스 마련.
    3. **교육 기회의 불균형 (Histogram)**: `TrainingTimesLastYear` 분포를 `Attrition`으로 비교.
        - **인사이트**: 이탈자 그룹이 잔류자 그룹에 비해 작년 교육 횟수가 현저히 적음. '회사로부터 투자받지 못한다'는 인식이 이탈을 촉진.
        - **액션플랜**: 전 직원 대상 연간 최소 교육 시간(e.g., 20시간) 보장 및 교육 이력과 승진 심사 연계.

### 🌿 업무 환경 분석
- **목표**: 물리적, 심리적 업무 환경이 이탈에 미치는 영향을 분석한다.
- **콘텐츠 (Tabs)**:
    1. **만족도 매트릭스 (2D Density Plot)**: X축 `JobSatisfaction`, Y축 `EnvironmentSatisfaction`, 이탈자/잔류자 그룹으로 나누어 밀도 시각화.
        - **인사이트**: 업무와 환경 만족도가 모두 낮은 '위험 영역'(좌하단)에 이탈자들이 집중 분포.
        - **액션플랜**: 분기별 직원 만족도 설문(Pulse Survey)을 통해 '위험 영역' 직원 조기 발견 및 HRBP 집중 면담.
    2. **출장과 워라밸 (Faceted Bar Chart)**: `BusinessTravel` 빈도와 `WorkLifeBalance` 점수를 조합하여 그룹별 이탈률 막대그래프로 비교.
        - **인사이트**: '잦은 출장' 그룹의 워라밸 점수가 가장 낮으며, 이 그룹의 이탈률이 가장 높음. 출장이 워라밸 붕괴와 이탈의 직접적 원인.
        - **액션플랜**: 불필요한 출장을 줄이기 위한 '원격 회의 우선 정책' 도입. 잦은 출장 직원에 대한 '출장 마일리지' 및 '대체 휴가' 제공.
    3. **동료 관계와 이탈 (Histogram)**: `RelationshipSatisfaction` 점수 분포를 `Attrition`으로 비교.
        - **인사이트**: 동료 관계 만족도는 이탈에 큰 영향을 주지 않음. 직원들은 '사람'보다는 '보상'과 '성장' 때문에 떠남.
        - **액션플랜**: 조직 활성화(Team Building) 예산을 줄이고, 해당 예산을 직접 보상이나 성장 지원 프로그램으로 전환하는 것을 고려.

### 🔍 종합 진단
- **목표**: 주요 변수들의 관계를 종합적으로 진단하고, 이탈자 프로필을 시각화한다.
- **콘텐츠 (Tabs)**:
    1. **주요 변수 상관관계 (Heatmap)**: 주요 수치형 변수 간의 상관관계 행렬 시각화.
        - **인사이트**: 이탈(`Attrition`)은 '월 소득', '직무 레벨', '총 경력', '나이'와 강한 음의 상관관계를 보임. 젊고, 경력 짧고, 직급 낮고, 돈 못 버는 직원이 떠남.
    2. **핵심 이탈 동인 (Waterfall Chart)**: '저소득', '승진 정체', '과도한 야근', '낮은 만족도' 등이 이탈에 얼마나 기여하는지 시각화.
        - **인사이트**: '보상'과 '성장' 문제가 이탈 원인의 70% 이상을 차지하는 핵심 동인임을 재확인.
    3. **이탈자 프로필 시각화 (Parallel Categories Plot)**: `JobRole` -> `OverTime` -> `JobSatisfaction` -> `Attrition` 순서로 직원의 이탈 경로를 시각화.
        - **인사이트**: 'Sales Rep.'이면서 '야근'을 하고 '업무 만족도'가 낮은 직원이 '이탈'로 귀결되는 전형적인 경로를 시각적으로 확인.

### 🔎 데이터 직접 탐색
- **목표**: HR 담당자가 직접 데이터를 필터링하며 가설을 검증하고 특정 직원 그룹을 식별할 수 있도록 지원.
- **콘텐츠**:
  - **사이드바 필터**: 직무, 이탈여부, 월소득, 업무 만족도, 성과 등급 등 주요 변수 필터.
  - **데이터 테이블**: 필터링된 결과를 `st.dataframe`으로 표시.

### 🎯 최종 제언
- **목표**: 모든 분석을 바탕으로, 즉시 실행할 수 있는 우선순위별 최종 액션 플랜을 제시한다.
- **콘텐츠 (Markdown Table)**:
| 우선순위 | 영역 | 핵심 문제 | 제안 액션 | 기대 효과 |
|:---:|:---|:---|:---|:---|
| **상** | 보상 | Sales Rep. 저임금 및 불합리한 성과 보상 | 1. 초임 연봉 테이블 15% 인상<br>2. 성과 등급별 연봉 인상률 차등 적용 | 핵심인재 이탈 방지, 신규 채용 경쟁력 확보 |
| **중** | 성장 | 승진 정체 및 불투명한 커리어 경로 | 1. 2년차 자동 승진 심사 제도화<br>2. 경력직 채용 시 경력 인정 강화 | 성장 기대감 부여, 내부 동기 강화 |
| **하** | 환경 | 과도한 업무 부담(야근, 출장) | 1. 야근/출장 그룹 추가 보상 의무화<br>2. Pulse Survey를 통한 위험군 조기 경보 | 번아웃 방지, 조직 만족도 개선 |

---

## 5. 구현 가이드 (Code Skeleton)
```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales 이탈 분석", layout="wide")

@st.cache_data
def load_data():
    # 데이터 로딩 및 전처리
    df = pd.read_csv("3y_sales_hr/HR-Employee-Attrition.csv")
    df_sales = df[(df['Department'] == 'Sales') & (df['YearsAtCompany'] <= 3)].copy()
    # 파생 변수 생성
    df_sales['Attrition_Kor'] = df_sales['Attrition'].apply(lambda x: '이탈' if x == 'Yes' else '잔류')
    return df_sales

df = load_data()

# 사이드바
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["요약", "보상 문제 분석", "성장 정체 분석", "업무 환경 분석", "종합 진단", "데이터 직접 탐색", "최종 제언"])

# 페이지 함수 정의
def show_summary(df):
    st.title("📄 요약")
    # ... 구현 ...

def show_compensation_analysis(df):
    st.title("💰 보상 문제 분석")
    # ... Tabs 및 Violin, Box, Scatter Plot 구현 ...

def show_growth_analysis(df):
    st.title("📈 성장 정체 분석")
    # ... Tabs 및 Bar, Scatter, Histogram 구현 ...

def show_environment_analysis(df):
    st.title("🌿 업무 환경 분석")
    # ... Tabs 및 2D Density, Bar Chart, Histogram 구현 ...

def show_holistic_analysis(df):
    st.title("🔍 종합 진단")
    # ... Tabs 및 Heatmap, Waterfall, Parallel Categories 구현 ...

def show_explorer(df):
    st.title("🔎 데이터 직접 탐색")
    # ... Sidebar 필터 및 DataFrame 구현 ...

def show_recommendations():
    st.title("🎯 최종 제언")
    # ... Markdown 테이블 구현 ...

# 페이지 라우팅
page_map = {
    "요약": show_summary,
    "보상 문제 분석": show_compensation_analysis,
    "성장 정체 분석": show_growth_analysis,
    "업무 환경 분석": show_environment_analysis,
    "종합 진단": show_holistic_analysis,
    "데이터 직접 탐색": show_explorer,
    "최종 제언": show_recommendations
}

# 함수 호출
selected_function = page_map[page]
if page == "최종 제언":
    selected_function()
else:
    selected_function(df)

```