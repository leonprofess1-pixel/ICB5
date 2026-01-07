import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# 1. 한글 폰트 및 설정
font_path = r'C:\Windows\Fonts\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
sns.reset_orig()

# 2. 데이터 로드 및 심층 전처리
file_path = r'P2\data\youtube_recom.csv'
df = pd.read_csv(file_path)

# 날짜/시간 처리
df['published_at'] = pd.to_datetime(df['published_at'])
df['hour'] = df['published_at'].dt.hour
df['day_name'] = df['published_at'].dt.day_name()
df['is_weekend'] = df['published_at'].dt.dayofweek >= 5

# 파생 변수 생성: Velocity (일평균 조회수 - 폭발력 측정 지표)
# 0일차인 경우 1일로 보정하여 무한대 방지
df['video_age_days'] = df['video_age_days'].clip(lower=1)
df['views_per_day'] = df['view_count'] / df['video_age_days']

# 파생 변수 생성: Title Length
df['title_length'] = df['Title'].str.len()

# 파생 변수 생성: Duration Category (영상 길이 구간화)
# 0~60s: Shorts, 60~300s: Short, 300~900s: Mid, 900s+: Long
bins = [0, 60, 300, 900, float('inf')]
labels = ['Shorts (<1m)', 'Short (1-5m)', 'Mid (5-15m)', 'Long (>15m)']
df['duration_cat'] = pd.cut(df['duration_seconds'], bins=bins, labels=labels)

# 카테고리 매핑
category_map = {
    1: 'Film & Animation', 2: 'Autos & Vehicles', 10: 'Music',
    15: 'Pets & Animals', 17: 'Sports', 19: 'Travel & Events',
    20: 'Gaming', 22: 'People & Blogs', 23: 'Comedy',
    24: 'Entertainment', 25: 'News & Politics', 26: 'Howto & Style',
    27: 'Education', 28: 'Science & Technology', 29: 'Nonprofits & Activism'
}
df['category_name'] = df['category_id'].map(category_map).fillna('Other')

# 저장 경로
save_dir = r'P2\images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

print("4차 진단 분석 시작...")

# --- 1. 바이럴의 근거: Views per Day (Velocity) 분포 ---
# 상위 1%와 나머지 그룹 비교
top_threshold = df['view_count'].quantile(0.99)
df['performance_tier'] = np.where(df['view_count'] >= top_threshold, 'Top 1% (Viral)', 'Others')

plt.figure(figsize=(10, 6))
# 로그 스케일 적용하여 분포 비교
sns.histplot(data=df, x='views_per_day', hue='performance_tier', element="step", stat="density", common_norm=False, log_scale=True, palette='Set1')
plt.title('바이럴의 근거: 일평균 조회수(Velocity) 분포 비교', fontproperties=font_prop, fontsize=15)
plt.xlabel('일평균 조회수 (Log Scale)', fontproperties=font_prop)
plt.ylabel('밀도 (Density)', fontproperties=font_prop)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v4_1_velocity_distribution.png'))
plt.close()
print("1. Velocity Distribution 완료")

# --- 2. 제목 길이의 심리학: KDE Plot (Top vs Bottom) ---
# 상위 10% vs 하위 50% 비교
high_tier = df[df['view_count'] >= df['view_count'].quantile(0.90)]
low_tier = df[df['view_count'] <= df['view_count'].quantile(0.50)]

plt.figure(figsize=(10, 6))
sns.kdeplot(data=high_tier, x='title_length', fill=True, label='Top 10% (High Views)', color='red', alpha=0.3)
sns.kdeplot(data=low_tier, x='title_length', fill=True, label='Bottom 50% (Low Views)', color='gray', alpha=0.3)
plt.title('제목 길이의 최적점: 인지 부하와 클릭률의 관계', fontproperties=font_prop, fontsize=15)
plt.xlabel('제목 글자 수', fontproperties=font_prop)
plt.ylabel('분포 밀도', fontproperties=font_prop)
plt.legend(prop=font_prop)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v4_2_title_length_kde.png'))
plt.close()
print("2. Title Length KDE 완료")

# --- 3. 포맷별 알고리즘 기대치: Duration Binning Analysis ---
# 길이 구간별 평균 참여율과 평균 조회수 비교
format_stats = df.groupby('duration_cat', observed=False)[['engagement_rate', 'view_count']].mean().reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))

# 막대: 평균 조회수
color = 'tab:blue'
ax1.set_xlabel('영상 길이 구간 (Format)', fontproperties=font_prop)
ax1.set_ylabel('평균 조회수', color=color, fontproperties=font_prop)
ax1.bar(format_stats['duration_cat'], format_stats['view_count'], color=color, alpha=0.6, label='Avg Views')
ax1.tick_params(axis='y', labelcolor=color)

# 선: 평균 참여율
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('평균 참여율 (Engagement Rate)', color=color, fontproperties=font_prop)
ax2.plot(format_stats['duration_cat'], format_stats['engagement_rate'], color=color, marker='o', linewidth=3, label='Engagement Rate')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('포맷별 성과 분석: Shorts의 고참여 vs Long의 충성도', fontproperties=font_prop, fontsize=15)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v4_3_format_performance.png'))
plt.close()
print("3. Format Performance 완료")

# --- 4. 주말 효과 해부: 24h Time Series Comparison ---
# 평일과 주말의 시간대별 평균 조회수 분리
weekday_hourly = df[~df['is_weekend']].groupby('hour')['view_count'].mean()
weekend_hourly = df[df['is_weekend']].groupby('hour')['view_count'].mean()

plt.figure(figsize=(12, 6))
plt.plot(weekday_hourly.index, weekday_hourly.values, label='평일 (Weekday)', color='gray', linestyle='--')
plt.plot(weekend_hourly.index, weekend_hourly.values, label='주말 (Weekend)', color='orange', linewidth=2.5)

# 차이 채우기 (Gap 강조)
plt.fill_between(weekday_hourly.index, weekday_hourly.values, weekend_hourly.values, 
                 where=(weekend_hourly.values > weekday_hourly.values),
                 interpolate=True, color='orange', alpha=0.2, label='Weekend Advantage')

plt.title('주말 효과의 해부: 24시간 트래픽 패턴 비교', fontproperties=font_prop, fontsize=15)
plt.xlabel('시간 (0~23시)', fontproperties=font_prop)
plt.ylabel('평균 조회수', fontproperties=font_prop)
plt.xticks(range(0, 24))
plt.legend(prop=font_prop)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v4_4_weekend_gap_analysis.png'))
plt.close()
print("4. Weekend Gap Analysis 완료")

# --- 5. 소셜 증명 메커니즘: Likes to Comments Regression ---
# 좋아요가 댓글을 얼마나 설명하는가?
plt.figure(figsize=(10, 6))
# 데이터 샘플링 및 로그 변환
sample_df = df.sample(n=min(1000, len(df)), random_state=42).copy()
sample_df['log_likes'] = np.log1p(sample_df['like_count'])
sample_df['log_comments'] = np.log1p(sample_df['comment_count'])

sns.regplot(data=sample_df, x='log_likes', y='log_comments', 
            scatter_kws={'alpha':0.3, 'color':'purple'}, line_kws={'color':'gold'})
plt.title('소셜 증명(Social Proof): 좋아요와 댓글의 인과성', fontproperties=font_prop, fontsize=15)
plt.xlabel('좋아요 수 (Log Scale)', fontproperties=font_prop)
plt.ylabel('댓글 수 (Log Scale)', fontproperties=font_prop)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v4_5_social_proof_reg.png'))
plt.close()
print("5. Social Proof Regression 완료")

# --- 6. 성공 공식의 다양성: Parallel Coordinates Plot ---
# 주요 3개 카테고리의 지표 패턴 비교 (정규화 필수)
target_cats = ['Music', 'Gaming', 'News & Politics']
df_target = df[df['category_name'].isin(target_cats)].copy()

# 지표 정규화 (MinMax)
cols_to_plot = ['view_count', 'like_count', 'comment_count', 'duration_seconds']
scaler = MinMaxScaler()
df_target[cols_to_plot] = scaler.fit_transform(df_target[cols_to_plot])

# 카테고리별 평균 계산
parallel_data = df_target.groupby('category_name')[cols_to_plot].mean().reset_index()

plt.figure(figsize=(12, 6))
pd.plotting.parallel_coordinates(parallel_data, 'category_name', color=['#FF5733', '#33FF57', '#3357FF'], linewidth=4)
plt.title('카테고리별 성공 지표의 구조적 차이 (Parallel Coordinates)', fontproperties=font_prop, fontsize=15)
plt.ylabel('정규화된 지표 값 (0~1)', fontproperties=font_prop)
plt.legend(prop=font_prop)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v4_6_success_formula_parallel.png'))
plt.close()
print("6. Parallel Coordinates 완료")

print("4차 진단 분석 시각화 완료.")
