import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 한글 폰트 설정
# Windows
plt.rc('font', family='Malgun Gothic')

st.set_page_config(layout="wide")

st.title('HR 직원 이탈 분석 대시보드')

import os

# 데이터 로드
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '..', 'HR-Employee-Attrition.csv')
    data = pd.read_csv(file_path)
    return data

data = load_data()

st.header('데이터 개요')
st.dataframe(data.head())

st.write(f"데이터 크기: {data.shape[0]}행, {data.shape[1]}열")

st.sidebar.header('분석 메뉴')
menu = st.sidebar.selectbox('보고 싶은 분석을 선택하세요.',
                            ['이탈률 분석', '특성별 분석', '상관관계 분석'])

if menu == '이탈률 분석':
    st.header('전체 이탈률 분석')

    attrition_counts = data['Attrition'].value_counts()
    attrition_rate = (attrition_counts['Yes'] / (attrition_counts['Yes'] + attrition_counts['No'])) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("전체 직원 수", data.shape[0])
        st.metric("이탈 직원 수", attrition_counts['Yes'])
        st.metric("이탈률", f"{attrition_rate:.2f}%")

    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(attrition_counts, labels=['잔류', '이탈'], autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff9999'])
        ax.axis('equal')
        st.pyplot(fig)

elif menu == '특성별 분석':
    st.header('주요 특성별 이탈률 분석')
    
    # 분석할 컬럼 선택
    feature = st.selectbox('분석할 특성을 선택하세요.', 
                               ['Department', 'JobRole', 'Gender', 'EducationField', 'JobLevel', 'OverTime'])

    # 특성별 이탈률 계산 및 시각화
    attrition_by_feature = data.groupby(feature)['Attrition'].value_counts(normalize=True).unstack()
    attrition_by_feature = attrition_by_feature.rename(columns={'Yes': '이탈률', 'No': '잔류율'})
    
    if '이탈률' not in attrition_by_feature.columns:
        attrition_by_feature['이탈률'] = 0

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write(f"### {feature}별 이탈률")
        st.dataframe(attrition_by_feature[['이탈률']].style.format("{:.2%}"))

    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        attrition_by_feature['이탈률'].sort_values(ascending=True).plot(kind='barh', ax=ax, color='skyblue')
        ax.set_title(f'{feature}별 이탈률')
        ax.set_xlabel('이탈률')
        st.pyplot(fig)
        
    if feature == 'JobRole':
        st.subheader("직무별 월 수입 분포")
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.boxplot(x='JobRole', y='MonthlyIncome', data=data, ax=ax, palette='Set3')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)


elif menu == '상관관계 분석':
    st.header('숫자형 특성 간 상관관계 분석')

    # 숫자형 데이터만 선택
    numeric_data = data.select_dtypes(include=np.number)
    
    # 상관관계 행렬 계산
    corr_matrix = numeric_data.corr()

    fig, ax = plt.subplots(figsize=(18, 15))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax, annot_kws={"size": 8})
    ax.set_title('상관관계 히트맵')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    st.pyplot(fig)

    st.write("#### 상관관계가 높은 상위 10개 쌍")
    # 상관관계 행렬에서 중복을 제외하고 절대값 기준으로 정렬
    corr_unstacked = corr_matrix.unstack()
    sorted_corr = corr_unstacked.sort_values(kind="quicksort", ascending=False)
    # 자기 자신과의 상관관계(1)는 제외
    top_corr = sorted_corr[sorted_corr != 1].drop_duplicates().head(10)
    st.dataframe(top_corr.to_frame(name='상관계수'))


st.sidebar.info("""
**사용 안내:**
- 사이드바 메뉴를 통해 원하는 분석을 선택하세요.
- '특성별 분석'에서는 드롭다운 메뉴로 다양한 특성을 탐색할 수 있습니다.
""")

st.sidebar.warning("""
**참고:**
이 대시보드는 `HR-Employee-Attrition.csv` 데이터를 기반으로 생성되었습니다.
데이터의 출처 및 세부 정보는 별도로 확인해야 합니다.
""")

st.info("대시보드 로딩 완료. 좌측 사이드바에서 메뉴를 선택하여 분석을 시작하세요.")
