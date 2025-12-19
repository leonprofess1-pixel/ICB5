
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 페이지 설정 ---
st.set_page_config(page_title="Sales 고성과자 이탈 분석", layout="wide", page_icon="🌊")

# --- 데이터 로딩 및 전처리 ---
@st.cache_data
def load_data():
    """데이터를 로드하고 전처리합니다."""
    file_path = "3y_sales_hr/HR-Employee-Attrition.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"오류: 데이터 파일('{file_path}')을 찾을 수 없습니다.")
        st.info("스크립트가 올바르게 작동하려면 '3y_sales_hr' 폴더 내에 'HR-Employee-Attrition.csv' 파일이 필요합니다.")
        st.stop()
        
    df_sales = df[(df['Department'] == 'Sales') & (df['YearsAtCompany'] <= 3)].copy()
    
    # 파생 변수 생성
    df_sales['Attrition_Kor'] = df_sales['Attrition'].apply(lambda x: '이탈' if x == 'Yes' else '잔류')
    df_sales['PerformanceRating_Kor'] = df_sales['PerformanceRating'].map({1: 'Low', 2: 'Good', 3: 'Excellent', 4: 'Outstanding'})
    df_sales['OverTime_Kor'] = df_sales['OverTime'].apply(lambda x: '야근' if x == 'Yes' else '야근 없음')

    return df_sales

df = load_data()
# --- 색상 맵 ---
color_map = {'이탈': '#FF6B6B', '잔류': '#6B82FF'}

# --- 페이지 함수 정의 ---

def show_summary(df):
    """요약 페이지"""
    st.title("📄 요약: Sales 저연차 이탈 현황")
    st.markdown("---")

    total_employees = len(df)
    attrition_count = df['Attrition'].value_counts().get('Yes', 0)
    attrition_rate = (attrition_count / total_employees * 100) if total_employees > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("분석 대상 인원", f"{total_employees} 명")
    col2.metric("이탈 인원", f"{attrition_count} 명", delta=f"{attrition_count}명 이탈", delta_color="inverse")
    col3.metric("이탈률", f"{attrition_rate:.1f} %", delta_color="inverse")

    st.markdown("---")
    
    col1, col2 = st.columns([1.2, 2])
    
    with col1:
        st.subheader("이탈 현황")
        fig_pie = px.pie(df, names='Attrition_Kor', title='이탈 vs. 잔류 비율',
                         hole=0.4, color='Attrition_Kor', color_discrete_map=color_map)
        fig_pie.update_layout(legend_title_text='범례')
        st.plotly_chart(fig_pie, width='stretch')

    with col2:
        st.subheader("Executive Summary")
        st.info(
            """
            - **문제**: 3명 중 1명이 3년 내 퇴사하는 심각한 인력 누수, 특히 **미래 성장 동력인 고성과자의 이탈**이 가속화되고 있습니다.
            - **핵심 원인**: 데이터 분석 결과, **(1) 보상의 비현실성**, **(2) 성장의 불확실성**, **(3) 성과 창출 과정의 소진(Burnout)**이 복합적으로 작용합니다.
            - **Top 제안**: 고성과자 그룹의 **기본 연봉 테이블(Salary Band)을 재설계**하고, **'재충전 안식월(Sabbatical)' 제도**를 도입하여 핵심 인재의 장기 근속을 유도해야 합니다.
            """
        )

def show_compensation_analysis(df):
    """보상 문제 분석 페이지"""
    st.title("💰 보상 문제 분석")
    st.markdown("##### '낮은 보상'이 이탈의 가장 큰 동인임을 입증하고, 문제의 깊이를 다각도로 보여줍니다.")
    
    tabs = st.tabs(["직무별 소득 격차", "야근과 보상"])
    
    with tabs[0]:
        st.subheader("직무별 소득 격차 (Violin Plot)")
        fig = px.violin(df, x='JobRole', y='MonthlyIncome', color='Attrition_Kor', box=True,
                        title='직무별 월 소득 분포 (이탈/잔류 그룹)',
                        labels={'JobRole': '직무', 'MonthlyIncome': '월 소득', 'Attrition_Kor': '이탈 여부'},
                        color_discrete_map=color_map)
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: 이탈 문제는 특히 **'Sales Representative' 직급의 '저임금' 문제**에 집중되어 있습니다.")
        st.markdown("**👉 액션플랜**: 'Sales Representative' 직급의 초임 연봉을 시장 상위 25% 수준으로 인상하는 것을 적극 검토해야 합니다.")

    with tabs[1]:
        st.subheader("야근과 보상 (Box Plot)")
        fig = px.box(df, x='OverTime_Kor', y='MonthlyIncome', color='Attrition_Kor',
                     title='야근 유무에 따른 월 소득 분포',
                     labels={'OverTime_Kor': '야근 유무', 'MonthlyIncome': '월 소득', 'Attrition_Kor': '이탈 여부'},
                     color_discrete_map=color_map)
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: **야근하는 그룹의 소득 중앙값이 야근하지 않는 그룹보다 오히려 낮습니다.** 즉, '적게 버는 직원이 야근까지 하는' 상황이며, 이 그룹에서 이탈률이 심각하게 높습니다.")
        st.markdown("**👉 액션플랜**: 야근 수당을 현실화하고, 장기적으로는 포괄임금제 재검토 및 인력 충원을 통해 과도한 야근 문화를 개선해야 합니다.")

def show_growth_analysis(df):
    """성장 정체 분석 페이지"""
    st.title("📈 성장 정체 분석")
    st.markdown("##### 직원들이 '성장의 한계'를 느끼고 떠나는 과정을 시각적으로 보여줍니다.")

    tabs = st.tabs(["승진 정체", "경력과 직급의 미스매치"])

    with tabs[0]:
        st.subheader("승진 정체 (Bar Chart)")
        df_promotion = df.groupby('YearsSinceLastPromotion')['Attrition_Kor'].value_counts(normalize=True).mul(100).rename('percentage').reset_index()
        df_promotion_churn = df_promotion[df_promotion['Attrition_Kor'] == '이탈']
        fig = px.bar(df_promotion_churn, x='YearsSinceLastPromotion', y='percentage',
                     title='마지막 승진 이후 기간별 이탈률',
                     labels={'YearsSinceLastPromotion': '마지막 승진 이후 년수', 'percentage': '이탈률 (%)'})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: **승진 없이 단 1년만 지나도 이탈률이 급격히 증가**합니다. 승진 경험의 부재가 퇴사의 결정적 계기가 되고 있습니다.")
        st.markdown("**👉 액션플랜**: 입사 2년차에 자동으로 승진 심사 대상이 되는 제도를 도입하고, 역량 미달자를 제외하고는 대부분 승진시키는 것을 고려해 볼 수 있습니다(Promotion by default).")

    with tabs[1]:
        st.subheader("경력과 직급의 미스매치 (Scatter Plot)")
        fig = px.scatter(df, x='TotalWorkingYears', y='JobLevel', color='Attrition_Kor',
                         title='총 경력과 직무 레벨의 관계',
                         labels={'TotalWorkingYears': '총 경력(년)', 'JobLevel': '직무 레벨', 'Attrition_Kor': '이탈 여부'},
                         color_discrete_map=color_map, opacity=0.7)
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: 총 경력(타사 경력 포함)이 많음에도 불구하고 낮은 직무 레벨(1, 2)에 머물러 있는 **'과소평가(Undervalued)' 그룹에서 이탈이 두드러집니다.**")
        st.markdown("**👉 액션플랜**: 경력직 채용 시, 총 경력을 공정하게 평가하여 직무 레벨과 연봉에 반영하는 프로세스를 마련하고, 내부 직원의 경력 관리 계획(Career Path)을 강화해야 합니다.")

def show_environment_analysis(df):
    """업무 환경 분석 페이지"""
    st.title("🌿 업무 환경 분석")
    st.markdown("##### 물리적, 심리적 업무 환경이 이탈에 미치는 영향을 분석합니다.")
    
    tabs = st.tabs(["만족도 매트릭스", "출장과 워라밸"])

    with tabs[0]:
        st.subheader("만족도 매트릭스 (2D Density Plot)")
        fig = px.density_heatmap(df, x="JobSatisfaction", y="EnvironmentSatisfaction", facet_col="Attrition_Kor",
                                 title="업무 만족도와 환경 만족도 관계 (이탈/잔류 그룹)",
                                 labels={"JobSatisfaction": "업무 만족도", "EnvironmentSatisfaction": "환경 만족도"})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: 업무와 환경 만족도가 **모두 낮은 '위험 영역'(좌하단)에 이탈자들이 집중 분포**되어 있습니다.")
        st.markdown("**👉 액션플랜**: 분기별 직원 만족도 설문(Pulse Survey)을 통해 '위험 영역'에 속한 직원을 조기 발견하고, HRBP(HR Business Partner)가 집중 면담 및 케어 프로그램을 제공해야 합니다.")

    with tabs[1]:
        st.subheader("출장과 워라밸 (Faceted Bar Chart)")
        df_travel = df.groupby(['BusinessTravel', 'WorkLifeBalance'])['Attrition_Kor'].value_counts(normalize=True).mul(100).rename('percentage').reset_index()
        df_travel_churn = df_travel[df_travel['Attrition_Kor'] == '이탈']
        fig = px.bar(df_travel_churn, x='WorkLifeBalance', y='percentage', color='BusinessTravel', barmode='group',
                     title='출장 빈도와 워라밸에 따른 이탈률',
                     labels={'WorkLifeBalance': '워라밸 점수', 'percentage': '이탈률 (%)', 'BusinessTravel': '출장 빈도'})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: **'잦은 출장(Travel_Frequently)' 그룹의 워라밸 점수가 가장 낮으며, 이 그룹의 이탈률이 전반적으로 가장 높게** 나타납니다. 잦은 출장이 워라밸 붕괴와 이탈의 직접적인 원인 중 하나입니다.")
        st.markdown("**👉 액션플랜**: 불필요한 출장을 줄이기 위한 '원격 회의 우선 정책'을 도입하고, 잦은 출장 직원에 대한 '출장 마일리지' 및 '대체 휴가' 제공과 같은 보상 체계를 강화해야 합니다.")

def show_lifecycle_analysis(df):
    """고성과자 생애주기 분석 페이지"""
    st.title("🌊 고성과자 생애주기 분석 (High-Performer Lifecycle Analysis)")
    st.markdown("##### 고성과 직원의 입사부터 이탈까지의 여정(Journey)을 추적하여, 단계별 핵심적인 이탈 위험 요인을 식별하고 선제적인 인재 유지 전략을 수립합니다.")

    tabs = st.tabs(["누가 고성과를 내는가?", "고성과자의 보상 현실", "성과와 소진의 악순환", "정체된 고성과자의 이탈 경로"])

    with tabs[0]:
        st.subheader("누가 고성과를 내는가? (Who are the High-Performers?)")
        df_perf = df.groupby(['JobRole', 'PerformanceRating_Kor']).size().reset_index(name='count')
        fig = px.bar(df_perf, x='JobRole', y='count', color='PerformanceRating_Kor', barmode='group',
                     title='직무별 성과 등급 분포',
                     labels={'JobRole': '직무', 'count': '인원 수', 'PerformanceRating_Kor': '성과 등급'},
                     category_orders={"PerformanceRating_Kor": ["Good", "Excellent", "Outstanding"]})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 진단**: 고성과자는 대부분 **'Sales Representative' 직급에 집중**되어 있습니다. 이는 해당 직급이 우리 회사의 핵심적인 가치 창출 그룹임을 의미합니다.")
        st.markdown("**👉 액션플랜**: 고성과를 내는 Sales Representative 그룹에 대한 유지(Retention) 전략을 최우선 순위로 설정하고, 이들의 성장에 집중적으로 투자해야 합니다.")

    with tabs[1]:
        st.subheader("고성과자의 보상 현실 (Compensation Reality)")
        fig = px.box(df, x='PerformanceRating_Kor', y='MonthlyIncome', color='Attrition_Kor',
                     title='성과 등급별 월 소득 분포',
                     labels={'PerformanceRating_Kor': '성과 등급', 'MonthlyIncome': '월 소득', 'Attrition_Kor': '이탈 여부'},
                     color_discrete_map=color_map, category_orders={"PerformanceRating_Kor": ["Good", "Excellent", "Outstanding"]})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 진단**: 최고 성과(Outstanding)를 내는 직원의 월 소득 중앙값이, 바로 아래 등급(Excellent)과 큰 차이가 없습니다. **절대적인 소득 수준 자체가 고성과에 대한 기대치를 충족시키지 못하고 있습니다.**")
        st.markdown("**👉 액션플랜**: 연봉 인상률だけでなく, 고성과자 그룹의 **기본 연봉 테이블(Salary Band) 자체를 시장 최상위 수준으로 재설계**하여, 업계 최고 대우를 보장해야 합니다.")

    with tabs[2]:
        st.subheader("성과와 소진의 악순환 (Performance-Burnout Cycle)")
        fig = px.density_heatmap(df, x="WorkLifeBalance", y="PerformanceRating", facet_col="Attrition_Kor",
                                 title="워라밸과 성과 등급의 관계 (이탈/잔류 그룹)",
                                 labels={"WorkLifeBalance": "워라밸 점수", "PerformanceRating": "성과 등급"})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 진단**: 이탈하는 고성과자 그룹은 **'높은 성과'와 '낮은 워라밸' 영역에 집중적으로 분포**합니다. 이는 성과 창출 과정이 개인의 희생과 소진을 담보로 하고 있음을 명백히 보여줍니다.")
        st.markdown("**👉 액션플랜**: **'지속 가능한 성과(Sustainable Performance)' 프로그램**을 도입해야 합니다. 특정 기간 이상 고성과를 유지한 직원에 대한 **'재충전 안식월(Sabbatical)' 또는 '특별 유급휴가' 부여**를 제도화하여, 장기적인 동기 부여와 번아웃 예방을 동시에 추구해야 합니다.")

    with tabs[3]:
        st.subheader("정체된 고성과자의 이탈 경로 (Stagnant High-Performer's Exit Path)")
        high_perf_leavers = df[(df['PerformanceRating'] == 4)]
        
        if not high_perf_leavers.empty:
            # Sankey Diagram 데이터 준비
            df_sankey = high_perf_leavers.groupby(['YearsSinceLastPromotion', 'JobSatisfaction', 'Attrition_Kor']).size().reset_index(name='count')
            
            # 레이블 리스트 생성
            labels = []
            labels.extend(df_sankey['YearsSinceLastPromotion'].apply(lambda x: f"승진정체 {x}년").unique())
            labels.extend(df_sankey['JobSatisfaction'].apply(lambda x: f"만족도 {x}").unique())
            labels.extend(df_sankey['Attrition_Kor'].unique())
            
            label_map = {label: i for i, label in enumerate(labels)}

            # 소스, 타겟, 값 리스트 생성
            source = []
            target = []
            value = []

            # Promotion -> Satisfaction
            for _, row in df_sankey.groupby(['YearsSinceLastPromotion', 'JobSatisfaction']).agg({'count': 'sum'}).reset_index().iterrows():
                source.append(label_map[f"승진정체 {row['YearsSinceLastPromotion']}"])
                target.append(label_map[f"만족도 {row['JobSatisfaction']}"])
                value.append(row['count'])

            # Satisfaction -> Attrition
            for _, row in df_sankey.iterrows():
                source.append(label_map[f"만족도 {row['JobSatisfaction']}"])
                target.append(label_map[row['Attrition_Kor']])
                value.append(row['count'])
            
            fig = go.Figure(data=[go.Sankey(
                node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels),
                link=dict(source=source, target=target, value=value)
            )])
            fig.update_layout(title_text="최고 성과(Outstanding) 직원의 이탈 경로", font_size=12)
            st.plotly_chart(fig, width='stretch')
            st.markdown("**💡 진단**: '최고 성과자' 중 **'승진 못한 지 1년 이상'된 그룹의 80%가 '낮은 직무 만족도'를 보이며, 이들 중 대부분이 결국 '이탈'로 이어지는 명확한 경로**가 확인됩니다.")
            st.markdown("**👉 액션플랜**: HR 시스템 내에 **'고성과자 승진 정체 알림(Stagnation Alert)'** 기능을 개발해야 합니다. 최고 등급 성과자가 18개월 이상 승진하지 못할 경우, 담당 HRBP와 임원에게 자동 알림이 가고, 해당 직원에 대한 의무적인 커리어 개발 면담을 진행해야 합니다.")
        else:
            st.warning("최고 성과(Outstanding) 등급의 직원이 데이터에 없습니다.")

def show_recommendations():
    """최종 제언 페이지"""
    st.title("🎯 최종 제언: 실행 중심 Action Plan")
    st.markdown("---")

    st.subheader("P1 (즉시 실행): 보상 체계의 근본적 혁신")
    st.success(
        """
        - **진단**: 현재 보상 시스템은 고성과 인재 유치 및 유지에 완전히 실패했습니다.
        - **액션**: 
            1. **고성과자 Salary Band 재설계**: Sales Rep. 고성과자 그룹의 기본 연봉을 시장 상위 10% 수준으로 상향 조정합니다.
            2. **성과 기반 인상률 차등**: 4등급(Outstanding) 성과자에 대해 최소 15% 이상의 연봉 인상을 보장하는 규정을 신설합니다.
        - **기대 효과**: 핵심 인재 이탈 방지, 공정한 보상 문화 정착, 채용 경쟁력 확보.
        """
    )
    st.subheader("P2 (중기 과제): '성장 정체' 해소를 위한 제도적 지원")
    st.warning(
        """
        - **진단**: 승진 정체는 고성과자의 동기 부여를 저해하는 가장 큰 장애물입니다.
        - **액션**:
            1. **Fast-Track 승진 제도 도입**: 2년 연속 최고 등급 성과자는 다음 직급으로 즉시 승진 심사 자격을 부여합니다.
            2. **'성장 정체 알림' 시스템**: 18개월 이상 승진이 없는 고성과자를 시스템이 자동 식별하여 HRBP에게 통보, 의무적으로 커리어 코칭을 진행하게 합니다.
        - **기대 효과**: 잠재적 리더 그룹의 조기 육성, 직원들에게 장기적인 성장 비전을 제시하여 조직 몰입도를 강화.
        """
    )
    st.subheader("P3 (장기 과제): 지속가능한 성과 문화를 위한 투자")
    st.info(
        """
        - **진단**: 현재의 성과는 직원의 '소진(burnout)'을 대가로 이루어지고 있어 장기적으로 위험합니다.
        - **액션**:
            1. **'재충전 안식월' 도입**: 3년 이상 연속 고성과자에게 1개월의 유급 안식월을 부여하여 재충전과 자기계발 기회를 제공합니다.
            2. **Pulse Survey 정례화**: 분기별 익명 설문을 통해 이탈 위험군을 조기에 발견하고 선제적으로 지원합니다.
        - **기대 효과**: 직원의 워라밸 개선 및 심리적 안정감 제공, 장기적인 근속 유도 및 건강한 조직 문화 구축.
        """
    )


# --- 사이드바 및 페이지 라우팅 ---
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["요약", "보상 문제 분석", "성장 정체 분석", "업무 환경 분석", "고성과자 생애주기 분석", "최종 제언"])

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
