import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 디렉토리 설정
output_dir = 'P2'
images_dir = os.path.join(output_dir, 'images')
os.makedirs(images_dir, exist_ok=True)

# 한글 폰트 설정
# 시스템에 나눔고딕이 설치되어 있다면 사용하고, 없다면 다른 폰트를 시도
try:
    fm.FontProperties(fname='/usr/share/fonts/truetype/nanum/NanumGothic.ttf')
    plt.rcParams['font.family'] = 'NanumGothic'
except:
    try:
        fm.FontProperties(fname='C:/Windows/Fonts/malgunbd.ttf')
        plt.rcParams['font.family'] = 'Malgun Gothic'
    except:
        print("나눔고딕 또는 맑은고딕 폰트를 찾을 수 없습니다. 기본 폰트로 대체합니다.")
        pass

plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지

# 데이터 로드
file_path = os.path.join(output_dir, 'data', 'price112.csv')
df = pd.read_csv(file_path)

# 데이터 전처리
# 컬럼명 변경 (불필요한 컬럼 제거 및 월별 데이터 컬럼 추출)
df = df.iloc[:, 1:] # '통계표' 컬럼 제거
df.columns = ['Item', 'Unit', 'Weight', 'Transform'] + pd.to_datetime(df.columns[4:], format='%b-%y').strftime('%Y-%m').tolist()

# 월별 데이터 컬럼 추출
month_cols = df.columns[4:]

# 물가 지수 데이터를 숫자로 변환 (coerce를 사용하여 오류가 있는 값은 NaN으로 처리)
for col in month_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# '총지수' 데이터 추출 (전체 소비자물가지수)
total_cpi = df[df['Item'] == '총지수'].copy()
total_cpi_melted = total_cpi.melt(id_vars=['Item', 'Unit', 'Weight', 'Transform'],
                                   var_name='날짜', value_name='CPI')
total_cpi_melted['날짜'] = pd.to_datetime(total_cpi_melted['날짜'])


# '식료품 및 비주류음료' 카테고리 데이터 추출
food_beverage_cpi = df[df['Item'] == '식료품 및 비주류음료'].copy()
food_beverage_cpi_melted = food_beverage_cpi.melt(id_vars=['Item', 'Unit', 'Weight', 'Transform'],
                                                  var_name='날짜', value_name='CPI')
food_beverage_cpi_melted['날짜'] = pd.to_datetime(food_beverage_cpi_melted['날짜'])


# 가설 검증을 위한 세부 품목 추출 (식료품 및 비주류음료 내에서 가중치가 높은 품목 위주)
# '식료품 및 비주류음료'의 하위 카테고리만 필터링 (총지수, 식료품 및 비주류음료, 식료품, 육류, 어류 및 수산, 우유, 치즈 및 계란, 과일, 채소 및 해조, 과자, 빙과류 및 당류, 기타 식료품, 비주류 음료, 주류 및 담배 등은 제외)
exclude_items = ['총지수', '식료품 및 비주류음료', '식료품', '육류', '어류 및 수산', '우유, 치즈 및 계란',
                 '과자, 빙과류 및 당류', '기타 식료품', '비주류 음료', '주류 및 담배',
                 '의류 및 신발', '주택, 수도, 전기 및 연료', '가정용품 및 가사 서비스', '보건', '교통', '통신',
                 '오락 및 문화', '교육', '음식 및 숙박', '기타 상품 및 서비스', '의류', '신발', '주택임차료',
                 '주거시설 유지·보수', '수도 및 주거관련 서비스', '전기, 가스 및 기타연료', '가구, 가사비품 및 카페트',
                 '가정용 섬유제품', '가정용 기기', '가정용 기구 수리서비스', '주방용품 및 가정용품',
                 '가정·정원용 공구 및 장비', '일상 생활용품 및 가사 서비스', '가구내 고용 및 가사 서비스',
                 '의료용품 및 장비', '외래환자 서비스', '병원 서비스', '운송장비', '개인운송장비 운영',
                 '개인운송장비 소모품 및 유지·수리', '개인운송장비 관련 기타 서비스', '운송 서비스', '우편서비스',
                 '전화 및 팩스장비', '전화 및 팩스 서비스', '음향, 영상, 사진 및 정보처리 장비',
                 '기타 오락 및 문화용 주요 내구재', '기타 오락용품, 조경용품 및 애완동물', '오락 및 문화 서비스',
                 '신문, 서적 및 문방구', '단체여행', '유치원 및 초등교육', '고등교육', '기타교육', '음식 서비스',
                 '숙박 서비스', '미용용품 및 미용 서비스', '개인용 전기용품 및 미용용품', '기타 개인용품',
                 '기타서비스']

# '식료품 및 비주류음료'의 하위 카테고리 중 가중치가 0이 아닌 품목
food_items = df[(df['Weight'] > 0) & (~df['Item'].isin(exclude_items))].copy()

# 시계열 형태로 변환
food_items_melted = food_items.melt(id_vars=['Item', 'Unit', 'Weight', 'Transform'],
                                     var_name='날짜', value_name='CPI')
food_items_melted['날짜'] = pd.to_datetime(food_items_melted['날짜'])


# 월별 CPI 변화율 계산
def calculate_monthly_change(df_melted):
    df_melted = df_melted.sort_values(by=['Item', '날짜'])
    df_melted['MonthlyChange'] = df_melted.groupby('Item')['CPI'].pct_change() * 100
    return df_melted

total_cpi_melted = calculate_monthly_change(total_cpi_melted)
food_beverage_cpi_melted = calculate_monthly_change(food_beverage_cpi_melted)
food_items_melted = calculate_monthly_change(food_items_melted)

print("데이터 전처리 완료.")


# 1. 전체 CPI 추이 및 식료품/비주류 음료 CPI 추이 (Line Chart)
plt.figure(figsize=(15, 7))
plt.plot(total_cpi_melted['날짜'], total_cpi_melted['CPI'], label='총지수 (Total CPI)', marker='o', linestyle='-')
plt.plot(food_beverage_cpi_melted['날짜'], food_beverage_cpi_melted['CPI'], label='식료품 및 비주류음료 (Food & Non-alcoholic Beverages CPI)', marker='x', linestyle='--')
plt.title('전체 소비자물가지수 및 식료품/비주류음료 물가지수 추이')
plt.xlabel('날짜')
plt.ylabel('CPI (2020=100)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '1_total_food_cpi_trend.png'))
plt.close()

print("1. 전체 CPI 및 식료품/비주류음료 CPI 추이 그래프 저장 완료.")

# 2. 주요 식품 품목 CPI 추이 (Line Chart) - 가중치 상위 5개 품목
top_weighted_food_items = food_items.sort_values(by='Weight', ascending=False).head(5)['Item'].tolist()
plt.figure(figsize=(15, 8))
for item in top_weighted_food_items:
    item_data = food_items_melted[food_items_melted['Item'] == item]
    plt.plot(item_data['날짜'], item_data['CPI'], label=item, marker='.', linestyle='-')

plt.title('주요 식품 품목 CPI 추이 (가중치 상위 5개)')
plt.xlabel('날짜')
plt.ylabel('CPI (2020=100)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '2_top5_food_items_cpi_trend.png'))
plt.close()

print("2. 주요 식품 품목 CPI 추이 그래프 저장 완료.")

# 3. 가중치 분포 (Donut Chart) - 전체 카테고리 기준
# '총지수' 제외하고 가중치 기준으로 상위 10개 품목 추출
weighted_items = df[df['Item'] != '총지수'].groupby('Item')['Weight'].first().sort_values(ascending=False)
top_10_weighted = weighted_items.head(10)
other_weight = weighted_items.iloc[10:].sum()
if other_weight > 0:
    top_10_weighted['기타'] = other_weight

plt.figure(figsize=(10, 10))
plt.pie(top_10_weighted, labels=top_10_weighted.index, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3))
plt.title('전체 품목 가중치 분포 (상위 10개 및 기타)')
plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '3_item_weight_donut_chart.png'))
plt.close()

print("3. 가중치 분포 도넛 차트 저장 완료.")

# 4. 월별 CPI 변화율 히스토그램 (Histogram) - 총지수와 식료품/비주류음료
plt.figure(figsize=(15, 7))

plt.subplot(1, 2, 1)
plt.hist(total_cpi_melted['MonthlyChange'].dropna(), bins=10, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('총지수 월별 변화율 분포')
plt.xlabel('월별 변화율 (%)')
plt.ylabel('빈도')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.hist(food_beverage_cpi_melted['MonthlyChange'].dropna(), bins=10, alpha=0.7, color='lightcoral', edgecolor='black')
plt.title('식료품 및 비주류음료 월별 변화율 분포')
plt.xlabel('월별 변화율 (%)')
plt.ylabel('빈도')
plt.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(images_dir, '4_monthly_cpi_change_histogram.png'))
plt.close()

print("4. 월별 CPI 변화율 히스토그램 저장 완료.")

# 5. 가장 높은/낮은 물가 상승률을 보인 품목 (Horizontal Bar Chart)
# 최근 월의 물가 상승률을 기준으로 분석
latest_month = food_items_melted['날짜'].max()
latest_month_changes = food_items_melted[food_items_melted['날짜'] == latest_month].dropna(subset=['MonthlyChange'])

# 상위 10개 상승 품목
top_10_increases = latest_month_changes.sort_values(by='MonthlyChange', ascending=False).head(10)
plt.figure(figsize=(12, 7))
plt.barh(top_10_increases['Item'], top_10_increases['MonthlyChange'], color='salmon')
plt.xlabel('월별 변화율 (%)')
plt.title(f'최근 월({latest_month.strftime("%Y-%m")}) 물가 상승률 상위 10개 품목')
plt.gca().invert_yaxis() # 가장 높은 값부터 표시
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '5_top10_cpi_increases.png'))
plt.close()

print("5. 물가 상승률 상위 10개 품목 바 차트 저장 완료.")

# 6. 가장 높은/낮은 물가 상승률을 보인 품목 (Horizontal Bar Chart)
# 하위 10개 하락 품목 (추가 분석 제안과 일관성을 위해 5번과 분리하여 6번으로 재명명)
top_10_decreases = latest_month_changes.sort_values(by='MonthlyChange', ascending=True).head(10)
plt.figure(figsize=(12, 7))
plt.barh(top_10_decreases['Item'], top_10_decreases['MonthlyChange'], color='lightgreen')
plt.xlabel('월별 변화율 (%)')
plt.title(f'최근 월({latest_month.strftime("%Y-%m")}) 물가 하락률 상위 10개 품목')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '6_top10_cpi_decreases.png'))
plt.close()

print("6. 물가 하락률 상위 10개 품목 바 차트 저장 완료.")

# 7. 월별 품목별 CPI 변화율 Box Plot (특정 기간 동안의 주요 품목)
# '과일'과 '채소 및 해조' 품목군 선택하여 Box Plot 생성
selected_categories = df[df['Item'].isin(['과일', '채소 및 해조'])].copy()
selected_categories_melted = selected_categories.melt(id_vars=['Item', 'Unit', 'Weight', 'Transform'],
                                                      var_name='날짜', value_name='CPI')
selected_categories_melted['날짜'] = pd.to_datetime(selected_categories_melted['날짜'])
selected_categories_melted = calculate_monthly_change(selected_categories_melted)

plt.figure(figsize=(15, 8))
# seaborn은 스타일을 사용하지 않으므로, 직접 boxplot을 그립니다.
data_for_boxplot = [selected_categories_melted[selected_categories_melted['Item'] == '과일']['MonthlyChange'].dropna(),
                    selected_categories_melted[selected_categories_melted['Item'] == '채소 및 해조']['MonthlyChange'].dropna()]
plt.boxplot(data_for_boxplot, labels=['과일', '채소 및 해조'])
plt.title('과일 및 채소/해조 품목군의 월별 CPI 변화율 분포')
plt.xlabel('품목군')
plt.ylabel('월별 변화율 (%)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '7_fruit_vegetable_cpi_boxplot.png'))
plt.close()

print("7. 과일 및 채소/해조 품목군 월별 CPI 변화율 Box Plot 저장 완료.")

# 8. 품목군별 누적 CPI 변화율 (Stacked Area Chart) - 식료품 내 주요 5개 품목
# 가설에 집중하여 '식료품 및 비주류음료' 내의 가중치 상위 5개 품목의 누적 CPI 변화율 시각화
top_5_food_items_for_area = food_items.sort_values(by='Weight', ascending=False).head(5)
top_5_food_items_for_area_melted = top_5_food_items_for_area.melt(id_vars=['Item', 'Unit', 'Weight', 'Transform'],
                                                                    var_name='날짜', value_name='CPI')
top_5_food_items_for_area_melted['날짜'] = pd.to_datetime(top_5_food_items_for_area_melted['날짜'])

# 각 품목의 CPI를 기준 시점(가장 오래된 날짜)으로 정규화하여 누적 변화율 계산
pivot_df = top_5_food_items_for_area_melted.pivot_table(index='날짜', columns='Item', values='CPI')

plt.figure(figsize=(15, 8))
plt.stackplot(pivot_df.index, pivot_df.T, labels=pivot_df.columns, alpha=0.8)
plt.title('식료품 내 주요 5개 품목의 CPI 누적 추이')
plt.xlabel('날짜')
plt.ylabel('CPI (2020=100)')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '8_stacked_area_cpi_top5_food.png'))
plt.close()

print("8. 품목군별 누적 CPI 변화율 (Stacked Area Chart) 저장 완료.")

# 9. 전체 CPI와 주요 품목 CPI 간의 상관관계 (Scatter Plot)
# '총지수'와 '과일', '채소 및 해조'의 CPI를 비교
# 데이터 병합
merged_cpi = total_cpi_melted[['날짜', 'CPI']].rename(columns={'CPI': '총지수 CPI'})
fruit_cpi = selected_categories_melted[selected_categories_melted['Item'] == '과일'][['날짜', 'CPI']].rename(columns={'CPI': '과일 CPI'})
vegetable_cpi = selected_categories_melted[selected_categories_melted['Item'] == '채소 및 해조'][['날짜', 'CPI']].rename(columns={'CPI': '채소 및 해조 CPI'})

comparison_df = merged_cpi.merge(fruit_cpi, on='날짜', how='inner').merge(vegetable_cpi, on='날짜', how='inner')

plt.figure(figsize=(10, 8))
plt.scatter(comparison_df['총지수 CPI'], comparison_df['과일 CPI'], alpha=0.7, label='총지수 vs 과일')
plt.scatter(comparison_df['총지수 CPI'], comparison_df['채소 및 해조 CPI'], alpha=0.7, label='총지수 vs 채소 및 해조', color='orange')
plt.title('총지수 CPI와 과일/채소 CPI 간의 관계')
plt.xlabel('총지수 CPI')
plt.ylabel('품목 CPI')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '9_cpi_correlation_scatter.png'))
plt.close()

print("9. 전체 CPI와 주요 품목 CPI 간의 상관관계 (Scatter Plot) 저장 완료.")

# 10. 월별 품목별 변화율 Heatmap (상위 10개 변화 품목)
# 전체 기간 동안 변화율이 큰 품목들을 대상으로 Heatmap
# 각 품목의 월별변화율의 표준편차를 기준으로 상위 10개 품목 선정
food_items_change_std = food_items_melted.groupby('Item')['MonthlyChange'].std().sort_values(ascending=False).head(10).index.tolist()
heatmap_data = food_items_melted[food_items_melted['Item'].isin(food_items_change_std)].pivot_table(index='Item', columns='날짜', values='MonthlyChange')

plt.figure(figsize=(18, 10))
plt.imshow(heatmap_data, cmap='coolwarm', aspect='auto', interpolation='nearest')
plt.colorbar(label='월별 변화율 (%)')
plt.xticks(np.arange(len(heatmap_data.columns)), [d.strftime('%Y-%m') for d in heatmap_data.columns], rotation=90)
plt.yticks(np.arange(len(heatmap_data.index)), heatmap_data.index)
plt.title('월별 품목별 CPI 변화율 히트맵 (변동성 상위 10개 품목)')
plt.xlabel('날짜')
plt.ylabel('품목')
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '10_item_monthly_cpi_heatmap.png'))
plt.close()

print("10. 월별 품목별 변화율 Heatmap 저장 완료.")


# 11. 과일/채소 품목의 월별 평균 CPI 변화율 (Bar Chart) - 계절성 분석
# '과일'과 '채소 및 해조' 품목의 데이터를 필터링
fruit_vegetable_melted = food_items_melted[food_items_melted['Item'].isin(['과일', '채소 및 해조'])].copy()
fruit_vegetable_melted['Month'] = fruit_vegetable_melted['날짜'].dt.month

# 월별 평균 변화율 계산
monthly_avg_change = fruit_vegetable_melted.groupby(['Item', 'Month'])['MonthlyChange'].mean().unstack()

plt.figure(figsize=(15, 8))
monthly_avg_change.T.plot(kind='bar', figsize=(15, 8))
plt.title('과일 및 채소/해조 품목군의 월별 평균 CPI 변화율 (계절성)')
plt.xlabel('월')
plt.ylabel('평균 월별 변화율 (%)')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.legend(title='품목')
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '11_fruit_vegetable_monthly_avg_change.png'))
plt.close()

print("11. 과일 및 채소/해조 품목군의 월별 평균 CPI 변화율 그래프 저장 완료.")

# 12. 특정 품목(예: 귤, 배추)의 연도별 월별 CPI 변화 추이 (Line Chart) - 계절성 분석
selected_seasonal_items = ['귤', '배추']
seasonal_items_df = food_items_melted[food_items_melted['Item'].isin(selected_seasonal_items)].copy()
seasonal_items_df['Year'] = seasonal_items_df['날짜'].dt.year
seasonal_items_df['Month_Name'] = seasonal_items_df['날짜'].dt.strftime('%b') # 월 이름을 가져오기

plt.figure(figsize=(15, 8))
for item in selected_seasonal_items:
    item_data = seasonal_items_df[seasonal_items_df['Item'] == item]
    for year in item_data['Year'].unique():
        yearly_data = item_data[item_data['Year'] == year].sort_values(by='날짜')
        plt.plot(yearly_data['Month_Name'], yearly_data['CPI'], marker='o', label=f'{item} ({year}년)')

plt.title('주요 계절 품목(귤, 배추)의 연도별 월별 CPI 변화 추이')
plt.xlabel('월')
plt.ylabel('CPI (2020=100)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '12_seasonal_items_yearly_cpi_trend.png'))
plt.close()

print("12. 주요 계절 품목의 연도별 월별 CPI 변화 추이 그래프 저장 완료.")

# 13. 명절이 포함된 월(9월)과 다른 월의 CPI 변화율 비교 (Box Plot) - 이벤트 상관관계 분석
# 여기서는 9월을 추석이 있는 달로 가정 (데이터 기간 2024-12 ~ 2025-12)
# 모든 food_items_melted 데이터를 사용
food_items_melted['Month'] = food_items_melted['날짜'].dt.month
food_items_melted['Is_Chuseok_Month'] = food_items_melted['Month'] == 9 # 9월을 추석 월로 가정

plt.figure(figsize=(10, 7))
# seaborn 스타일을 사용하지 않으므로 직접 plt.boxplot을 사용
data_chuseok = food_items_melted[food_items_melted['Is_Chuseok_Month']]['MonthlyChange'].dropna()
data_other_months = food_items_melted[~food_items_melted['Is_Chuseok_Month']]['MonthlyChange'].dropna()

plt.boxplot([data_other_months, data_chuseok], labels=['기타 월', '9월 (명절 가정)'])
plt.title('식료품 품목의 월별 CPI 변화율 분포 (9월 vs 기타 월)')
plt.xlabel('월 그룹')
plt.ylabel('월별 변화율 (%)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(images_dir, '13_chuseok_month_cpi_boxplot.png'))
plt.close()

print("13. 명절(9월) CPI 변화율 비교 Box Plot 저장 완료.")
