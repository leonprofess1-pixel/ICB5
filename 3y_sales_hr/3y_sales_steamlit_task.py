import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 페이지 설정 및 데이터 로딩 ---
st.set_page_config(
    page_title="Sales 직원 이탈 현황 대시보드",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    """CSV 파일을 로드하고 초기 필터링을 수행하는 함수"""
    try:
        df_raw = pd.read_csv("3y_sales_hr/HR-Employee-Attrition.csv")
    except FileNotFoundError:
        st.error("Error: '3y_sales_hr/HR-Employee-Attrition.csv' 파일을 찾을 수 없습니다.")
        st.stop()
    
    # 핵심 필터링: Department='Sales' & YearsAtCompany<=3
    df_filtered = df_raw[(df_raw['Department'] == 'Sales') & (df_raw['YearsAtCompany'] <= 3)].copy()
    df_filtered['Attrition_Kor'] = df_filtered['Attrition'].apply(lambda x: '이탈' if x == 'Yes' else '잔류')
    return df_filtered

df_base = load_data()

# --- 2. 사이드바 필터 ---
st.sidebar.title("필터")

# 직무 필터
job_roles = df_base['JobRole'].unique()
selected_job_roles = st.sidebar.multiselect(
    '직무 (JobRole)',
    options=job_roles,
    default=job_roles
)

# 성별 필터
genders = df_base['Gender'].unique()
selected_genders = st.sidebar.multiselect(
    '성별 (Gender)',
    options=genders,
    default=genders
)

# 나이 필터
min_age, max_age = int(df_base['Age'].min()), int(df_base['Age'].max())
age_range = st.sidebar.slider(
    '나이 (Age)',
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# 필터링된 데이터프레임 생성
df_filtered = df_base[
    df_base['JobRole'].isin(selected_job_roles) &
    df_base['Gender'].isin(selected_genders) &
    (df_base['Age'] >= age_range[0]) &
    (df_base['Age'] <= age_range[1])
]

# --- 3. 메인 화면 구성 ---
st.title("근속 3년 이하 Sales 직원 이탈 현황 대시보드")

# 1행: 핵심 지표 (KPIs)
total_employees = len(df_filtered)
attrition_count = len(df_filtered[df_filtered['Attrition'] == 'Yes'])
attrition_rate = (attrition_count / total_employees) * 100 if total_employees > 0 else 0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("전체 직원 수", f"{total_employees} 명")
kpi2.metric("이탈 직원 수", f"{attrition_count} 명")
kpi3.metric("이탈률", f"{attrition_rate:.1f} %")

st.markdown("---")

# 2행: 이탈 현황 개요
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("이탈률 분포")
    if not df_filtered.empty:
        fig_pie = px.pie(
            df_filtered,
            names='Attrition_Kor',
            title='이탈 vs. 잔류 비율',
            hole=0.3,
            color_discrete_map={'이탈': 'salmon', '잔류': 'skyblue'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("선택된 필터에 해당하는 데이터가 없습니다.")

with col2:
    st.subheader("이탈 사유별 인원 (샘플)")
    df_attrition_yes = df_filtered[df_filtered['Attrition'] == 'Yes']
    st.dataframe(df_attrition_yes[[
        'JobRole', 'MonthlyIncome', 'JobSatisfaction', 'WorkLifeBalance', 'YearsSinceLastPromotion'
    ]].head())

st.markdown("---")

# 3행: 변수별 심층 분석 (탭)
st.subheader("변수별 심층 분석")
tab1, tab2, tab3 = st.tabs(["인구통계학적 분석", "직무 관련 분석", "만족도 분석"])

with tab1:
    st.markdown("#### 인구통계학적 분석")
    if not df_filtered.empty:
        # 성별에 따른 이탈률
        fig_gender = px.bar(
            df_filtered.groupby(['Gender', 'Attrition_Kor']).size().reset_index(name='count'),
            x='Gender', y='count', color='Attrition_Kor', barmode='group',
            title='성별에 따른 이탈 현황', labels={'Gender': '성별', 'count': '인원 수', 'Attrition_Kor': '이탈 여부'}
        )
        st.plotly_chart(fig_gender, use_container_width=True)

        # 연령대별 이탈 현황
        fig_age = px.histogram(
            df_filtered, x='Age', color='Attrition_Kor', marginal='box',
            title='연령대별 이탈 현황', labels={'Age': '나이'}, barmode='overlay'
        )
        st.plotly_chart(fig_age, use_container_width=True)

        # 학력 수준별 이탈률
        education_attrition = df_filtered.groupby('EducationField')['Attrition_Kor'].value_counts(normalize=True).mul(100).rename('percentage').reset_index()
        fig_edu = px.bar(
            education_attrition[education_attrition['Attrition_Kor'] == '이탈'],
            x='EducationField', y='percentage', title='학력 분야별 이탈률',
            labels={'EducationField': '학력 분야', 'percentage': '이탈률 (%)'}
        )
        st.plotly_chart(fig_edu, use_container_width=True)
    else:
        st.warning("데이터 없음")

with tab2:
    st.markdown("#### 직무 관련 분석")
    if not df_filtered.empty:
        # 직무별 이탈 현황
        fig_jobrole = px.bar(
            df_filtered.groupby(['JobRole', 'Attrition_Kor']).size().reset_index(name='count'),
            x='JobRole', y='count', color='Attrition_Kor', title='직무별 이탈 현황',
            labels={'JobRole': '직무', 'count': '인원 수', 'Attrition_Kor': '이탈 여부'}
        )
        st.plotly_chart(fig_jobrole, use_container_width=True)

        # 월급과 이탈 여부
        fig_income = px.box(
            df_filtered, x='Attrition_Kor', y='MonthlyIncome', color='Attrition_Kor',
            title='이탈 그룹과 잔류 그룹의 월급 분포',
            labels={'Attrition_Kor': '이탈 여부', 'MonthlyIncome': '월 소득'}
        )
        st.plotly_chart(fig_income, use_container_width=True)

        # 총 경력과 이탈 여부
        fig_workyears = px.violin(
            df_filtered, x='Attrition_Kor', y='TotalWorkingYears', color='Attrition_Kor', box=True,
            title='이탈 그룹과 잔류 그룹의 총 경력 분포',
            labels={'Attrition_Kor': '이탈 여부', 'TotalWorkingYears': '총 경력(년)'}
        )
        st.plotly_chart(fig_workyears, use_container_width=True)

        # 출장 빈도와 이탈률
        fig_travel = px.sunburst(
            df_filtered, path=['BusinessTravel', 'Attrition_Kor'],
            title='출장 빈도와 이탈 여부 관계',
            color_discrete_map={'(?)':'lightgray', '이탈':'salmon', '잔류':'skyblue'}
        )
        st.plotly_chart(fig_travel, use_container_width=True)
    else:
        st.warning("데이터 없음")

with tab3:
    st.markdown("#### 만족도 분석")
    if not df_filtered.empty:
        # 만족도별 이탈률
        satisfaction_cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction']
        df_satisfaction = df_filtered.melt(
            id_vars=['Attrition_Kor'], 
            value_vars=satisfaction_cols,
            var_name='SatisfactionType',
            value_name='Score'
        )
        df_sat_rate = df_satisfaction.groupby(['SatisfactionType', 'Score', 'Attrition_Kor']).size().reset_index(name='count')
        
        fig_satis = px.bar(
            df_sat_rate, x='Score', y='count', color='Attrition_Kor',
            facet_col='SatisfactionType', barmode='group',
            labels={'Score': '만족도 점수', 'count': '인원 수', 'Attrition_Kor': '이탈 여부'},
            title='항목별 만족도와 이탈 현황'
        )
        st.plotly_chart(fig_satis, use_container_width=True)

        # 월급과 업무 만족도 관계
        fig_scatter = px.scatter(
            df_filtered, x='MonthlyIncome', y='JobSatisfaction', color='Attrition_Kor',
            title='월급과 업무 만족도의 관계',
            labels={'MonthlyIncome': '월 소득', 'JobSatisfaction': '업무 만족도', 'Attrition_Kor': '이탈 여부'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("데이터 없음")
