import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# --- 1. 기본 설정 ---
st.set_page_config(
    page_title="Sales 부서 이탈 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

# --- 2. 데이터 로딩 ---
@st.cache_data
def load_data():
    """CSV 파일을 로드하고 초기 필터링 및 파생 변수를 생성하는 함수"""
    try:
        df_raw = pd.read_csv("3y_sales_hr/HR-Employee-Attrition.csv")
    except FileNotFoundError:
        st.error("Error: HR-Employee-Attrition.csv 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        st.stop()
    
    # 보고서와 동일한 조건으로 데이터 필터링
    df_filtered = df_raw[(df_raw['Department'] == 'Sales') & (df_raw['YearsAtCompany'] <= 3)].copy()
    
    # 분석에 필요한 파생 변수 추가
    df_filtered['Attrition_Kor'] = df_filtered['Attrition'].apply(lambda x: '이탈' if x == 'Yes' else '잔류')
    df_filtered['Attrition_Num'] = df_filtered['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
    df_filtered['Promotion_Status'] = df_filtered['YearsSinceLastPromotion'].apply(lambda x: '승진경험 없음' if x == 0 else '승진경험 있음')

    return df_filtered

df = load_data()

# 이미지 경로 설정
IMG_DIR = "3y_sales_hr/images_v2"

# --- 3. 사이드바 내비게이션 ---
st.sidebar.title("메뉴")
page = st.sidebar.radio(
    "페이지 선택",
    ["요약", "소득과 만족도", "직무와 경력", "성과와 평가", "데이터 탐색", "종합 제언"]
)

# --- 4. 페이지별 함수 정의 ---

def show_summary():
    """요약 페이지 표시 함수"""
    st.title("근속 3년 이하 Sales 직원 이탈 분석 대시보드")
    
    # 핵심 지표 표시
    total_employees = len(df)
    attrition_count = len(df[df['Attrition'] == 'Yes'])
    attrition_rate = (attrition_count / total_employees) * 100

    st.markdown("### 주요 이탈 지표")
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 Sales 직원", f"{total_employees} 명")
    col2.metric("이탈 직원", f"{attrition_count} 명")
    col3.metric("이탈률", f"{attrition_rate:.1f} %")
    st.markdown("---")

    # Executive Summary 표시
    st.header("Executive Summary")
    with st.expander("보고서 요약 보기", expanded=True):
        st.markdown("""
        근속 3년 이하 Sales 부서의 이탈률은 **34.1%**로, 조직 안정성에 심각한 위협이 되고 있습니다. 
        분석 결과, 이탈의 핵심 동인은 다음과 같습니다:
        1.  **낮은 보상 수준:** 특히 'Sales Representative' 직급의 월 소득은 이탈의 가장 강력한 예측 변수입니다.
        2.  **성장 정체에 대한 불안감:** 입사 후 승진 경험이 없는 직원들의 이탈 경향이 뚜렷하게 나타났습니다.
        3.  **직무 불만족:** 낮은 업무 만족도는 이탈과 직접적인 연관이 있으며, 이는 낮은 보상 및 부족한 성장 기회와 상호작용하여 이탈 결정을 증폭시키는 것으로 보입니다.
        """)
    st.markdown("---")

    # 전체 이탈 현황 차트
    st.subheader("전체 이탈 현황 요약")
    st.image(os.path.join(IMG_DIR, "10_attrition_overview.png"), caption="전체 이탈 현황")
    st.info("💡 인사이트: 3명 중 1명 이상이 3년을 채우지 못하고 퇴사하는 심각한 상황입니다.")


def show_income_satisfaction():
    """소득/만족도 분석 페이지"""
    st.title("소득 및 만족도와 이탈의 관계 분석")

    tab1, tab2, tab3 = st.tabs([
        "월 소득과 업무 만족도", 
        "출장 빈도와 월 소득", 
        "학력 분야별 월 소득"
    ])

    with tab1:
        st.subheader("월 소득과 업무 만족도가 이탈에 미치는 영향")
        st.image(os.path.join(IMG_DIR, "1_income_satisfaction_attrition.png"), caption="월 소득과 업무 만족도가 이탈에 미치는 영향 (원본 보고서)")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **관찰**: 업무 만족도가 '1(낮음)'인 그룹에서 이탈자들의 월 소득 중앙값이 잔류자들에 비해 현저히 낮습니다.
            - **인사이트**: 낮은 업무 만족도와 낮은 월 소득은 강력한 '이탈 시너지'를 발생시킵니다.
            - **액션 플랜**: 월 소득 하위 25%이면서 업무 만족도 1~2점인 직원을 대상으로 우선적인 면담 및 케어를 진행합니다.
            """)
        # 인터랙티브 차트 추가
        fig = px.box(df, x='JobSatisfaction', y='MonthlyIncome', color='Attrition_Kor',
                     labels={'JobSatisfaction': '업무 만족도', 'MonthlyIncome': '월 소득', 'Attrition_Kor': '이탈 여부'},
                     color_discrete_map={'잔류': 'skyblue', '이탈': 'salmon'})
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("출장 빈도와 월 소득이 이탈에 미치는 영향")
        st.image(os.path.join(IMG_DIR, "6_travel_income_attrition.png"), caption="출장 빈도와 월 소득이 이탈에 미치는 영향")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **관찰**: 'Travel_Frequently' 그룹에서 이탈자들의 소득이 전반적으로 낮은 구간에 밀집해 있습니다.
            - **인사이트**: 잦은 출장은 '낮은 보상'과 결합될 때 강력한 불만 요인으로 작용합니다.
            - **액션 플랜**: 출장비 규정 현실화 및 대체 근무 옵션 제공.
            """)
            
    with tab3:
        st.subheader("학력 분야별 월 소득과 이탈 현황")
        st.image(os.path.join(IMG_DIR, "8_education_income_attrition.png"), caption="학력 분야별 월 소득과 이탈 현황")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **관찰**: 'Life Sciences'와 'Medical' 분야 전공자들 사이에서 이탈 그룹의 소득 중앙값이 잔류 그룹에 비해 특히 낮게 나타납니다.
            - **인사이트**: 전공 분야보다는 해당 전공자들이 기대하는 소득 수준과 실제 보상 간의 '격차'가 이탈에 영향을 미칠 수 있습니다.
            - **액션 플랜**: 채용 시 기대 연봉 파악 및 투명한 소통 강화.
            """)


def show_job_career():
    """직무/경력 분석 페이지"""
    st.title("직무 및 경력 경로 분석")

    tab1, tab2, tab3 = st.tabs([
        "직무 레벨별 월 소득",
        "연령 및 총 경력",
        "승진 경험과 직무 레벨"
    ])

    with tab1:
        st.subheader("직무 레벨별 월 소득과 이탈 현황")
        st.image(os.path.join(IMG_DIR, "2_jobrole_income_attrition.png"), caption="직무 레벨별 월 소득과 이탈 현황")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **인사이트**: 'Sales Representative' 직급의 낮은 보상 수준이 저연차 직원의 핵심 이탈 드라이버입니다.
            - **액션 플랜**: 'Sales Representative' 연봉 테이블 재조정 및 'Rep -> Exec' 성장 프로그램 강화.
            """)
    with tab2:
        st.subheader("연령 및 총 경력과 이탈의 관계")
        st.image(os.path.join(IMG_DIR, "3_age_workyears_attrition.png"), caption="연령 및 총 경력과 이탈의 관계")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **인사이트**: 사회초년생 딱지를 떼고 본격적으로 커리어를 쌓아가는 시기(20대 후반 ~ 30대 초반)에 이탈이 가장 활발합니다.
            - **액션 플랜**: 2-3년차 직원 대상 경력 개발 면담 정례화 및 사내 직무 이동 기회 확대.
            """)
    with tab3:
        st.subheader("승진 경험과 직무 레벨에 따른 이탈 분석")
        st.image(os.path.join(IMG_DIR, "4_promotion_joblevel_attrition.png"), caption="승진 경험과 직무 레벨에 따른 이탈 분석")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **인사이트**: 입사 후 3년 내에 승진 경험이 없는 것은 매우 강력한 이탈 신호입니다.
            - **액션 플랜**: 입사 2년차 대상 역량 평가 및 승진 검토, 명확한 승진 기준 공표.
            """)
    

def show_performance_evaluation():
    """성과/평가 분석 페이지"""
    st.title("성과 및 만족도 평가 분석")

    tab1, tab2, tab3, tab4 = st.tabs([
        "성과 등급과 이탈률",
        "만족도 조합",
        "주요 이탈 요인",
        "주요 변수 상관관계"
    ])
    
    with tab1:
        st.subheader("성과 등급과 이탈률의 관계")
        st.image(os.path.join(IMG_DIR, "11_performance_rating_attrition.png"), caption="성과 등급과 이탈률의 관계")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **인사이트**: 성과 평가가 인재 유지(Retention) 기능에 실패하고 있습니다. '우수' 인재마저 이탈하고 있습니다.
            - **액션 플랜**: 성과 평가 시스템 전면 재검토 및 상위 등급자에 대한 차별화된 보상/인정 강화.
            """)
    with tab2:
        st.subheader("만족도 조합에 따른 이탈률 변화")
        st.image(os.path.join(IMG_DIR, "5_satisfaction_scores.png"), caption="만족도 조합에 따른 이탈률 변화")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **인사이트**: 전반적인 경험의 질이 이탈 결정에 더 큰 영향을 미칩니다.
            - **액션 플랜**: 직원 경험(Employee Experience) 전담 조직/담당자 지정, 웰니스 프로그램 도입.
            """)
    with tab3:
        st.subheader("주요 요인에 따른 이탈 과정 (Waterfall Chart)")
        st.image(os.path.join(IMG_DIR, "9_waterfall_chart.png"), caption="주요 요인에 따른 이탈 과정 (Waterfall Chart)")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **인사이트**: '경제적 보상'이 가장 우선적인 해결 과제임을 명확히 보여줍니다.
            - **액션 플랜**: 이탈 방지 예산 배정 시, 보상 관련 항목에 최우선 순위를 부여합니다.
            """)
    with tab4:
        st.subheader("주요 수치 변수와 이탈 간의 상관관계")
        st.image(os.path.join(IMG_DIR, "7_correlation_heatmap.png"), caption="주요 수치 변수와 이탈 간의 상관관계")
        with st.expander("분석 내용 보기"):
            st.markdown("""
            - **인사이트**: 저연차, 저직급, 저임금 직원이 이탈의 핵심 '위험군'임을 명확히 보여줍니다.
            - **액션 플랜**: 핵심 인재 관리 정책 재정의.
            """)

def show_data_explorer():
    """데이터 탐색 페이지"""
    st.title("데이터 탐색 및 검색")
    st.write("아래 필터를 사용하여 원본 데이터를 탐색할 수 있습니다.")

    # 필터링 UI
    st.sidebar.header("데이터 필터")
    
    # 직무 선택
    selected_job_roles = st.sidebar.multiselect(
        '직무 (JobRole)',
        options=df['JobRole'].unique(),
        default=df['JobRole'].unique()
    )

    # 이탈 여부 선택
    selected_attrition = st.sidebar.multiselect(
        '이탈 여부 (Attrition)',
        options=df['Attrition_Kor'].unique(),
        default=df['Attrition_Kor'].unique()
    )

    # 월 소득 범위 선택
    min_income, max_income = int(df['MonthlyIncome'].min()), int(df['MonthlyIncome'].max())
    selected_income = st.sidebar.slider(
        '월 소득 (MonthlyIncome)',
        min_value=min_income,
        max_value=max_income,
        value=(min_income, max_income)
    )

    # 승진 경험 선택
    selected_promotion = st.sidebar.multiselect(
        '승진 경험',
        options=df['Promotion_Status'].unique(),
        default=df['Promotion_Status'].unique()
    )

    # 필터링 로직
    filtered_df = df[
        df['JobRole'].isin(selected_job_roles) &
        df['Attrition_Kor'].isin(selected_attrition) &
        (df['MonthlyIncome'] >= selected_income[0]) &
        (df['MonthlyIncome'] <= selected_income[1]) &
        df['Promotion_Status'].isin(selected_promotion)
    ]

    st.write(f"**총 {len(filtered_df)}개의 데이터가 조회되었습니다.**")
    st.dataframe(filtered_df)


def show_recommendations():
    """종합 제언 페이지"""
    st.title("종합 제언 및 액션 플랜")
    
    st.markdown("""
    분석 결과를 바탕으로, 저연차 Sales 직원의 성공적인 조직 안착과 장기 근속을 유도하기 위한 종합적인 액션 플랜을 다음과 같이 제안합니다.
    """)

    tab1, tab2, tab3 = st.tabs(["보상 및 인정", "성장 및 경력", "업무 환경 및 문화"])

    with tab1:
        st.subheader("보상 및 인정")
        st.markdown("""
        | 핵심 문제 | 우선순위 | 제안 액션 | 기대 효과 |
        |:---:|:---:|:---|:---|
        | `Sales Rep` 낮은 급여 | **상** | - 초임 연봉 테이블 현실화<br>- 성과 기반 인센티브 강화 | 단기 이탈률 감소 |
        """)
    with tab2:
        st.subheader("성장 및 경력")
        st.markdown("""
        | 핵심 문제 | 우선순위 | 제안 액션 | 기대 효과 |
        |:---:|:---:|:---|:---|
        | 불투명한 커리어 패스 | **상** | - 성장 경로 명확화<br>- 조기 승진 제도 도입 | 동기 부여, 성장 기대감 |
        """)
    with tab3:
        st.subheader("업무 환경 및 문화")
        st.markdown("""
        | 핵심 문제 | 우선순위 | 제안 액션 | 기대 효과 |
        |:---:|:---:|:---|:---|
        | 낮은 만족도, 잦은 출장 | **중** | - 1:1 멘토링 의무화<br>- 출장 규정 재검토 | 조직 적응 지원, 워라밸 개선 |
        """)
    
    st.success("위 제안들의 성공적인 실행을 통해 이탈률을 **향후 1년 내 15%p 이상 감소**시킬 수 있을 것으로 기대됩니다.")


# --- 5. 페이지 라우팅 ---
if page == "요약":
    show_summary()
elif page == "소득과 만족도":
    show_income_satisfaction()
elif page == "직무와 경력":
    show_job_career()
elif page == "성과와 평가":
    show_performance_evaluation()
elif page == "데이터 탐색":
    show_data_explorer()
elif page == "종합 제언":
    show_recommendations()