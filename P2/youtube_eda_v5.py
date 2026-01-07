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

# 2. 데이터 로드
file_path = r'P2\data\youtube_recom.csv'
df = pd.read_csv(file_path)

# 3. 전처리
df['published_at'] = pd.to_datetime(df['published_at'])
df['hour'] = df['published_at'].dt.hour
df['day_name'] = df['published_at'].dt.day_name()
df['title_length'] = df['Title'].str.len()
df['video_age_days'] = df['video_age_days'].clip(lower=1)
df['views_per_day'] = df['view_count'] / df['video_age_days']

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

print("5차 심층 분석 (Deep Dive) 시작...")

# --- 1. 채널 불평등: Lorenz Curve (Pareto Principle) ---
# 채널별 총 조회수 집계 및 정렬
channel_stats = df.groupby('channel_title')['view_count'].sum().sort_values()
lorenz = channel_stats.cumsum() / channel_stats.sum()
lorenz = np.insert(lorenz.values, 0, 0) # 0에서 시작

plt.figure(figsize=(8, 8))
plt.plot(np.linspace(0, 1, len(lorenz)), lorenz, drawstyle='steps-post', color='crimson', linewidth=2)
plt.plot([0, 1], [0, 1], color='gray', linestyle='--', label='Perfect Equality')
plt.title('채널 불평등 분석: 로렌츠 곡선 (Lorenz Curve)', fontproperties=font_prop, fontsize=15)
plt.xlabel('하위 채널 비율 (Cumulative % of Channels)', fontproperties=font_prop)
plt.ylabel('조회수 점유율 (Cumulative % of Views)', fontproperties=font_prop)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v5_1_lorenz_curve.png'))
plt.close()
print("1. Lorenz Curve 완료")

# --- 2. 기술적 스펙의 영향: Definition & Caption ---
# 해상도(definition)와 자막(caption) 유무에 따른 조회수 분포 (Log Scale Boxplot)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.boxplot(data=df, x='definition', y='view_count', hue='definition', ax=axes[0], palette='Set2', legend=False)
axes[0].set_yscale('log')
axes[0].set_title('해상도(Definition)에 따른 조회수 차이', fontproperties=font_prop)

sns.boxplot(data=df, x='caption', y='view_count', hue='caption', ax=axes[1], palette='Set3', legend=False)
axes[1].set_yscale('log')
axes[1].set_title('자막(Caption) 유무에 따른 조회수 차이', fontproperties=font_prop)

plt.suptitle('기술적 요소(Tech Specs)가 성과에 미치는 영향', fontproperties=font_prop, fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v5_2_definition_caption_impact.png'))
plt.close()
print("2. Tech Specs Impact 완료")

# --- 3. 제목 길이의 역설: 조회수 vs 참여율 Trade-off ---
# 제목 길이를 구간화하여 조회수와 참여율의 관계 비교
df['title_len_bin'] = pd.cut(df['title_length'], bins=range(0, 110, 10))
title_stats = df.groupby('title_len_bin', observed=False)[['view_count', 'engagement_rate']].mean().reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))

# 조회수 (Bar)
color1 = 'tab:blue'
ax1.set_xlabel('제목 길이 구간 (글자 수)', fontproperties=font_prop)
ax1.set_ylabel('평균 조회수 (Views)', color=color1, fontproperties=font_prop)
ax1.bar(title_stats['title_len_bin'].astype(str), title_stats['view_count'], color=color1, alpha=0.6, label='Views')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.tick_params(axis='x', rotation=45)

# 참여율 (Line)
ax2 = ax1.twinx()
color2 = 'tab:green'
ax2.set_ylabel('평균 참여율 (Engagement Rate)', color=color2, fontproperties=font_prop)
ax2.plot(title_stats['title_len_bin'].astype(str), title_stats['engagement_rate'], color=color2, marker='s', linewidth=2, label='Engagement')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('제목 길이의 역설: 클릭(Views) vs 만족(Engagement)', fontproperties=font_prop, fontsize=15)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v5_3_title_engagement_tradeoff.png'))
plt.close()
print("3. Title Trade-off 완료")

# --- 4. 골든 타임 히트맵: Category vs Upload Hour ---
# 카테고리별 업로드 시간대 히트맵 (값: 정규화된 평균 조회수)
pivot_table = df.pivot_table(index='category_name', columns='hour', values='view_count', aggfunc='mean').fillna(0)
# 행(카테고리)별로 MinMax Scaling하여 시간대 패턴 강조
pivot_norm = pivot_table.div(pivot_table.max(axis=1), axis=0)

plt.figure(figsize=(14, 10))
sns.heatmap(pivot_norm, cmap='YlOrRd', annot=False, fmt=".1f", linewidths=.5)
plt.title('카테고리별 업로드 골든 타임 (Normalized Views)', fontproperties=font_prop, fontsize=15)
plt.xlabel('업로드 시간 (Hour)', fontproperties=font_prop)
plt.ylabel('카테고리', fontproperties=font_prop)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v5_4_upload_heatmap.png'))
plt.close()
print("4. Upload Heatmap 완료")

# --- 5. 속도와 품질의 상관관계: Velocity vs Quality ---
# Velocity(초기 속도)가 빠를수록 품질(좋아요 비율)이 떨어지는가? (Clickbait 검증)
# 극단값 제거 후 시각화
filtered_df = df[(df['views_per_day'] > 0) & (df['likes_to_views_ratio'] > 0)]
sample_df = filtered_df.sample(n=min(2000, len(filtered_df)), random_state=42)
sample_df = sample_df[sample_df['views_per_day'] < sample_df['views_per_day'].quantile(0.99)]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=sample_df, x='views_per_day', y='likes_to_views_ratio', hue='category_name', alpha=0.5, palette='tab10', legend=False)
sns.regplot(data=sample_df, x='views_per_day', y='likes_to_views_ratio', scatter=False, color='black', line_kws={'linestyle':'--'})

plt.title('속도(Velocity)와 품질(Quality)의 딜레마', fontproperties=font_prop, fontsize=15)
plt.xlabel('일평균 조회수 (Velocity)', fontproperties=font_prop)
plt.ylabel('좋아요/조회수 비율 (Quality Proxy)', fontproperties=font_prop)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'v5_5_velocity_quality_scatter.png'))
plt.close()
print("5. Velocity vs Quality 완료")

print("5차 분석 시각화 완료.")
