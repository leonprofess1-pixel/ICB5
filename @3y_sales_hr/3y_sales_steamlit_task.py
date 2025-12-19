
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 페이지 설정 ---
st.set_page_config(page_title="Sales 저연차 이탈 분석", layout="wide", page_icon="📊")

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

    # 1. 핵심 지표
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
        # 3. 이탈 현황 (Pie Chart)
        st.subheader("이탈 현황")
        fig_pie = px.pie(df, names='Attrition_Kor', title='이탈 vs. 잔류 비율',
                         hole=0.4, color='Attrition_Kor', color_discrete_map=color_map)
        fig_pie.update_layout(legend_title_text='범례')
        st.plotly_chart(fig_pie, width='stretch')

    with col2:
        # 2. Executive Summary
        st.subheader("Executive Summary")
        st.info(
            """
            - **문제**: Sales 부서의 3년차 이하 직원 3명 중 1명(이탈률 34.1%)이 퇴사하여 심각한 인력 누수가 발생하고 있습니다. 특히, **성과가 우수한 핵심인재의 이탈**이 두드러져 장기적인 경쟁력 약화가 우려됩니다.
            - **핵심 원인**: 데이터 분석 결과, **(1) 성과에 대한 불합리한 보상**, **(2) 성장 기대감 부재**, **(3) 고성과자의 번아웃**이 이탈의 주요 원인으로 복합적으로 작용하고 있습니다.
            - **Top 제안**:
                1. 성과 등급과 연동된 **차등 연봉 인상률 테이블**을 즉시 도입하여 '공정한 보상'에 대한 신뢰를 회복해야 합니다.
                2. 우수 인재의 성장 비전을 제시하기 위한 **고성과자 Fast-Track 승진 경로**를 신설해야 합니다.
            """
        )

def show_compensation_analysis(df):
    """보상 문제 분석 페이지"""
    st.title("💰 보상 문제 분석")
    st.markdown("##### '낮은 보상'이 이탈의 가장 큰 동인임을 입증하고, 문제의 깊이를 다각도로 보여줍니다.")
    
    tabs = st.tabs(["직무별 소득 격차", "소득 대비 만족도", "야근과 보상"])
    
    with tabs[0]:
        st.subheader("직무별 소득 격차 (Violin Plot)")
        fig = px.violin(df, x='JobRole', y='MonthlyIncome', color='Attrition_Kor', box=True,
                        title='직무별 월 소득 분포 (이탈/잔류 그룹)',
                        labels={'JobRole': '직무', 'MonthlyIncome': '월 소득', 'Attrition_Kor': '이탈 여부'},
                        color_discrete_map=color_map)
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: 이탈 문제는 특히 **'Sales Representative' 직급의 '저임금' 문제**에 집중되어 있습니다. 해당 직급의 이탈자 그룹은 월 소득 중앙값이 매우 낮게 형성되어 있습니다.")
        st.markdown("**👉 액션플랜**: 'Sales Representative' 직급의 초임 연봉을 시장 상위 25% 수준으로 인상하는 것을 적극 검토해야 합니다.")

    with tabs[1]:
        st.subheader("소득 대비 만족도 (Scatter Plot)")
        fig = px.scatter(df, x='MonthlyIncome', y='JobSatisfaction', color='Attrition_Kor',
                         title='월 소득과 직무 만족도의 관계',
                         labels={'MonthlyIncome': '월 소득', 'JobSatisfaction': '직무 만족도', 'Attrition_Kor': '이탈 여부'},
                         color_discrete_map=color_map, opacity=0.7)
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: 소득이 낮으면서 직무 만족도까지 낮은 **'저소득-저만족' 그룹에서 이탈이 집중**되는 경향이 뚜렷합니다.")
        st.markdown("**👉 액션플랜**: 저연차 직원들의 만족도에 영향을 미치는 비금전적 요인(업무 자율성, 인정 및 피드백 문화, 성장 기회)을 함께 개선하여 보상 불만을 완화해야 합니다.")

    with tabs[2]:
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

    tabs = st.tabs(["승진 정체", "경력과 직급의 미스매치", "교육 기회 불균형"])

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

    with tabs[2]:
        st.subheader("교육 기회 불균형 (Histogram)")
        fig = px.histogram(df, x='TrainingTimesLastYear', color='Attrition_Kor', barmode='overlay',
                           title='지난 1년간 교육 횟수 분포',
                           labels={'TrainingTimesLastYear': '지난 1년간 교육 횟수', 'Attrition_Kor': '이탈 여부'},
                           color_discrete_map=color_map)
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: **이탈자 그룹이 잔류자 그룹에 비해 작년 교육 횟수가 현저히 적습니다.** '회사로부터 투자받지 못한다'는 인식이 이탈을 촉진할 수 있습니다.")
        st.markdown("**👉 액션플랜**: 모든 직원을 대상으로 연간 최소 교육 시간(예: 20시간)을 보장하고, 교육 이수 현황을 성과 평가 및 승진 심사와 연계하는 방안을 검토해야 합니다.")

def show_environment_analysis(df):
    """업무 환경 분석 페이지"""
    st.title("🌿 업무 환경 분석")
    st.markdown("##### 물리적, 심리적 업무 환경이 이탈에 미치는 영향을 분석합니다.")
    
    tabs = st.tabs(["만족도 매트릭스", "출장과 워라밸", "동료 관계와 이탈"])

    with tabs[0]:
        st.subheader("만족도 매트릭스 (2D Density Plot)")
        fig = px.density_heatmap(df, x="JobSatisfaction", y="EnvironmentSatisfaction", facet_col="Attrition_Kor",
                                 title="업무 만족도와 환경 만족도 관계 (이탈/잔류 그룹)",
                                 labels={"JobSatisfaction": "업무 만족도", "EnvironmentSatisfaction": "환경 만족도"})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: 업무 만족도와 환경 만족도가 **모두 낮은 '위험 영역'(좌하단)에 이탈자들이 집중 분포**되어 있습니다.")
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

    with tabs[2]:
        st.subheader("동료 관계와 이탈 (Histogram)")
        fig = px.histogram(df, x='RelationshipSatisfaction', color='Attrition_Kor', barmode='overlay',
                           title='동료 관계 만족도 분포',
                           labels={'RelationshipSatisfaction': '동료 관계 만족도', 'Attrition_Kor': '이탈 여부'},
                           color_discrete_map=color_map)
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 인사이트**: 동료 관계 만족도는 이탈에 결정적인 영향을 주지 않는 것으로 보입니다. 이탈자와 잔류자 그룹 간의 분포 차이가 미미합니다. 직원들은 **'사람' 문제보다는 '보상'과 '성장' 문제 때문에 회사를 떠나고 있습니다.**")
        st.markdown("**👉 액션플랜**: 조직 활성화(Team Building) 예산의 일부를 줄여, 그 예산을 직접적인 보상(연봉 인상, 성과급)이나 성장 지원 프로그램(교육, 자격증 취득 지원)으로 전환하는 것을 고려해 볼 수 있습니다.")

def show_performance_analysis(df):
    """성과 관리 심층 분석 페이지"""
    st.title("💎 성과 관리 심층 분석")
    st.markdown("##### 현재의 성과 평가 및 보상 시스템이 **핵심 인재를 유지**하고 동기를 부여하는 데 효과적인지 진단합니다.")

    tabs = st.tabs(["성과 등급별 이탈 현황", "성과와 보상의 실패", "고성과는 번아웃의 다른 이름인가?", "고성과 이탈자 프로파일"])

    with tabs[0]:
        st.subheader("성과 등급별 이탈 현황 (Bar Chart)")
        df_perf = df.groupby('PerformanceRating_Kor')['Attrition_Kor'].value_counts().rename('count').reset_index()
        fig = px.bar(df_perf, x='PerformanceRating_Kor', y='count', color='Attrition_Kor', barmode='group',
                     title='성과 등급별 이탈/잔류 인원',
                     labels={'PerformanceRating_Kor': '성과 등급', 'count': '인원 수', 'Attrition_Kor': '이탈 여부'},
                     color_discrete_map=color_map, category_orders={"PerformanceRating_Kor": ["Good", "Excellent", "Outstanding"]})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 진단**: 놀랍게도 **최고 성과 그룹('Outstanding')에서 상당수의 이탈이 발생**하고 있습니다. 이는 성과가 좋은 직원이 회사에 만족하고 남아있다는 가정이 틀렸음을 보여주는 심각한 신호입니다.")
        st.markdown("**👉 액션플랜**: 고성과자 그룹의 이탈 원인을 다른 각도에서 심층적으로 분석하여, 이들의 숨겨진 불만 요소를 찾아내야 합니다.")

    with tabs[1]:
        st.subheader("성과와 보상의 실패 (Violin Plot)")
        fig = px.violin(df, x='PerformanceRating_Kor', y='PercentSalaryHike', color='Attrition_Kor', box=True,
                        title='성과 등급별 연봉 인상률 분포',
                        labels={'PerformanceRating_Kor': '성과 등급', 'PercentSalaryHike': '연봉 인상률 (%)', 'Attrition_Kor': '이탈 여부'},
                        color_discrete_map=color_map, category_orders={"PerformanceRating_Kor": ["Good", "Excellent", "Outstanding"]})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 진단**: **성과 관리의 핵심 실패 지점입니다.** 최고 성과('Outstanding')를 받은 직원의 연봉 인상률 분포가 바로 아래 등급('Excellent')과 큰 차이가 없습니다. '열심히 일할수록 손해'라는 인식이 팽배할 수밖에 없는 구조입니다.")
        st.markdown("**👉 액션플랜**: 성과 등급과 연봉 인상률을 명확하고 예측 가능하게 연동해야 합니다. **'Outstanding 등급: 최소 15% 이상', 'Excellent 등급: 8~14%'** 와 같이 차등 보상안을 즉시 마련하고 투명하게 공개해야 합니다.")

    with tabs[2]:
        st.subheader("고성과는 번아웃의 다른 이름인가? (Sunburst Chart)")
        high_performers = df[df['PerformanceRating'] >= 3]
        fig = px.sunburst(high_performers, path=['PerformanceRating_Kor', 'OverTime_Kor', 'Attrition_Kor'],
                          title='고성과 그룹(Excellent, Outstanding)의 이탈 경로',
                          color='Attrition_Kor', color_discrete_map={'이탈': '#FF6B6B', '잔류': '#6B82FF', '(?)':'lightgray'})
        st.plotly_chart(fig, width='stretch')
        st.markdown("**💡 진단**: 성과가 좋은 직원일수록 야근('OverTime') 비율이 높으며, **'고성과 + 야근' 그룹에서 이탈이 집중**되는 것을 볼 수 있습니다. 회사는 이들의 추가 근무를 성과 창출의 당연한 요소로 여기고, 합당한 보상이나 인정에는 실패하고 있습니다.")
        st.markdown("**👉 액션플랜**: 고성과 그룹의 야근 현황을 HR 차원에서 면밀히 모니터링하고, 야근 시간에 비례하는 **추가 보상(특별 인센티브, 유급 휴가)을 제도화**하여 번아웃을 방지하고 로열티를 높여야 합니다.")

    with tabs[3]:
        st.subheader("고성과 이탈자 프로파일 (Parallel Categories Plot)")
        high_perf_leavers = df[(df['PerformanceRating'] == 4) & (df['Attrition'] == 'Yes')]
        if not high_perf_leavers.empty:
            fig = go.Figure(go.Parcats(
                dimensions=[
                    {'label': '직무', 'values': high_perf_leavers['JobRole']},
                    {'label': '승진까지 남은 기간', 'values': high_perf_leavers['YearsSinceLastPromotion']},
                    {'label': '직무 만족도', 'values': high_perf_leavers['JobSatisfaction']},
                    {'label': '야근 여부', 'values': high_perf_leavers['OverTime_Kor']}
                ],
                line={'color': high_perf_leavers['JobSatisfaction'], 'colorscale': 'viridis'},
                hoverinfo='count+probability'
            ))
            fig.update_layout(title="최고 성과(Outstanding) 이탈자들의 공통 특성")
            st.plotly_chart(fig, width='stretch')
            st.markdown("**💡 진단**: 우리가 놓치고 있는 핵심 인재는 주로 **'승진이 정체된(0~1년차) Sales Representative'** 이며, 이들은 **'성과는 최고지만, 직무 만족도는 낮은'** 상태로 회사를 떠나고 있습니다.")
            st.markdown("**👉 액션플랜**: 'Sales Representative' 직급의 고성과자에 대한 **Fast-Track 승진 제도** 도입을 검토하고, 분기별 1:1 면담을 통해 직무 만족도 저하 요인을 선제적으로 파악하고 해결해야 합니다.")
        else:
            st.warning("최고 성과(Outstanding) 이탈자 데이터가 없습니다.")

def show_recommendations():
    """최종 제언 페이지"""
    st.title("🎯 최종 제언: 실행 중심 Action Plan")
    st.markdown("---")

    st.subheader("P1 (상): 성과/보상 체계 즉시 개편")
    st.success(
        """
        - **핵심 문제**: 현재의 보상 시스템은 고성과자에게 동기를 부여하지 못하고, 오히려 이들의 이탈을 가속화하는 '역 인센티브' 구조입니다.
        - **제안 액션**:
            1. **성과연동 연봉인상률 차등 적용**: 성과 등급(Performance Rating)과 연봉 인상률을 명확히 연동하는 새로운 테이블을 즉시 설계하고, 전사 공지해야 합니다. (예: 4등급: 15% 이상, 3등급: 8~14%, 2등급 이하: 5% 미만)
            2. **초임 연봉 경쟁력 확보**: Sales Representative 직무의 초임 연봉을 업계 상위 25% 수준으로 인상하여, 신규 인재 유치 경쟁에서 우위를 점해야 합니다.
        - **기대 효과**: 핵심 인재의 이탈을 방지하고, '성과를 내면 공정하게 보상받는다'는 신뢰 문화를 정착시켜 조직 전반의 생산성을 높일 수 있습니다.
        """
    )

    st.subheader("P2 (중): 고성과자 성장 경로(Career Path) 재설계")
    st.warning(
        """
        - **핵심 문제**: 뛰어난 성과를 내고 있음에도 불구하고, 승진이 정체되거나 명확한 성장 비전을 제시받지 못해 회사를 떠나는 '경력 개발형 이탈'이 다수 발생하고 있습니다.
        - **제안 액션**:
            1. **고성과자 Fast-Track 승진 제도 도입**: 'Outstanding' 등급을 2회 연속 달성한 Sales Representative를 대상으로, Senior 직급으로 조기 승진할 수 있는 경로를 신설합니다.
            2. **경력직 직급/연봉 재산정**: 외부 경력을 충분히 인정하지 않는 현재의 관행을 깨고, 총 경력을 고려한 직급과 연봉을 재산정하는 유연한 채용 프로세스를 도입합니다.
        - **기대 효과**: 잠재적 리더 그룹을 조기에 육성하고, 직원들에게 장기적인 성장 비전을 제시하여 조직 몰입도를 강화할 수 있습니다.
        """
    )
    
    st.subheader("P3 (하): 고성과자 번아웃 방지 및 조직 환경 개선")
    st.info(
        """
        - **핵심 문제**: 높은 성과를 내는 직원일수록 과도한 야근과 출장에 내몰리고 있으며, 이에 대한 합당한 인정이나 보상이 부족하여 번아웃과 심리적 소진을 겪고 있습니다.
        - **제안 액션**:
            1. **추가 업무에 대한 보상 의무화**: 규정 이상의 야근 및 잦은 출장에 대해서는 '대체 휴가' 또는 '특별 인센티브'를 지급하는 것을 의무화합니다.
            2. **이탈 위험군 조기 경보 및 케어**: 분기별 Pulse Survey와 1:1 면담을 정례화하여, 만족도가 낮은 '이탈 위험군'을 선제적으로 파악하고 HR 차원의 맞춤형 케어 프로그램을 제공합니다.
        - **기대 효과**: 직원의 워라밸을 개선하고 심리적 안정감을 제공함으로써, 장기적인 근속을 유도하고 건강한 조직 문화를 구축할 수 있습니다.
        """
    )


# --- 사이드바 및 페이지 라우팅 ---
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["요약", "보상 문제 분석", "성장 정체 분석", "업무 환경 분석", "성과 관리 심층 분석", "최종 제언"])

page_map = {
    "요약": show_summary,
    "보상 문제 분석": show_compensation_analysis,
    "성장 정체 분석": show_growth_analysis,
    "업무 환경 분석": show_environment_analysis,
    "성과 관리 심층 분석": show_performance_analysis,
    "최종 제언": show_recommendations
}

# 함수 호출
selected_function = page_map[page]
if page == "최종 제언":
    selected_function()
else:
    selected_function(df)
