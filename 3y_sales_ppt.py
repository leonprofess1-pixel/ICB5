import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 스타일
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Retention Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS (다크 모드 스타일링 및 폰트 조정)
st.markdown("""
<style>
    .main {
        background-color: #0f172a; /* Slate 900 */
        color: #e2e8f0; /* Slate 200 */
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    h1, h2, h3 {
        color: white !important;
    }
    .metric-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #334155;
        text-align: center;
    }
    .highlight {
        color: #60a5fa; /* Blue 400 */
        font-weight: bold;
    }
    .danger {
        color: #f87171; /* Red 400 */
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 세션 상태 관리 (슬라이드 네비게이션)
# -----------------------------------------------------------------------------
if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

SLIDE_COUNT = 6

def next_slide():
    if st.session_state.slide_index < SLIDE_COUNT - 1:
        st.session_state.slide_index += 1

def prev_slide():
    if st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1

# -----------------------------------------------------------------------------
# 3. 데이터 및 차트 생성 함수
# -----------------------------------------------------------------------------

def plot_survival_analysis():
    # 데이터: 근속 기간별 이탈률
    data = pd.DataFrame({
        'Tenure': ['3M', '6M', '9M', '1Y', '1.5Y', '2Y', '3Y'],
        'Rate': [12, 28, 15, 10, 18, 8, 5],
        'Type': ['Normal', 'Critical', 'Normal', 'Normal', 'Warning', 'Normal', 'Normal']
    })
    
    colors = {'Normal': '#3b82f6', 'Critical': '#ef4444', 'Warning': '#f97316'}
    
    fig = go.Figure(data=[go.Bar(
        x=data['Tenure'],
        y=data['Rate'],
        marker_color=[colors[t] for t in data['Type']],
        text=data['Rate'].apply(lambda x: f"{x}%"),
        textposition='auto',
    )])
    
    # 어노테이션 추가
    fig.add_annotation(x='6M', y=28, text="🚩 Death Valley", showarrow=True, arrowhead=1, yshift=10)
    fig.add_annotation(x='1.5Y', y=18, text="⚠️ Promotion Gap", showarrow=True, arrowhead=1, yshift=10)

    fig.update_layout(
        title="근속 기간별 이탈 생존 분석 (Survival Analysis)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="이탈률 (%)",
        xaxis_title="근속 기간"
    )
    return fig

def plot_heatmap():
    # 데이터: 성과 등급(Y) vs 근속 기간(X) 이탈률
    z_data = [
        [5, 10, 15, 20, 10],   # S
        [10, 20, 30, 40, 25],  # A
        [20, 30, 40, 30, 20],  # B
        [40, 60, 50, 20, 15],  # C
        [80, 90, 70, 40, 30]   # D
    ]
    x_labels = ['1-3개월', '4-6개월', '7-12개월', '13-24개월', '25-36개월']
    y_labels = ['S등급', 'A등급', 'B등급', 'C등급', 'D등급']

    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x_labels,
        y=y_labels,
        colorscale='RdYlGn_r', # 빨강(위험) -> 초록(안전) 역순
        texttemplate="%{z}%",
        textfont={"size": 12}
    ))
    
    fig.update_layout(
        title="성과 등급별/기간별 이탈 위험 히트맵",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def plot_bubble_chart():
    # 데이터: 성과(X) vs 보상만족도(Y)
    df = pd.DataFrame([
        {'Performance': 90, 'Satisfaction': 80, 'Tenure': 30, 'Status': 'Stay', 'Label': 'Core Talent'},
        {'Performance': 85, 'Satisfaction': 30, 'Tenure': 20, 'Status': 'Leave', 'Label': 'Risk Zone'},
        {'Performance': 40, 'Satisfaction': 40, 'Tenure': 10, 'Status': 'Leave', 'Label': 'Low Perf'},
        {'Performance': 60, 'Satisfaction': 70, 'Tenure': 25, 'Status': 'Stay', 'Label': 'Mid Perf'},
        {'Performance': 95, 'Satisfaction': 20, 'Tenure': 15, 'Status': 'Leave', 'Label': 'Burnout'},
        {'Performance': 50, 'Satisfaction': 50, 'Tenure': 28, 'Status': 'Stay', 'Label': 'Average'},
        {'Performance': 30, 'Satisfaction': 80, 'Tenure': 5, 'Status': 'Stay', 'Label': 'Overpaid'},
    ])

    fig = px.scatter(
        df, x="Performance", y="Satisfaction",
        size="Tenure", color="Status",
        color_discrete_map={'Stay': '#3b82f6', 'Leave': '#ef4444'},
        hover_name="Label",
        size_max=60,
        text="Label"
    )
    
    fig.update_traces(textposition='top center')
    fig.update_layout(
        title="성과 대비 인센티브 만족도 분포",
        xaxis_title="성과 점수 (Performance)",
        yaxis_title="보상 만족도 (Satisfaction)",
        xaxis=dict(range=[0, 110]),
        yaxis=dict(range=[0, 110]),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    
    # 사분면 가이드라인
    fig.add_hline(y=50, line_dash="dash", line_color="gray")
    fig.add_vline(x=50, line_dash="dash", line_color="gray")
    
    return fig

def plot_radar_chart():
    categories = ['목표 달성력', '활동량(Call)', '관리자 코칭', '동료 관계', '직무 적합성']
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[85, 80, 75, 85, 70],
        theta=categories,
        fill='toself',
        name='재직자 평균',
        line_color='#3b82f6'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[90, 95, 40, 60, 50],
        theta=categories,
        fill='toself',
        name='이탈자 평균',
        line_color='#ef4444'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="역량 및 환경 만족도 비교 (Radar Chart)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    return fig

# -----------------------------------------------------------------------------
# 4. 슬라이드 렌더링 함수
# -----------------------------------------------------------------------------

def render_slide_1():
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>Sales 부서 저년차 직원<br>이탈 요인 심층 분석</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #94a3b8;'>성과(Performance) 데이터를 중심으로 한<br>3년 이하 근속자 Retention 전략</h3>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #64748b;'>CONFIDENTIAL | HR ANALYTICS TEAM</p>", unsafe_allow_html=True)

def render_slide_2():
    st.header("1. 분석 배경 및 가설")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🚨 Problem Definition")
        st.markdown("""
        ### 최근 1년간 이탈률 급증
        * Sales 부서 3년차 이하 직원 이탈률: **28%**
        * 전사 평균(12%) 대비 **2배 이상** 상회
        """)
    
    with col2:
        st.success("🎯 Research Hypothesis")
        st.markdown("""
        ### 가설 설정
        "저년차 직원의 이탈은 단순 부적응이 아닌, **성과 압박과 보상 시스템의 괴리**에서 오는 구조적 문제일 것이다."
        """)
        
    st.markdown("### 🔍 Focus Areas")
    c1, c2, c3 = st.columns(3)
    c1.metric("Focus 1", "Onboarding 성과", "0-6개월")
    c2.metric("Focus 2", "Incentive 달성", "Threshold")
    c3.metric("Focus 3", "경쟁 강도", "Burnout")

def render_slide_3():
    st.header("2. 이탈 현황 오버뷰 (Overview)")
    st.markdown("---")
    
    # KPI Row
    col1, col2, col3 = st.columns(3)
    col1.metric("3년 이하 총 이탈률", "28.4%", "+4.2%p")
    col2.metric("평균 이탈 시점", "8.5개월", "Onboarding 직후")
    col3.metric("이탈자 평균 성과율", "92%", "고성과자 이탈 심각")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart Row
    st.plotly_chart(plot_survival_analysis(), use_container_width=True)
    st.info("💡 Insight: 입사 6개월 차(Death Valley)와 1.5년 차(Promotion Gap)에 이탈이 집중됨.")

def render_slide_4():
    st.header("3. 심층 분석: 성과와 보상의 괴리")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_heatmap(), use_container_width=True)
        st.error("Key Insight: 입사 4~6개월 차 D등급뿐만 아니라, **A등급(고성과자)의 1년 전후 이탈**도 매우 높음.")
        
    with col2:
        st.plotly_chart(plot_bubble_chart(), use_container_width=True)
        st.warning("Key Insight: **High Performance / Low Satisfaction** 군집이 이탈 위험이 가장 높음 (보상 캡 문제).")

def render_slide_5():
    st.header("4. 심층 분석: 페르소나 및 역량 비교")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.plotly_chart(plot_radar_chart(), use_container_width=True)
        st.markdown("**분석결과:** 이탈자는 개인 실적은 좋으나 **'관리자 코칭'**과 **'동료 관계'** 점수가 현저히 낮음.")
        
    with col2:
        st.markdown("### 🔍 주요 이탈 페르소나")
        
        with st.expander("🔥 The Lone Wolf (고독한 늑대형)", expanded=True):
            st.markdown("""
            * **특징:** 입사 1년차, 개인 실적 Top 10%.
            * **원인:** 팀 미팅 참여 저조, 매니저 면담 부족.
            * **불만:** "내가 번 만큼 못 가져간다" (보상 구조 불만).
            """)
            
        with st.expander("💧 The Early Burnout (조기 소진형)", expanded=True):
            st.markdown("""
            * **특징:** 입사 6개월차, 초반 활동량 과다.
            * **원인:** 첫 Deal Closing 지연으로 인한 동기 상실.
            * **불만:** 멘탈 케어 및 가이드 부재.
            """)

def render_slide_6():
    st.header("5. 종합 결론 및 해결 방안 (Action Plan)")
    st.markdown("---")
    
    st.markdown("### 📌 종합 진단")
    st.markdown("Sales 저년차 이탈의 핵심은 **'성과-보상의 Time Lag'**와 **'고립된 성장 환경'**입니다.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### 💰 Fast-Track Incentive")
        st.success("""
        **Spot Bonus 도입**
        신규 입사자 첫 6개월간
        인센티브 월 단위 지급으로
        즉각적 보상 제공
        """)
        
    with c2:
        st.markdown("#### 🤝 Sales Enablement")
        st.info("""
        **코칭 의무화**
        팀장 평가에 Retention 반영
        신규 입사자 전담 멘토링
        (Buddy Program) 강화
        """)
        
    with c3:
        st.markdown("#### 🚨 Early Warning System")
        st.warning("""
        **데이터 기반 관리**
        3개월 연속 활동/실적 불균형자
        자동 식별 및 면담 진행
        """)

# -----------------------------------------------------------------------------
# 5. 메인 앱 실행 로직
# -----------------------------------------------------------------------------

# 슬라이드 맵핑
slides = {
    0: render_slide_1,
    1: render_slide_2,
    2: render_slide_3,
    3: render_slide_4,
    4: render_slide_5,
    5: render_slide_6
}

# 현재 슬라이드 렌더링
slides[st.session_state.slide_index]()

# 하단 네비게이션 바
st.markdown("---")
col_prev, col_pg, col_next = st.columns([1, 10, 1])

with col_prev:
    if st.button("◀ Prev"):
        prev_slide()
        st.rerun()

with col_pg:
    st.progress((st.session_state.slide_index + 1) / SLIDE_COUNT)
    st.markdown(f"<div style='text-align: center'>Slide {st.session_state.slide_index + 1} / {SLIDE_COUNT}</div>", unsafe_allow_html=True)

with col_next:
    if st.button("Next ▶"):
        next_slide()
        st.rerun()
