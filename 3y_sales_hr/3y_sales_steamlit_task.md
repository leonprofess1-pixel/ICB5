# 3y_sales_steamlit_task.py
# Streamlit 대시보드 개발을 위한 작업 명세서

"""
## 목표
- 'HR_Sales_Attrition_Report_v2.md' 보고서의 분석 내용을 기반으로,インタラクティブ한 Streamlit 대시보드를 개발합니다.
- 사용자가 데이터를 직접 탐색하고, 이탈 요인에 대한 깊은 인사이트를 얻을 수 있도록 시각화와 필터링 기능을 제공합니다.

## 개발 요구사항

### 1. 기본 구조
- **페이지 설정**: `st.set_page_config`를 사용하여 페이지 제목, 아이콘, 레이아웃(wide)을 설정합니다.
- **사이드바 내비게이션**: `st.sidebar`를 사용하여 대시보드의 각 분석 섹션으로 이동할 수 있는 메뉴를 만듭니다.
    - 메뉴 항목: "요약", "소득과 만족도", "직무/경력 분석", "성과/평가 분석", "종합 제언" 등 보고서 목차에 따라 구성합니다.
- **데이터 로딩**:
    - `HR-Employee-Attrition.csv` 파일을 로드하고, 보고서와 동일하게 근속 3년 이하 Sales 부서 데이터만 필터링합니다.
    - 데이터 로딩 함수는 `@st.cache_data` 데코레이터를 사용하여 성능을 최적화합니다.

### 2. 페이지별 콘텐츠

#### 2.1. 요약 (Executive Summary)
- **페이지 제목**: `st.title`로 "근속 3년 이하 Sales 직원 이탈 분석 대시보드"를 표시합니다.
- **핵심 지표**: `st.metric`을 사용하여 주요 지표를 시각적으로 강조합니다.
    - 전체 직원 수
    - 이탈 직원 수
    - 이탈률 (33.3%)
- **보고서 요약**: `Executive Summary`의 내용을 `st.markdown`과 `st.expander`를 사용하여 깔끔하게 정리하여 보여줍니다.
- **전체 이탈 현황**: `10_attrition_overview.png` (파이 차트)를 `st.image`로 표시하고, 관련 분석 내용을 텍스트로 제공합니다.

#### 2.2. 소득과 만족도 분석
- **섹션 제목**: `st.header` 또는 `st.subheader`로 "소득과 만족도가 이탈에 미치는 영향"을 표시합니다.
- **시각화**:
    - **[필수]** '월 소득과 업무 만족도' 박스 플롯 (`1_income_satisfaction_attrition.png`)을 `st.image`로 표시합니다.
    - **[선택]** 원본 데이터를 사용하여 Plotly로 동일한 차트를 직접 그려インタラクティブ 기능을 추가합니다.
- **필터링 기능**:
    - `st.selectbox`를 만들어 '업무 만족도' 등급(1, 2, 3, 4)을 선택하면 해당 그룹의 데이터만 하이라이트 되거나 필터링되어 보이도록 구현합니다.
- **분석 내용**: 보고서의 '관찰', '인사이트', '액션 플랜'을 `st.expander` 내에 텍스트로 정리합니다.
- **관련 분석 추가**:
    - '출장 빈도와 월 소득' (`6_travel_income_attrition.png`)
    - '학력 분야별 월 소득' (`8_education_income_attrition.png`)
    - 각 차트와 분석 내용을 함께 제공합니다.

#### 2.3. 직무/경력 분석
- **섹션 제목**: "직무 및 경력 경로 분석"
- **시각화 및 내용**:
    - **직무 레벨별 소득**: `2_jobrole_income_attrition.png` (바이올린 플롯) 및 관련 분석 내용 표시.
    - **연령 및 총 경력**: `3_age_workyears_attrition.png` (산점도) 및 관련 분석 내용 표시.
    - **승진 경험**: `4_promotion_joblevel_attrition.png` (카운트 플롯) 및 관련 분석 내용 표시.
- **インタラクティブ 요소**:
    - '직무(JobRole)'를 선택할 수 있는 `st.multiselect` 필터를 추가하여 특정 직무 그룹의 데이터만 동적으로 시각화합니다.
    - '승진 경험 유무'에 따라 데이터를 필터링하는 `st.radio` 버튼을 제공합니다.

#### 2.4. 성과/평가 분석
- **섹션 제목**: "성과 및 만족도 평가 분석"
- **시각화 및 내용**:
    - **성과 등급과 이탈률**: `11_performance_rating_attrition.png` (막대 차트)를 표시하고, '성과 등급이 이탈에 영향을 주지 못한다'는 핵심 메시지를 강조합니다.
    - **종합 만족도**: `5_satisfaction_scores.png` (히스토그램)를 표시하고, 종합 만족도 점수에 따른 이탈 경향을 설명합니다.
- **インタラクティブ 요소**:
    - '성과 등급'을 선택하면 해당 등급 직원들의 다른 특성(예: 월소득, 만족도) 분포를 볼 수 있는 동적 차트를 추가합니다.

#### 2.5. 종합 제언
- **섹션 제목**: "종합 제언 및 액션 플랜"
- **내용**: 보고서의 '종합 제언' 테이블을 `st.markdown`을 사용하여 보기 좋게 렌더링합니다.
- 각 제언(보상, 성장, 문화)을 `st.tabs`로 구분하여 제시하는 것을 고려합니다.

### 3. 코드 구조 (구현 가이드)

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. 기본 설정 및 데이터 로딩 ---
st.set_page_config(page_title="Sales 부서 이탈 분석", layout="wide")

@st.cache_data
def load_data():
    """CSV 파일을 로드하고 초기 필터링을 수행하는 함수"""
    df_raw = pd.read_csv("3y_sales_hr/HR-Employee-Attrition.csv")
    # 보고서와 동일한 조건으로 데이터 필터링
    df_filtered = df_raw[(df_raw['Department'] == 'Sales') & (df_raw['YearsAtCompany'] <= 3)].copy()
    # 분석에 필요한 파생 변수 추가
    df_filtered['Attrition_Kor'] = df_filtered['Attrition'].apply(lambda x: '이탈' if x == 'Yes' else '잔류')
    return df_filtered

df = load_data()

# --- 2. 사이드바 내비게이션 ---
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["요약", "소득과 만족도", "직무와 경력", "성과와 평가", "종합 제언"])

# --- 3. 페이지별 함수 정의 ---

def show_summary():
    """요약 페이지 표시 함수"""
    st.title("근속 3년 이하 Sales 직원 이탈 분석")
    
    # 핵심 지표 표시
    total_employees = len(df)
    attrition_count = len(df[df['Attrition'] == 'Yes'])
    attrition_rate = (attrition_count / total_employees) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("전체 직원", f"{total_employees} 명")
    col2.metric("이탈 직원", f"{attrition_count} 명")
    col3.metric("이탈률", f"{attrition_rate:.1f} %")

    # Executive Summary 표시
    st.subheader("Executive Summary")
    with st.expander("자세히 보기"):
        st.markdown("""
        - **핵심 동인**: 낮은 보상, 성장 정체, 직무 불만족
        - **핵심 제안**: 초임 연봉 현실화, 명확한 커리어 패스 제시
        """)

    # 전체 이탈 현황 차트
    st.subheader("전체 이탈 현황")
    st.image("3y_sales_hr/images_v2/10_attrition_overview.png")
    st.info("3명 중 1명 이상이 3년을 채우지 못하고 퇴사하는 심각한 상황입니다.")

def show_income_satisfaction():
    """소득/만족도 분석 페이지"""
    st.title("소득과 만족도 분석")

    st.subheader("1. 월 소득과 업무 만족도")
    st.image("3y_sales_hr/images_v2/1_income_satisfaction_attrition.png")
    with st.expander("분석 내용"):
        st.markdown("""
        - **관찰**: 업무 만족도가 낮을수록 이탈 그룹의 월 소득이 현저히 낮음.
        - **인사이트**: 낮은 보상과 낮은 만족도는 강력한 '이탈 시너지'를 발생시킴.
        - **액션 플랜**: '보상-만족도' 위험 그룹(소득 하위 25%, 만족도 1~2점) 우선 면담.
        """)
    # 추가: Plotly로 인터랙티브 차트 구현
    # satisfaction_filter = st.selectbox("업무 만족도 등급으로 필터링:", [None, 1, 2, 3, 4])
    # ... 필터링 로직 ...
    # fig = px.box(df_filtered, x='JobSatisfaction', y='MonthlyIncome', color='Attrition_Kor')
    # st.plotly_chart(fig)

def show_job_career():
    """직무/경력 분석 페이지"""
    st.title("직무와 경력 분석")
    
    st.subheader("1. 직무 레벨별 월 소득")
    st.image("3y_sales_hr/images_v2/2_jobrole_income_attrition.png")
    st.info("'Sales Representative' 직급의 낮은 보상이 핵심 이탈 드라이버입니다.")

    st.subheader("2. 승진 경험과 이탈")
    st.image("3y_sales_hr/images_v2/4_promotion_joblevel_attrition.png")
    st.warning("입사 후 3년 내 승진 경험이 없는 것은 매우 강력한 이탈 신호입니다.")


def show_performance_evaluation():
    """성과/평가 분석 페이지"""
    st.title("성과와 평가 분석")

    st.subheader("1. 성과 등급과 이탈률")
    st.image("3y_sales_hr/images_v2/11_performance_rating_attrition.png")
    with st.expander("분석 내용"):
        st.markdown("""
        - **관찰**: 성과 등급 3(Excellent)과 4(Outstanding) 그룹 간 이탈률 차이가 거의 없음 (약 33%).
        - **인사이트**: 성과 평가가 인재 유지(Retention)에 기여하지 못하고 있음. '우수' 인재마저 이탈.
        - **액션 플랜**: 성과 평가 시스템 전면 재검토 및 상위 등급자에 대한 차별화된 보상/인정 강화.
        """)

def show_recommendations():
    """종합 제언 페이지"""
    st.title("종합 제언")
    st.markdown("""
    | 영역 | 핵심 문제 | 우선순위 | 제안 액션 | 기대 효과 |
    |:---|:---|:---:|:---|:---|
    | **보상 및 인정** | `Sales Rep` 낮은 급여 | **상** | - 초임 연봉 현실화<br>- 성과 기반 인센티브 강화 | 단기 이탈률 감소 |
    | **성장 및 경력** | 불투명한 커리어 패스 | **상** | - 성장 경로 명확화<br>- 조기 승진 제도 도입 | 동기 부여, 성장 기대감 |
    | **업무 환경** | 낮은 만족도, 잦은 출장 | **중** | - 1:1 멘토링 의무화<br>- 출장 규정 재검토 | 조직 적응 지원, 워라밸 개선 |
    """)

# --- 4. 페이지 라우팅 ---
if page == "요약":
    show_summary()
elif page == "소득과 만족도":
    show_income_satisfaction()
elif page == "직무와 경력":
    show_job_career()
elif page == "성과와 평가":
    show_performance_evaluation()
elif page == "종합 제언":
    show_recommendations()

```

## 기대 효과
- 현업 담당자들이 보고서의 핵심 내용을 쉽게 이해하고, 데이터 기반의 의사결정을 내릴 수 있도록 지원합니다.
- 정적 보고서를 넘어,インタラクティブ한 탐색을 통해 새로운 인사이트를 발견할 기회를 제공합니다.
"""
