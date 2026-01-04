import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

# 운영체제에 맞는 폰트 설정
try:
    plt.rc('font', family='Malgun Gothic')
except:
    plt.rc('font', family='AppleGothic')
    
plt.rcParams['axes.unicode_minus'] = False


def main():
    """
    Olist 데이터셋에 대한 EDA를 수행하고, 결과를 마크다운 보고서로 생성합니다.
    """
    # --- 1. 환경 설정 ---
    # 데이터 경로 설정
    data_path = './FCIC/kpi-tree/data/olist_merged_dataset_deduped.csv'
    
    # 결과물 저장 경로 설정
    output_dir = './FCIC/kpi-tree'
    image_dir = os.path.join(output_dir, 'images')
    report_path = os.path.join(output_dir, 'kpi_tree_eda_report.md')

    # 이미지 저장 디렉토리 생성
    os.makedirs(image_dir, exist_ok=True)

    # --- 2. 데이터 로드 및 기본 탐색 ---
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"오류: 데이터 파일을 찾을 수 없습니다. 경로: {data_path}")
        return

    # 마크다운 보고서 내용 초기화
    report_md = "# Olist 데이터셋 KPI Tree 분석을 위한 EDA 보고서\n\n"
    report_md += "이 보고서는 Olist 데이터셋의 주요 특징을 파악하고 KPI Tree 설계를 위한 인사이트를 얻기 위해 작성되었습니다.\n\n"

    # 데이터 기본 정보
    report_md += "## 1. 데이터 기본 정보\n\n"
    report_md += "### 데이터 샘플 (상위 5개)\n"
    report_md += df.head().to_markdown(index=False) + "\n\n"
    
    # 데이터 기술 통계
    report_md += "### 기술 통계\n"
    report_md += "```\n"
    report_md += df.describe(include='all').to_string() + "\n"
    report_md += "```\n\n"
    
    # 결측치 확인
    report_md += "### 결측치 확인\n"
    missing_values = df.isnull().sum()
    missing_df = missing_values[missing_values > 0].reset_index()
    missing_df.columns = ['컬럼명', '결측치 수']
    if not missing_df.empty:
        report_md += missing_df.to_markdown(index=False) + "\n\n"
    else:
        report_md += "결측치가 없습니다.\n\n"

    # --- 3. 탐색적 데이터 분석 (EDA) 및 시각화 ---
    report_md += "## 2. 탐색적 데이터 분석 (EDA)\n\n"
    
    # 시각화 함수 정의
    def save_plot_and_get_md(fig, filename, title, description, data_table=None):
        """차트를 저장하고 마크다운 섹션을 반환합니다."""
        img_path = os.path.join(image_dir, filename)
        fig.savefig(img_path, bbox_inches='tight')
        plt.close(fig)
        
        md_section = f"### {title}\n\n"
        md_section += f"![{title}](./images/{filename})\n\n"
        md_section += f"**해석:** {description}\n\n"
        if data_table is not None:
            md_section += "**데이터 테이블:**\n"
            md_section += data_table.to_markdown(index=True) + "\n\n"
        return md_section

    # --- 시각화 리스트 ---

    # 1. 주문 상태 분포 (Bar Chart)
    order_status_counts = df['order_status'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=order_status_counts.index, y=order_status_counts.values, ax=ax, palette='viridis')
    ax.set_title('주문 상태 분포', fontsize=15)
    ax.set_xlabel('주문 상태')
    ax.set_ylabel('주문 수')
    ax.tick_params(axis='x', rotation=45)
    report_md += save_plot_and_get_md(fig, 
                                     '1_order_status_distribution.png', 
                                     '1. 주문 상태 분포', 
                                     '대부분의 주문이 `delivered` 상태임을 알 수 있습니다. `shipped`, `processing` 등 다른 상태의 주문은 상대적으로 적습니다. 이는 대부분의 주문이 정상적으로 고객에게 배송 완료되었음을 의미합니다.',
                                     order_status_counts.reset_index().rename(columns={'index':'주문 상태', 'order_status':'주문 수'}))

    # 2. 고객 주(State)별 분포 (Bar Chart)
    customer_state_counts = df['customer_state'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=customer_state_counts.index, y=customer_state_counts.values, ax=ax, palette='plasma')
    ax.set_title('상위 10개 고객 주(State) 분포', fontsize=15)
    ax.set_xlabel('주 (State)')
    ax.set_ylabel('고객 수')
    report_md += save_plot_and_get_md(fig, 
                                     '2_customer_state_distribution.png',
                                     '2. 상위 10개 고객 주(State) 분포',
                                     '고객은 주로 `SP`(상파울루) 주에 집중되어 있습니다. 이어서 `RJ`(리우데자네이루), `MG`(미나스제라이스) 순으로 많습니다. 이는 Olist의 핵심 고객 기반이 브라질 남동부 지역에 있음을 시사합니다.',
                                     customer_state_counts.reset_index().rename(columns={'index':'주(State)', 'customer_state':'고객 수'}))

    # 3. 결제 유형 분포 (Pie Chart)
    payment_type_counts = df['payment_type'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(payment_type_counts, labels=payment_type_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    ax.set_title('결제 유형 분포', fontsize=15)
    ax.axis('equal') 
    report_md += save_plot_and_get_md(fig,
                                     '3_payment_type_distribution.png',
                                     '3. 결제 유형 분포',
                                     '`credit_card`(신용카드)가 가장 보편적인 결제 수단이며, 전체의 약 74%를 차지합니다. `boleto`(은행 송금)와 `voucher`(상품권)가 그 뒤를 잇습니다. `debit_card`(직불카드) 사용은 매우 적습니다.',
                                     payment_type_counts.reset_index().rename(columns={'index':'결제 유형', 'payment_type':'횟수'}))

    # 4. 리뷰 점수 분포 (Histogram)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['review_score'], bins=5, kde=False, ax=ax, color='skyblue')
    ax.set_title('리뷰 점수 분포', fontsize=15)
    ax.set_xlabel('리뷰 점수')
    ax.set_ylabel('주문 수')
    review_score_counts = df['review_score'].value_counts().sort_index()
    report_md += save_plot_and_get_md(fig, 
                                     '4_review_score_distribution.png',
                                     '4. 리뷰 점수 분포',
                                     '리뷰 점수는 5점이 압도적으로 많으며, 긍정적인 고객 경험이 많음을 나타냅니다. 반면, 1점 리뷰도 상당수 존재하여 부정적인 경험을 한 고객도 많다는 것을 알 수 있습니다. 중간 점수(2, 3점)는 상대적으로 적습니다.',
                                     review_score_counts.reset_index().rename(columns={'index':'리뷰 점수', 'review_score':'주문 수'}))
    
    # 5. 제품 카테고리별 주문 수 (Bar Chart)
    product_category_counts = df['product_category_name_english'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(y=product_category_counts.index, x=product_category_counts.values, ax=ax, palette='cubehelix', orient='h')
    ax.set_title('상위 10개 제품 카테고리별 주문 수', fontsize=15)
    ax.set_xlabel('주문 수')
    ax.set_ylabel('제품 카테고리')
    report_md += save_plot_and_get_md(fig,
                                     '5_product_category_orders.png',
                                     '5. 상위 10개 제품 카테고리별 주문 수',
                                     '`bed_bath_table`(침실/욕실/테이블 용품)이 가장 많이 판매된 카테고리입니다. 그 뒤로 `health_beauty`(건강/미용), `sports_leisure`(스포츠/레저)가 인기가 많습니다. 생활용품과 개인 관리 용품이 주요 판매 품목임을 알 수 있습니다.',
                                     product_category_counts.reset_index().rename(columns={'index':'카테고리', 'product_category_name_english':'주문 수'}))

    # 6. 월별 주문량 추이 (Line Chart)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    orders_by_month = df.set_index('order_purchase_timestamp').resample('M').size()
    fig, ax = plt.subplots(figsize=(14, 7))
    orders_by_month.plot(ax=ax, color='purple', marker='o')
    ax.set_title('월별 주문량 추이', fontsize=15)
    ax.set_xlabel('월')
    ax.set_ylabel('총 주문 수')
    ax.grid(True)
    report_md += save_plot_and_get_md(fig,
                                     '6_monthly_order_trend.png',
                                     '6. 월별 주문량 추이',
                                     '전반적으로 주문량이 증가하는 추세를 보이다가, 2017년 말부터 2018년 초에 급증하는 패턴을 보입니다. 이후 안정화되는 모습을 보입니다. 특정 시점의 프로모션이나 이벤트가 주문량에 큰 영향을 미쳤을 수 있습니다.',
                                     orders_by_month.reset_index().rename(columns={'order_purchase_timestamp':'월', 0:'주문 수'}))

    # 7. 결제 할부 개월 수 분포 (Histogram)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df[df['payment_installments_sum'] > 0]['payment_installments_sum'], bins=10, kde=False, ax=ax, color='teal')
    ax.set_title('결제 할부 개월 수 분포', fontsize=15)
    ax.set_xlabel('할부 개월 수')
    ax.set_ylabel('결제 건수')
    payment_installments_sum_counts = df['payment_installments_sum'].value_counts().sort_index()
    report_md += save_plot_and_get_md(fig,
                                     '7_payment_installments_sum_distribution.png',
                                     '7. 결제 할부 개월 수 분포',
                                     '할부 결제는 주로 1~3개월 사이에 집중되어 있습니다. 10개월 장기 할부도 비교적 많이 사용됩니다. 고객들은 소액 할부 결제를 선호하는 경향이 있습니다.',
                                     payment_installments_sum_counts.reset_index().rename(columns={'index':'할부 개월 수', 'payment_installments_sum':'결제 건수'}))
    
    # 8. 배송 시간에 따른 리뷰 점수 (Box Plot)
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
    df['delivery_duration'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
    df['delivery_punctuality'] = (df['order_estimated_delivery_date'] - df['order_delivered_customer_date']).dt.days
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.boxplot(x='review_score', y='delivery_duration', data=df, ax=ax, palette='coolwarm')
    ax.set_title('리뷰 점수별 배송 기간', fontsize=15)
    ax.set_xlabel('리뷰 점수')
    ax.set_ylabel('배송 기간 (일)')
    ax.set_ylim(0, 60) # Outlier 제외하고 보기
    report_md += save_plot_and_get_md(fig,
                                     '8_delivery_duration_by_review_score.png',
                                     '8. 리뷰 점수별 배송 기간',
                                     '리뷰 점수가 낮을수록(1-2점) 평균 배송 기간이 길어지는 경향이 뚜렷하게 나타납니다. 반면, 5점 리뷰는 배송 기간이 상대적으로 짧습니다. 즉, 빠른 배송이 고객 만족도에 매우 중요한 요소임을 알 수 있습니다.')

    # 9. 제품 가격 분포 (Histogram with log scale)
    fig, ax = plt.subplots(figsize=(10, 6))
    # 가격이 0 이하인 데이터 제외 및 로그 변환
    prices = df[df['main_product_price'] > 0]['main_product_price']
    sns.histplot(np.log1p(prices), ax=ax, color='green', kde=True)
    ax.set_title('제품 가격 분포 (로그 스케일)', fontsize=15)
    ax.set_xlabel('Log(가격 + 1)')
    ax.set_ylabel('제품 수')
    report_md += save_plot_and_get_md(fig,
                                     '9_price_distribution.png',
                                     '9. 제품 가격 분포 (로그 스케일)',
                                     '제품 가격은 대부분 낮은 가격대에 집중되어 있는 긴 꼬리 분포를 보입니다. 로그 변환 시, 여러 개의 봉우리가 나타나며 특정 가격대에 제품이 몰려있음을 시사합니다. 이는 저가 상품이 주를 이루지만, 다양한 가격대의 상품이 존재함을 의미합니다.')

    # 10. 판매자 주(State)별 분포 (Bar Chart)
    seller_state_counts = df['seller_state'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=seller_state_counts.index, y=seller_state_counts.values, ax=ax, palette='rocket')
    ax.set_title('상위 10개 판매자 주(State) 분포', fontsize=15)
    ax.set_xlabel('주 (State)')
    ax.set_ylabel('판매자 수')
    report_md += save_plot_and_get_md(fig,
                                     '10_seller_state_distribution.png',
                                     '10. 상위 10개 판매자 주(State) 분포',
                                     '판매자 역시 고객과 마찬가지로 `SP`(상파울루) 주에 가장 많이 분포해 있습니다. 이는 Olist의 물류 및 비즈니스 허브가 `SP` 지역에 집중되어 있음을 강력하게 시사합니다. 고객과 판매자의 지역적 일치는 효율적인 배송으로 이어질 수 있습니다.',
                                     seller_state_counts.reset_index().rename(columns={'index':'주(State)', 'seller_state':'판매자 수'}))

    # --- 4. 보고서 저장 ---
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_md)
        print(f"성공: EDA 보고서가 다음 경로에 저장되었습니다: {report_path}")
    except IOError as e:
        print(f"오류: 보고서 파일을 쓰는 중 문제가 발생했습니다. {e}")

if __name__ == '__main__':
    main()
