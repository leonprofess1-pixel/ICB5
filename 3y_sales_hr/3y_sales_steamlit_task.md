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
  - `💎 성과 관리 심층 분석`
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
        - **문제**: 3명 중 1명이 3년 내 퇴사하는 심각한 인력 누수, 특히 **성과가 좋은 핵심인재의 이탈**이 문제.
        - **핵심 원인**: **(1) 성과에 대한 불합리한 보상**, **(2) 성장 기대감 부재**, **(3) 고성과자의 번아웃**이 복합적으로 작용.
        - **Top 제안**: 성과 등급과 연동된 **차등 연봉 인상률 테이블**을 즉시 도입하고, 고성과자에 대한 **Fast-Track 승진 경로**를 신설.
    3. **이탈 현황 (Pie Chart)**: 이탈/잔류 비율 시각화.

### 💰 보상 문제 분석
- **목표**: '낮은 보상'이 이탈의 가장 큰 동인임을 입증하고, 문제의 깊이를 다각도로 보여준다.
- **콘텐츠 (Tabs)**:
    1. **직무별 소득 격차 (Violin Plot)**: `JobRole`별 `MonthlyIncome` 분포를 `Attrition`으로 비교.
        - **인사이트**: 이탈 문제는 'Sales Representative' 직급에 집중된 '저임금' 문제임.
        - **액션플랜**: 'Sales Rep.' 초임 연봉 시장 상위 25% 수준으로 인상 검토.
    2. **소득 대비 만족도 (Scatter Plot)**: X축 `MonthlyIncome`, Y축 `JobSatisfaction`, 색상 `Attrition`.
        - **인사이트**: 소득이 낮으면서 직무 만족도까지 낮은 그룹에서 이탈이 집중됨. '적게 벌고 만족도도 낮은' 직원들이 회사를 떠나고 있음.
        - **액션플랜**: 저연차 직원들의 만족도에 영향을 미치는 비금전적 요인(업무 자율성, 인정 문화 등)을 함께 개선.
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

### 💎 성과 관리 심층 분석
- **목표**: 현재의 성과 평가 및 보상 시스템이 **핵심 인재를 유지**하고 동기를 부여하는 데 효과적인지 진단하고, 고성과자 이탈의 근본 원인을 규명한다.
- **콘텐츠 (Tabs)**:
    1. **성과 등급별 이탈 현황 (Bar Chart)**: `PerformanceRating`별 이탈자/잔류자 수를 비교.
        - **진단**: 놀랍게도 최고 성과 그룹(4등급)에서 상당수의 이탈이 발생. 이는 **성과가 좋은 직원이라고 해서 회사에 만족하고 남아있지 않다**는 심각한 신호.
        - **액션플랜**: 고성과자 그룹의 이탈 원인을 다른 각도에서 심층적으로 분석할 필요성 제기.
    2. **성과와 보상의 실패 (Violin Plot)**: X축 `PerformanceRating`, Y축 `PercentSalaryHike`, `Attrition`으로 그룹 분리.
        - **진단**: **성과 관리의 핵심 실패 지점.** 최고 성과(4등급)를 받은 직원의 연봉 인상률 분포가 3등급과 큰 차이가 없음. '열심히 일할수록 손해'라는 인식이 팽배할 수밖에 없는 구조.
        - **액션플랜**: 성과 등급과 연봉 인상률을 **명확하고 예측 가능하게** 연동. `4등급: 15% 이상`, `3등급: 8~14%` 등 차등 보상안 즉시 마련.
    3. **고성과는 번아웃의 다른 이름인가? (Sunburst Chart)**: `PerformanceRating` -> `OverTime` -> `Attrition` 순으로 고성과 그룹(3, 4등급)의 이탈 경로 탐색.
        - **진단**: 성과가 좋은 직원일수록 야근(`OverTime`) 비율이 높으며, **'고성과 + 야근' 그룹에서 이탈이 집중**됨. 회사는 이들의 추가 근무를 성과 창출의 당연한 요소로 여기고, 합당한 보상이나 인정에는 실패하고 있음.
        - **액션플랜**: 고성과 그룹의 야근 현황을 HR 차원에서 면밀히 모니터링. 야근 시간에 비례하는 **추가 보상(특별 인센티브, 유급 휴가)을 제도화**하여 번아웃을 방지하고 로열티를 높여야 함.
    4. **고성과 이탈자 프로파일 (Parallel Categories Plot)**: 이탈한 고성과자(`PerformanceRating` 4등급 & `Attrition` 'Yes') 그룹의 특성을 `JobRole`, `YearsSinceLastPromotion`, `JobSatisfaction`으로 연결하여 분석.
        - **진단**: 우리가 놓치고 있는 핵심 인재는 **'승진이 정체된(0~1년) Sales Representative'** 이며, 이들은 **'성과는 최고지만, 직무 만족도는 낮은'** 상태로 회사를 떠나고 있음.
        - **액션플랜**: 'Sales Rep.' 직급의 고성과자에 대한 **Fast-Track 승진 제도** 도입 검토. 분기별 1:1 면담을 통해 직무 만족도 저하 요인을 선제적으로 파악하고 해결.

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
| **상** | **성과/보상** | **불합리한 고과 보상 시스템**<br>고성과/저성과자 간 보상 차이 부재 | 1. **성과연동 연봉인상률 차등 적용** (4등급: 15%+, 3등급: 8~14%)<br>2. Sales Rep. 초임 연봉 테이블 15% 인상 | 핵심인재 이탈 방지, 공정한 보상 문화 정착, 채용 경쟁력 확보 |
| **중** | **성장/경력** | **고성과자의 성장 정체**<br>승진 누락 및 불투명한 커리어 경로 | 1. **고성과자 Fast-Track 승진 제도** 도입<br>2. 경력직 채용 시 총 경력 고려한 직급/연봉 재산정 | 성장 비전 제시, 내부 동기 강화, 잠재 리더 육성 |
| **하** | **업무환경** | **고성과자의 번아웃**<br>과도한 야근 및 출장에 대한 보상 부재 | 1. 야근/출장 그룹에 대한 **추가 보상 의무화** (마일리지, 대체휴가 등)<br>2. Pulse Survey를 통한 **이탈 위험군 조기 경보 및 케어** | 워라밸 개선, 조직 만족도 향상, 장기근속 유도 |

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
    df = pd.read_csv("HR-Employee-Attrition.csv") # 파일 경로는 실제 위치에 맞게 수정
    df_sales = df[(df['Department'] == 'Sales') & (df['YearsAtCompany'] <= 3)].copy()
    # 파생 변수 생성
    df_sales['Attrition_Kor'] = df_sales['Attrition'].apply(lambda x: '이탈' if x == 'Yes' else '잔류')
    df_sales['PerformanceRating_Kor'] = df_sales['PerformanceRating'].map({1: 'Low', 2: 'Good', 3: 'Excellent', 4: 'Outstanding'})
    return df_sales

df = load_data()

# 사이드바
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["요약", "보상 문제 분석", "성장 정체 분석", "업무 환경 분석", "성과 관리 심층 분석", "데이터 직접 탐색", "최종 제언"])

# 페이지 함수 정의
def show_summary(df):
    st.title("📄 요약: Sales 저연차 이탈 현황")
    # ... 구현 ...

def show_compensation_analysis(df):
    st.title("💰 보상 문제 분석")
    # ... Tabs 및 Violin, Scatter, Box Plot 구현 ...

def show_growth_analysis(df):
    st.title("📈 성장 정체 분석")
    # ... Tabs 및 Bar, Scatter, Histogram 구현 ...

def show_environment_analysis(df):
    st.title("🌿 업무 환경 분석")
    # ... Tabs 및 2D Density, Bar Chart, Histogram 구현 ...

def show_performance_analysis(df):
    st.title("💎 성과 관리 심층 분석")
    # ... Tabs 및 Bar, Violin, Sunburst, Parallel Categories 구현 ...

def show_explorer(df):
    st.title("🔎 데이터 직접 탐색")
    # ... Sidebar 필터 및 DataFrame 구현 ...

def show_recommendations():
    st.title("🎯 최종 제언: 실행 중심 Action Plan")
    # ... Markdown 테이블 구현 ...

# 페이지 라우팅
page_map = {
    "요약": show_summary,
    "보상 문제 분석": show_compensation_analysis,
    "성장 정체 분석": show_growth_analysis,
    "업무 환경 분석": show_environment_analysis,
    "성과 관리 심층 분석": show_performance_analysis,
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