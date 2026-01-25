# -*- coding: utf-8 -*-
"""
Team-ready Preprocess Pipeline (OLIST)

- Single entry file
- RAW → processed mart
- Preprocess validation
- report_preprocess.md auto generation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import json
from pathlib import Path
from datetime import datetime

# ======================================================
# 0. BASIC CONFIG (팀원이 건드릴 부분)
# ======================================================
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROC_DIR = BASE_DIR / "data" / "processed"
FIG_DIR = BASE_DIR / "outputs" / "preprocess_figures"
REPORT_PATH = BASE_DIR / "report_preprocess.md"
META_PATH = PROC_DIR / "mart_metadata.json"

PROC_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ======================================================
# 1. 한글 폰트 (팀 공통 환경 대응)
# ======================================================
def set_korean_font():
    system = platform.system()
    if system == "Windows":
        plt.rcParams["font.family"] = "Malgun Gothic"
    elif system == "Darwin":
        plt.rcParams["font.family"] = "AppleGothic"
    else:
        plt.rcParams["font.family"] = "Noto Sans CJK KR"
    plt.rcParams["axes.unicode_minus"] = False

set_korean_font()

# ======================================================
# 2. Load RAW
# ======================================================
def read(name):
    return pd.read_csv(RAW_DIR / name)

orders = read("olist_orders_dataset.csv")
customers = read("olist_customers_dataset.csv")
items = read("olist_order_items_dataset.csv")
payments = read("olist_order_payments_dataset.csv")
reviews = read("olist_order_reviews_dataset.csv")
products = read("olist_products_dataset.csv")
sellers = read("olist_sellers_dataset.csv")
geo = read("olist_geolocation_dataset.csv")
cat_tr = read("product_category_name_translation.csv")

# ======================================================
# 3. Datetime 정규화
# ======================================================
dt_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for c in dt_cols:
    orders[c] = pd.to_datetime(orders[c], errors="coerce")

# ======================================================
# 4. GEO 대표 좌표 + 품질 체크
# ======================================================
geo_rep = geo.groupby("geolocation_zip_code_prefix", as_index=False).agg(
    lat=("geolocation_lat", "median"),
    lng=("geolocation_lng", "median"),
    lat_std=("geolocation_lat", "std"),
    lng_std=("geolocation_lng", "std")
).rename(columns={"geolocation_zip_code_prefix": "zip_prefix"})

geo_rep.to_csv(PROC_DIR / "geo_zip_state_city.csv", index=False, encoding="utf-8-sig")

# ======================================================
# 5. 주문 상태 플래그
# ======================================================
orders["is_delivered"] = (orders["order_status"] == "delivered").astype(int)
orders["is_canceled"] = orders["order_status"].isin(
    ["canceled", "unavailable"]
).astype(int)

# ======================================================
# 6. ITEM / PAYMENT / REVIEW 집계
# ======================================================
item_agg = items.groupby("order_id", as_index=False).agg(
    revenue_price=("price", "sum"),
    revenue_freight=("freight_value", "sum"),
    n_items=("order_item_id", "count")
)
item_agg["revenue_total"] = item_agg["revenue_price"] + item_agg["revenue_freight"]

payment_agg = payments.groupby("order_id", as_index=False).agg(
    payment_value=("payment_value", "sum"),
    n_payments=("payment_sequential", "max")
)

review_agg = reviews.groupby("order_id", as_index=False).agg(
    review_score=("review_score", "mean"),
    has_review=("review_id", lambda x: int(x.notna().any()))
)

# ======================================================
# 7. CORE MART (주문 기준)
# ======================================================
mart_core = (
    orders.merge(customers, on="customer_id", how="left")
    .merge(item_agg, on="order_id", how="left")
    .merge(payment_agg, on="order_id", how="left")
    .merge(review_agg, on="order_id", how="left")
)

# 시간 파생
mart_core["order_date"] = mart_core["order_purchase_timestamp"].dt.date
mart_core["order_week"] = mart_core["order_purchase_timestamp"].dt.to_period("W").astype(str)
mart_core["order_month"] = mart_core["order_purchase_timestamp"].dt.to_period("M").astype(str)

# 배송 파생
mart_core["delivery_lead_days"] = (
    mart_core["order_delivered_customer_date"]
    - mart_core["order_purchase_timestamp"]
).dt.days

mart_core["delivery_delay_days"] = (
    mart_core["order_delivered_customer_date"]
    - mart_core["order_estimated_delivery_date"]
).dt.days

# ======================================================
# 8. MART 분리 (역할 명확화)
# ======================================================
mart_core.to_csv(PROC_DIR / "mart_order_core.csv", index=False, encoding="utf-8-sig")

mart_logistics = mart_core[
    ["order_id", "delivery_lead_days", "delivery_delay_days", "is_delivered"]
]
mart_logistics.to_csv(PROC_DIR / "mart_order_logistics.csv", index=False, encoding="utf-8-sig")

mart_experience = mart_core[
    ["order_id", "payment_value", "n_payments", "review_score", "has_review"]
]
mart_experience.to_csv(PROC_DIR / "mart_order_experience.csv", index=False, encoding="utf-8-sig")

# ======================================================
# 9. 전처리 검증 시각화
# ======================================================
missing = mart_core.isna().mean().sort_values(ascending=False).head(15)
missing.plot(kind="bar", title="결측 비율 TOP15")
plt.tight_layout()
plt.savefig(FIG_DIR / "missing_ratio.png", dpi=200)
plt.close()

status_ratio = orders["order_status"].value_counts(normalize=True)
status_ratio.plot(kind="bar", title="주문 상태 비율")
plt.tight_layout()
plt.savefig(FIG_DIR / "order_status_ratio.png", dpi=200)
plt.close()

lead = mart_core["delivery_lead_days"].dropna()
lead = lead[(lead >= 0) & (lead <= lead.quantile(0.99))]
plt.boxplot(lead, vert=False)
plt.title("배송 리드타임 분포 (상위 1% 컷)")
plt.tight_layout()
plt.savefig(FIG_DIR / "delivery_leadtime_box.png", dpi=200)
plt.close()

# ======================================================
# 10. Metadata 저장
# ======================================================
metadata = {
    "unit": "order",
    "revenue_definition": "price + freight_value",
    "time_base": "order_purchase_timestamp",
    "geo_representation": "zip_prefix median lat/lng",
    "generated_at": datetime.now().isoformat(),
    "generated_by": "preprocess.py"
}

META_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

# ======================================================
# 11. REPORT 생성
# ======================================================
REPORT_PATH.write_text(f"""
# OLIST 전처리 보고서 (Team Version)

## 목적
본 전처리는 팀 공용 분석을 위한 **단일 기준 데이터셋 생성**을 목적으로 한다.

---

## 핵심 기준
- 관측 단위: 주문(order)
- 매출 정의: price + freight_value
- 시간 기준: order_purchase_timestamp
- 주문 상태 필터: delivered / canceled flag 분리
- Geo: zip_prefix 기준 대표 좌표

---

## 산출물
- mart_order_core.csv
- mart_order_logistics.csv
- mart_order_experience.csv
- geo_zip_state_city.csv
- mart_metadata.json

---

## 전처리 검증
### 결측 비율
![](outputs/preprocess_figures/missing_ratio.png)

### 주문 상태 분포
![](outputs/preprocess_figures/order_status_ratio.png)

### 배송 리드타임
![](outputs/preprocess_figures/delivery_leadtime_box.png)

---

## 유의사항
- canceled/unavailable 주문은 분석 목적에 따라 제외 필요
- geo 좌표 분산이 큰 지역은 공간 분석 시 주의 필요
""", encoding="utf-8")

print("✅ Team-ready preprocess completed.")
