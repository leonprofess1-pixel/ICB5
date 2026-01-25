import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
# 워드 클라우드 생성을 위해 wordcloud 라이브러리가 필요합니다.
# 설치: pip install wordcloud
try:
    from wordcloud import WordCloud
except ImportError:
    print("WordCloud 라이브러리가 설치되어 있지 않습니다. 'pip install wordcloud'로 설치해주세요.")
    WordCloud = None
import matplotlib.cm as cm


# --- Configuration ---
plt.rc('font', family='Malgun Gothic') # Windows default
plt.rcParams['axes.unicode_minus'] = False
# Explicitly avoiding seaborn style settings as requested, though using seaborn for complex plots is allowed if style is not overridden.
# We will stick to pure matplotlib or pandas plotting for maximum control over fonts and style.

DATA_DIR = 'P2/data'
IMAGE_DIR = 'P2/images_v2'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- Data Loading ---
def load_data():
    print("Loading datasets...")
    return {
        'customers': pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv')),
        'orders': pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv')),
        'items': pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv')),
        'payments': pd.read_csv(os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv')),
        'reviews': pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv')),
        'products': pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv')),
        'sellers': pd.read_csv(os.path.join(DATA_DIR, 'olist_sellers_dataset.csv')),
        'translation': pd.read_csv(os.path.join(DATA_DIR, 'product_category_name_translation.csv'))
    }

# --- Preprocessing ---
def preprocess_data(dfs):
    print("Preprocessing data...")
    orders = dfs['orders'].copy()
    items = dfs['items'].copy()
    products = dfs['products'].copy()
    translation = dfs['translation'].copy()
    sellers = dfs['sellers'].copy()
    
    # 1. Date Conversion
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 
                 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col])
        
    # 2. Product Category Translation
    products = products.merge(translation, on='product_category_name', how='left')
    products['product_category_name_english'] = products['product_category_name_english'].fillna(products['product_category_name'])
    
    # 3. Master DataFrame Creation (Order + Item + Product + Customer + Seller)
    order_items = orders.merge(items, on='order_id', how='inner')
    order_items_products = order_items.merge(products, on='product_id', how='left')
    order_items_products_sellers = order_items_products.merge(sellers, on='seller_id', how='left')
    full_df = order_items_products_sellers.merge(dfs['customers'], on='customer_id', how='left')
    
    return full_df, orders

# --- Analysis Functions ---

def analyze_revenue_trend(full_df):
    print("Analyzing Revenue Trends...")
    full_df['month_year'] = full_df['order_purchase_timestamp'].dt.to_period('M')
    
    monthly_stats = full_df.groupby('month_year').agg({
        'price': 'sum',
        'order_id': 'nunique'
    }).rename(columns={'price': 'Revenue', 'order_id': 'Order_Count'})
    
    monthly_stats.index = monthly_stats.index.astype(str)
    
    fig, ax1 = plt.subplots(figsize=(14, 7))
    
    ax1.bar(monthly_stats.index, monthly_stats['Revenue'], color='#1f77b4', alpha=0.6, label='Monthly Revenue')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Revenue (BRL)', color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    plt.xticks(rotation=45)
    
    ax2 = ax1.twinx()
    ax2.plot(monthly_stats.index, monthly_stats['Order_Count'], color='#d62728', marker='o', linewidth=2, label='Order Count')
    ax2.set_ylabel('Order Count', color='#d62728')
    ax2.tick_params(axis='y', labelcolor='#d62728')
    
    plt.title('Monthly Revenue & Order Volume Trend (Dual Axis)', fontsize=16)
    fig.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '1_revenue_order_trend.png'))
    plt.close()

def analyze_delivery_performance(orders, dfs):
    print("Analyzing Delivery Performance...")
    orders_delivered = orders[orders['order_status'] == 'delivered'].copy()
    orders_delivered['delivery_days'] = (orders_delivered['order_delivered_customer_date'] - orders_delivered['order_purchase_timestamp']).dt.days
    
    reviews = dfs['reviews'][['order_id', 'review_score']]
    orders_reviews = orders_delivered.merge(reviews, on='order_id', how='inner')
    
    plt.figure(figsize=(10, 6))
    data_to_plot = [orders_reviews[orders_reviews['review_score'] == s]['delivery_days'].dropna() for s in range(1, 6)]
    plt.boxplot(data_to_plot, labels=[1, 2, 3, 4, 5], showfliers=False)
    plt.title('Impact of Delivery Time on Review Score', fontsize=14)
    plt.xlabel('Review Score')
    plt.ylabel('Delivery Time (Days)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(IMAGE_DIR, '2_delivery_vs_review.png'))
    plt.close()
    
    orders_cust = orders_delivered.merge(dfs['customers'], on='customer_id', how='left')
    state_delivery = orders_cust.groupby('customer_state')['delivery_days'].mean().sort_values(ascending=False).head(15)
    
    plt.figure(figsize=(12, 6))
    state_delivery.plot(kind='bar', color='#2ca02c')
    plt.title('Average Delivery Time by State (Slowest 15)', fontsize=14)
    plt.xlabel('State')
    plt.ylabel('Avg Delivery Days')
    plt.xticks(rotation=0)
    plt.savefig(os.path.join(IMAGE_DIR, '3_delivery_by_state.png'))
    plt.close()

def analyze_pareto_categories(full_df):
    print("Analyzing Category Pareto...")
    cat_revenue = full_df.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False)
    
    total_revenue = cat_revenue.sum()
    cumulative_pct = cat_revenue.cumsum() / total_revenue * 100
    
    top_20 = cat_revenue.head(20)
    top_20_cum = cumulative_pct.loc[top_20.index]
    
    fig, ax1 = plt.subplots(figsize=(14, 7))
    
    ax1.bar(top_20.index, top_20.values, color='#ff7f0e')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Revenue', color='#ff7f0e')
    ax1.set_xticklabels(top_20.index, rotation=45, ha='right')
    
    ax2 = ax1.twinx()
    ax2.plot(top_20.index, top_20_cum.values, color='black', marker='D', ms=5)
    ax2.set_ylabel('Cumulative %', color='black')
    ax2.set_ylim(0, 110)
    ax2.axhline(80, color='grey', linestyle='--')
    
    plt.title('Pareto Analysis of Top 20 Categories (Revenue)', fontsize=16)
    fig.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '4_category_pareto.png'))
    plt.close()

def analyze_installments(dfs):
    print("Analyzing Payment Installments...")
    payments = dfs['payments']
    cc_payments = payments[payments['payment_type'] == 'credit_card']
    
    installment_stats = cc_payments.groupby('payment_installments')['payment_value'].agg(['mean', 'count'])
    installment_stats = installment_stats[installment_stats.index <= 12]
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    ax1.bar(installment_stats.index, installment_stats['count'], color='#9467bd', alpha=0.7, label='Transaction Count')
    ax1.set_xlabel('Number of Installments')
    ax1.set_ylabel('Count', color='#9467bd')
    ax1.set_xticks(installment_stats.index)
    
    ax2 = ax1.twinx()
    ax2.plot(installment_stats.index, installment_stats['mean'], color='black', marker='o', linewidth=2, label='Avg Value')
    ax2.set_ylabel('Average Transaction Value (BRL)', color='black')
    
    plt.title('Credit Card Installments: Usage Volume vs Average Value', fontsize=14)
    fig.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '5_installments_analysis.png'))
    plt.close()

def analyze_freight_efficiency(full_df):
    print("Analyzing Freight Efficiency...")
    sample_df = full_df.sample(n=min(5000, len(full_df)), random_state=42)
    
    plt.figure(figsize=(10, 8))
    plt.scatter(sample_df['price'], sample_df['freight_value'], alpha=0.3, color='#e377c2')
    
    plt.title('Product Price vs Freight Value', fontsize=14)
    plt.xlabel('Product Price (BRL)')
    plt.ylabel('Freight Value (BRL)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.savefig(os.path.join(IMAGE_DIR, '6_price_vs_freight_log.png'))
    plt.close()

def analyze_time_heatmap(orders):
    print("Analyzing Order Time Heatmap...")
    orders['day_of_week'] = orders['order_purchase_timestamp'].dt.day_name()
    orders['hour'] = orders['order_purchase_timestamp'].dt.hour
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    orders['day_of_week'] = pd.Categorical(orders['day_of_week'], categories=days_order, ordered=True)
    
    heatmap_data = orders.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(12, 6))
    plt.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    
    plt.colorbar(label='Number of Orders')
    plt.xticks(range(24), range(24))
    plt.yticks(range(7), days_order)
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.title('Order Volume Heatmap (Day vs Hour)', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '7_order_time_heatmap.png'))
    plt.close()

# --- New Analysis Functions ---

def analyze_clustered_bar_review_payment_category(merged_df):
    print("Analyzing Review Score vs. Payment Type for top 5 Categories...")
    top_categories = merged_df['product_category_name_english'].value_counts().nlargest(5).index
    df_top_cat = merged_df[merged_df['product_category_name_english'].isin(top_categories)]

    pivot_df = df_top_cat.groupby(['product_category_name_english', 'payment_type'])['review_score'].mean().unstack()
    
    pivot_df.plot(kind='bar', figsize=(15, 8), width=0.8)
    plt.title('Top 5 Categories: Average Review Score by Payment Type', fontsize=16)
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Average Review Score', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Payment Type')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '8_clustered_bar_review_payment_category.png'))
    plt.close()

def analyze_stacked_bar_order_status_state(merged_df):
    print("Analyzing Order Status Distribution per Top 10 Customer States...")
    top_states = merged_df['customer_state'].value_counts().nlargest(10).index
    df_top_states = merged_df[merged_df['customer_state'].isin(top_states)]
    
    status_by_state = df_top_states.groupby(['customer_state', 'order_status']).size().unstack(fill_value=0)
    status_by_state = status_by_state.loc[top_states] # Preserve order
    
    status_by_state.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='viridis')
    plt.title('Order Status Distribution in Top 10 States', fontsize=16)
    plt.xlabel('Customer State', fontsize=12)
    plt.ylabel('Number of Orders', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Order Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '9_stacked_bar_order_status_state.png'))
    plt.close()

def analyze_donut_payment_by_price(merged_df):
    print("Analyzing Payment Type Distribution for High/Low Price Tiers...")
    merged_df['price_tier'] = pd.cut(merged_df['price'], bins=[0, 100, np.inf], labels=['<= 100 BRL', '> 100 BRL'])
    payment_dist = merged_df.groupby(['price_tier', 'payment_type']).size().unstack(fill_value=0)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    for i, tier in enumerate(payment_dist.index):
        ax = axes[i]
        ax.pie(payment_dist.loc[tier], labels=payment_dist.columns, autopct='%1.1f%%', startangle=90,
               wedgeprops=dict(width=0.4), pctdistance=0.8)
        ax.set_title(f'Payment Types for Price Tier: {tier}', fontsize=14)

    plt.suptitle('Donut Chart of Payment Types by Price Tier', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '10_donut_payment_by_price.png'))
    plt.close()

def analyze_bubble_price_freight_review(merged_df):
    print("Analyzing Price, Freight Value, and Review Score Relationship...")
    # Sample to avoid overplotting
    sample_df = merged_df.dropna(subset=['price', 'freight_value', 'review_score']).sample(n=2000, random_state=42)

    plt.figure(figsize=(14, 8))
    scatter = plt.scatter(
        sample_df['price'],
        sample_df['freight_value'],
        s=sample_df['payment_value'] / 5,  # Bubble size by payment value
        c=sample_df['review_score'], # Color by review score
        cmap='coolwarm',
        alpha=0.6
    )
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Price (Log Scale)', fontsize=12)
    plt.ylabel('Freight Value (Log Scale)', fontsize=12)
    plt.title('Price vs. Freight Value (Bubble Size: Payment Value, Color: Review Score)', fontsize=16)
    
    cbar = plt.colorbar(scatter)
    cbar.set_label('Review Score')
    
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '11_bubble_chart_price_freight_review.png'))
    plt.close()

def analyze_correlation_heatmap(merged_df):
    print("Analyzing Correlation Heatmap of Numerical Features...")
    numerical_cols = ['price', 'freight_value', 'product_weight_g', 'review_score', 'payment_installments', 'delivery_days']
    
    # Calculate delivery days for correlation
    merged_df['delivery_days'] = (merged_df['order_delivered_customer_date'] - merged_df['order_purchase_timestamp']).dt.days
    
    corr_df = merged_df[numerical_cols].dropna()
    correlation_matrix = corr_df.corr()

    plt.figure(figsize=(10, 8))
    plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='none', aspect='auto')
    plt.colorbar(label='Correlation Coefficient')
    plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45, ha='right')
    plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
    
    # Add text annotations
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            plt.text(j, i, f"{correlation_matrix.iloc[i, j]:.2f}", ha='center', va='center', color='white', fontsize=10)

    plt.title('Correlation Heatmap of Key Numerical Features', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '12_correlation_heatmap.png'))
    plt.close()

def analyze_box_payment_value_seller_state(merged_df):
    print("Analyzing Payment Value by Seller State and Payment Type...")
    top_seller_states = merged_df['seller_state'].value_counts().nlargest(5).index
    top_payment_types = ['credit_card', 'boleto']
    
    df_filtered = merged_df[
        (merged_df['seller_state'].isin(top_seller_states)) & 
        (merged_df['payment_type'].isin(top_payment_types))
    ]
    
    # For boxplot, we create a list of data for each group
    data_to_plot = []
    labels = []
    for state in top_seller_states:
        for p_type in top_payment_types:
            subset = df_filtered[(df_filtered['seller_state'] == state) & (df_filtered['payment_type'] == p_type)]['payment_value'].dropna()
            if not subset.empty:
                data_to_plot.append(subset)
                labels.append(f"{state}\n({p_type})")

    plt.figure(figsize=(16, 8))
    plt.boxplot(data_to_plot, labels=labels, showfliers=False) # showfliers=False to focus on distribution
    plt.title('Payment Value Distribution: Top 5 Seller States by Payment Type', fontsize=16)
    plt.xlabel('Seller State and Payment Type', fontsize=12)
    plt.ylabel('Payment Value (BRL)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '13_boxplot_payment_value_state_type.png'))
    plt.close()

def analyze_hbar_seller_city_orders(merged_df):
    print("Analyzing Top 10 Seller Cities by Orders and Review Score...")
    city_stats = merged_df.groupby('seller_city').agg(
        order_count=('order_id', 'nunique'),
        avg_review_score=('review_score', 'mean')
    ).nlargest(10, 'order_count')

    city_stats = city_stats.sort_values('order_count', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(city_stats.index, city_stats['order_count'], color='skyblue')
    ax.set_xlabel('Number of Unique Orders', fontsize=12)
    ax.set_ylabel('Seller City', fontsize=12)
    ax.set_title('Top 10 Seller Cities by Order Count with Avg. Review Score', fontsize=16)

    # Annotate with average review score
    for i, bar in enumerate(bars):
        width = bar.get_width()
        city_name = city_stats.index[i]
        avg_score = city_stats.loc[city_name]['avg_review_score']
        ax.text(width + 5, bar.get_y() + bar.get_height()/2., f'score: {avg_score:.2f}', va='center')

    plt.xlim(right=ax.get_xlim()[1] * 1.15) # Make more space for annotations
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '14_hbar_seller_city_orders.png'))
    plt.close()

def analyze_stacked_area_revenue_category(merged_df):
    print("Analyzing Cumulative Revenue by Top 5 Product Categories...")
    top_categories = merged_df.groupby('product_category_name_english')['price'].sum().nlargest(5).index
    df_top_cat = merged_df[merged_df['product_category_name_english'].isin(top_categories)].copy()
    
    df_top_cat['month_year'] = df_top_cat['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    revenue_by_cat_time = df_top_cat.groupby(['month_year', 'product_category_name_english'])['price'].sum().unstack(fill_value=0)
    
    plt.figure(figsize=(15, 8))
    plt.stackplot(revenue_by_cat_time.index, revenue_by_cat_time.T, labels=revenue_by_cat_time.columns, alpha=0.8)
    plt.title('Monthly Revenue by Top 5 Product Categories', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Revenue (BRL)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Product Category', loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '15_stacked_area_revenue_category.png'))
    plt.close()

def analyze_word_cloud_category(merged_df):
    print("Generating Word Cloud for Product Categories...")
    if WordCloud is None:
        print("Skipping Word Cloud generation as the library is not installed.")
        return
        
    cat_stats = merged_df.groupby('product_category_name_english').agg(
        frequency=('order_id', 'nunique'),
        avg_score=('review_score', 'mean')
    ).dropna()

    # Create a color function
    min_score, max_score = cat_stats['avg_score'].min(), cat_stats['avg_score'].max()
    def color_func(word, **kwargs):
        score = cat_stats.loc[word, 'avg_score']
        # Normalize score to 0-1 range
        norm_score = (score - min_score) / (max_score - min_score) if (max_score - min_score) > 0 else 0.5
        # Map to a colormap and convert to integer RGB string
        rgba_float = cm.coolwarm(norm_score)
        r = int(rgba_float[0] * 255)
        g = int(rgba_float[1] * 255)
        b = int(rgba_float[2] * 255)
        return f"rgb({r}, {g}, {b})"

    wc = WordCloud(width=1200, height=800, background_color='white', color_func=color_func).generate_from_frequencies(cat_stats['frequency'])

    plt.figure(figsize=(15, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('Product Categories (Size: Order Count, Color: Avg Review Score)', fontsize=16)
    plt.savefig(os.path.join(IMAGE_DIR, '16_word_cloud_categories.png'))
    plt.close()

def analyze_violin_price_category_review(merged_df):
    print("Analyzing Price Distribution by Category and Review Score...")
    top_categories = merged_df['product_category_name_english'].value_counts().nlargest(4).index
    df_filtered = merged_df[merged_df['product_category_name_english'].isin(top_categories)].copy()
    df_filtered['review_tier'] = pd.cut(df_filtered['review_score'], bins=[0, 3, 5], labels=['Low (1-3)', 'High (4-5)'])

    fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharey=True)
    axes = axes.flatten()

    for i, category in enumerate(top_categories):
        ax = axes[i]
        subset = df_filtered[df_filtered['product_category_name_english'] == category]
        
        low_review_prices = subset[subset['review_tier'] == 'Low (1-3)']['price'].dropna()
        high_review_prices = subset[subset['review_tier'] == 'High (4-5)']['price'].dropna()
        
        if not low_review_prices.empty and not high_review_prices.empty:
            parts = ax.violinplot([low_review_prices, high_review_prices], showmedians=True, widths=0.9)
            # Customizing colors
            for pc, color in zip(parts['bodies'], ['lightblue', 'lightgreen']):
                pc.set_facecolor(color)
            parts['cmedians'].set_color('red')
                
        ax.set_xticks([1, 2])
        ax.set_xticklabels(['Low Review', 'High Review'])
        ax.set_title(category, fontsize=12)
        ax.set_yscale('log')
        ax.grid(True, which="both", ls="--", alpha=0.4)

    plt.suptitle('Violin Plot: Price Distribution by Review Tier for Top 4 Categories (Log Scale)', fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(IMAGE_DIR, '17_violin_price_category_review.png'))
    plt.close()


def main():
    dfs = load_data()
    full_df, orders = preprocess_data(dfs)
    
    # --- Original Analysis ---
    analyze_revenue_trend(full_df)
    analyze_delivery_performance(orders, dfs)
    analyze_pareto_categories(full_df)
    analyze_installments(dfs)
    analyze_freight_efficiency(full_df)
    analyze_time_heatmap(orders)
    
    # --- New Analysis ---
    # Create a comprehensive dataframe for new plots
    reviews = dfs['reviews'][['order_id', 'review_score']]
    payments = dfs['payments'][['order_id', 'payment_type', 'payment_installments', 'payment_value']]
    
    merged_df = full_df.merge(reviews, on='order_id', how='left')
    merged_df = merged_df.merge(payments, on='order_id', how='left')
    
    # Call new analysis functions
    analyze_clustered_bar_review_payment_category(merged_df)
    analyze_stacked_bar_order_status_state(merged_df)
    analyze_donut_payment_by_price(merged_df)
    analyze_bubble_price_freight_review(merged_df)
    analyze_correlation_heatmap(merged_df)
    analyze_box_payment_value_seller_state(merged_df)
    analyze_hbar_seller_city_orders(merged_df)
    analyze_stacked_area_revenue_category(merged_df)
    analyze_word_cloud_category(merged_df)
    analyze_violin_price_category_review(merged_df)
    
    print("Advanced EDA Complete. 17 images saved to P2/images_v2")

if __name__ == "__main__":
    main()