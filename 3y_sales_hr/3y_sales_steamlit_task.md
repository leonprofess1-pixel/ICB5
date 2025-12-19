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
  - `🌊 고성과자 생애주기 분석`
  - `🎯 최종 제언`
- **데이터**: `HR-Employee-Attrition.csv`에서 `Department`='Sales', `YearsAtCompany`<=3 필터링. `@st.cache_data` 사용.

---

## 4. 페이지별 상세 명세

### 📄 요약
- **목표**: 대시보드의 핵심 결론을 가장 먼저 제시하여, 바쁜 의사결정자가 1분 안에 상황을 파악할 수 있도록 한다.
- **콘텐츠**:
    1. **핵심 지표**: 이탈률(34.1%), 분석 대상 인원, 이탈 인원.
    2. **Executive Summary**:
        - **문제**: 3명 중 1명이 3년 내 퇴사하는 심각한 인력 누수, 특히 **미래 성장 동력인 고성과자의 이탈**이 가속화.
        - **핵심 원인**: **(1) 보상의 비현실성**, **(2) 성장의 불확실성**, **(3) 성과 창출 과정의 소진(Burnout)**.
        - **Top 제안**: 고성과자 그룹의 **기본 연봉 테이블(Salary Band) 재설계** 및 **'재충전 안식월(Sabbatical)' 제도** 도입.
    3. **이탈 현황 (Pie Chart)**: 이탈/잔류 비율 시각화.

### 💰 보상 문제 분석
- **목표**: '낮은 보상'이 이탈의 가장 큰 동인임을 입증하고, 문제의 깊이를 다각도로 보여준다.
- **콘텐츠 (Tabs)**:
    1. **직무별 소득 격차 (Violin Plot)**: `JobRole`별 `MonthlyIncome` 분포를 `Attrition`으로 비교.
        - **인사이트**: 이탈 문제는 'Sales Representative' 직급에 집중된 '저임금' 문제임.
        - **액션플랜**: 'Sales Rep.' 초임 연봉 시장 상위 25% 수준으로 인상 검토.
    2. **야근과 보상 (Box Plot)**: `OverTime` 유무에 따른 `MonthlyIncome` 분포를 `Attrition`으로 비교.
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

### 🌿 업무 환경 분석
- **목표**: 물리적, 심리적 업무 환경이 이탈에 미치는 영향을 분석한다.
- **콘텐츠 (Tabs)**:
    1. **만족도 매트릭스 (2D Density Plot)**: X축 `JobSatisfaction`, Y축 `EnvironmentSatisfaction`, 이탈자/잔류자 그룹으로 나누어 밀도 시각화.
        - **인사이트**: 업무와 환경 만족도가 모두 낮은 '위험 영역'(좌하단)에 이탈자들이 집중 분포.
        - **액션플랜**: 분기별 직원 만족도 설문(Pulse Survey)을 통해 '위험 영역' 직원 조기 발견 및 HRBP 집중 면담.
    2. **출장과 워라밸 (Faceted Bar Chart)**: `BusinessTravel` 빈도와 `WorkLifeBalance` 점수를 조합하여 그룹별 이탈률 막대그래프로 비교.
        - **인사이트**: '잦은 출장' 그룹의 워라밸 점수가 가장 낮으며, 이 그룹의 이탈률이 가장 높음. 출장이 워라밸 붕괴와 이탈의 직접적 원인.
        - **액션플랜**: 불필요한 출장을 줄이기 위한 '원격 회의 우선 정책' 도입. 잦은 출장 직원에 대한 '출장 마일리지' 및 '대체 휴가' 제공.

### 🌊 고성과자 생애주기 분석 (High-Performer Lifecycle Analysis)
- **목표**: 고성과 직원의 입사부터 이탈까지의 여정(Journey)을 추적하여, 단계별 핵심적인 이탈 위험 요인을 식별하고 선제적인 인재 유지 전략을 수립한다.
- **콘텐츠 (Tabs)**:
    1. **누가 고성과를 내는가? (Who are the High-Performers?)**: `JobRole` 대비 `PerformanceRating` 분포를 통해, 어떤 직무에서 고성과자가 주로 나타나는지 확인.
        - **진단**: 고성과자는 대부분 'Sales Representative' 직급에 집중되어 있음. 이는 해당 직급이 우리 회사의 핵심적인 가치 창출 그룹임을 의미.
        - **액션플랜**: 고성과 Sales Rep. 그룹에 대한 유지(Retention) 전략을 최우선 순위로 설정.
    2. **고성과자의 보상 현실 (Compensation Reality)**: `PerformanceRating`별 `MonthlyIncome` 분포를 이탈 여부로 비교.
        - **진단**: 최고 성과(Outstanding)를 내는 직원의 월 소득 중앙값이, 바로 아래 등급(Excellent)과 큰 차이가 없음. 절대적인 소득 수준 자체가 고성과에 대한 기대치를 충족시키지 못하고 있음.
        - **액션플랜**: 연봉 인상률だけでなく, 고성과자 그룹의 기본 연봉 테이블(Salary Band) 자체를 시장 최상위 수준으로 재설계하여, 업계 최고 대우를 보장.
    3. **성과와 소진의 악순환 (Performance-Burnout Cycle)**: X축 `WorkLifeBalance`, Y축 `PerformanceRating`의 2D 밀도 플롯을 이탈 여부로 비교.
        - **진단**: 이탈하는 고성과자 그룹은 '높은 성과'와 '낮은 워라밸' 영역에 집중적으로 분포. 이는 성과 창출 과정이 개인의 희생과 소진을 담보로 하고 있음을 시사.
        - **액션플랜**: '지속 가능한 성과(Sustainable Performance)' 프로그램을 도입. 특정 기간 이상 고성과를 유지한 직원에 대한 '재충전 안식월(Sabbatical)' 또는 '특별 유급휴가' 부여를 제도화.
    4. **정체된 고성과자의 이탈 경로 (Stagnant High-Performer's Exit Path)**: `PerformanceRating` 4등급 직원의 흐름을 `YearsSinceLastPromotion` -> `JobSatisfaction` -> `Attrition` 순으로 Sankey 다이어그램으로 시각화.
        - **진단**: '최고 성과자' 중 '승진 못한 지 1년 이상'된 그룹의 80%가 '낮은 직무 만족도'를 보이며, 이들 중 대부분이 결국 '이탈'로 이어지는 명확한 경로 확인.
        - **액션플랜**: HR 시스템 내에 **'고성과자 승진 정체 알림(Stagnation Alert)'** 기능 개발. 최고 등급 성과자가 18개월 이상 승진하지 못할 경우, 담당 HRBP와 임원에게 자동 알림이 가고, 해당 직원에 대한 의무적인 커리어 개발 면담을 진행.

### 🎯 최종 제언
- **목표**: 모든 분석을 바탕으로, 즉시 실행할 수 있는 우선순위별 최종 액션 플랜을 제시한다.
- **콘텐츠 (전문가 제언 형식)**:
    - **P1 (즉시 실행): 보상 체계의 근본적 혁신**
        - **진단**: 현재 보상 시스템은 고성과 인재 유치 및 유지에 완전히 실패했습니다.
        - **액션**: 
            1. **고성과자 Salary Band 재설계**: Sales Rep. 고성과자 그룹의 기본 연봉을 시장 상위 10% 수준으로 상향 조정합니다.
            2. **성과 기반 인상률 차등**: 4등급(Outstanding) 성과자에 대해 최소 15% 이상의 연봉 인상을 보장하는 규정을 신설합니다.
    - **P2 (중기 과제): '성장 정체' 해소를 위한 제도적 지원**
        - **진단**: 승진 정체는 고성과자의 동기 부여를 저해하는 가장 큰 장애물입니다.
        - **액션**:
            1. **Fast-Track 승진 제도 도입**: 2년 연속 최고 등급 성과자는 다음 직급으로 즉시 승진 심사 자격을 부여합니다.
            2. **'성장 정체 알림' 시스템**: 18개월 이상 승진이 없는 고성과자를 시스템이 자동 식별하여 HRBP에게 통보, 의무적으로 커리어 코칭을 진행하게 합니다.
    - **P3 (장기 과제): 지속가능한 성과 문화를 위한 투자**
        - **진단**: 현재의 성과는 직원의 '소진(burnout)'을 대가로 이루어지고 있어 장기적으로 위험합니다.
        - **액션**:
            1. **'재충전 안식월' 도입**: 3년 이상 연속 고성과자에게 1개월의 유급 안식월을 부여하여 재충전과 자기계발 기회를 제공합니다.
            2. **Pulse Survey 정례화**: 분기별 익명 설문을 통해 이탈 위험군을 조기에 발견하고 선제적으로 지원합니다.

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
page = st.sidebar.radio("페이지 선택", ["요약", "보상 문제 분석", "성장 정체 분석", "업무 환경 분석", "고성과자 생애주기 분석", "최종 제언"])

# 페이지 함수 정의
def show_summary(df):
    st.title("📄 요약: Sales 저연차 이탈 현황")
    # ... 구현 ...

def show_compensation_analysis(df):
    st.title("💰 보상 문제 분석")
    # ... Tabs 구현 ...

def show_growth_analysis(df):
    st.title("📈 성장 정체 분석")
    # ... Tabs 구현 ...

def show_environment_analysis(df):
    st.title("🌿 업무 환경 분석")
    # ... Tabs 구현 ...

def show_lifecycle_analysis(df):
    st.title("🌊 고성과자 생애주기 분석")
    # ... Tabs 및 Bar, Violin, 2D Density, Sankey 구현 ...

def show_recommendations():
    st.title("🎯 최종 제언: 실행 중심 Action Plan")
    # ... 전문가 제언 형식으로 구현 ...

# 페이지 라우팅
page_map = {
    "요약": show_summary,
    "보상 문제 분석": show_compensation_analysis,
    "성장 정체 분석": show_growth_analysis,
    "업무 환경 분석": show_environment_analysis,
    "고성과자 생애주기 분석": show_lifecycle_analysis,
    "최종 제언": show_recommendations
}

# 함수 호출
selected_function = page_map[page]
if page == "최종 제언":
    selected_function()
else:
    selected_function(df)

```