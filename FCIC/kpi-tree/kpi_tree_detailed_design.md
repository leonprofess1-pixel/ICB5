# Role
저는 8년 차 이상의 시니어 이커머스 데이터 전략가이자 분석 전문가입니다. 주어진 데이터를 기반으로 `payment_value_sum`을 최상단 지표로 하는 **'수학적으로 증명 가능한 KPI Tree'**를 설계했습니다.

# Objective
단순한 지표 나열이 아니라, 상위 지표가 하위 지표의 합(+) 또는 곱(*)으로 어떻게 구성되는지 계층적으로 보여주고, 각 지표를 데이터로 산출할 수 있는 구체적인 산술 로직을 제공하는 것이 목표입니다.

---

## 1. KPI Hierarchy Decomposition Summary

- **L0: 총 결제액 (Total Payment Value)**
  - `$L0 = L1_A (총 주문 수) \times L1_B (주문당 평균 결제액)`

- **L1: L0의 1차 분해**
  - `$L1_A (총 주문 수) = L2_A (총 고객 수) \times L2_B (고객당 평균 주문 수)`
  - `$L1_B (주문당 평균 결제액) = L2_C (주문당 평균 상품 판매가) + L2_D (주문당 평균 배송비)`

- **L2: L1의 1차 분해**
  - `$L2_A (총 고객 수) = L3_A (신규 고객 수) + L3_B (재구매 고객 수)`
  - `$L2_C (주문당 평균 상품 판매가) = L3_C (주문당 평균 상품 수) \times L3_D (상품 평균 단가)`

- **L3: L2의 1차 분해**
  - `$L3_A (신규 고객 수) = \sum (L4_A (지역별 신규 고객 수))`
  - `$L3_C (주문당 평균 상품 수) = \text{Weighted Avg.} (L4_B (카테고리별 주문당 상품 수))`
  - `$L3_D (상품 평균 단가) = \text{Weighted Avg.} (L4_C (카테고리별 상품 평균 단가))`

---

## 2. Detailed Metric Tree & Definition

# L0: 총 결제액 (Total Payment Value)
- **정의**: 분석 기간 동안 발생한 모든 결제의 총합. 비즈니스의 최종적인 재무 성과.
- **산출 로직**: `SUM(payment_value_sum)`
- **유형**: [Output Metric]

## L1: 총 결제액의 구성 요소
### L1-A: 총 주문 수 (Total Orders)
- **정의**: 특정 기간 동안 발생한 총 주문 건수.
- **산출 로직**: `COUNT(DISTINCT order_id)`
- **유형**: [Output Metric]
### L1-B: 주문당 평균 결제액 (AOV: Average Order Value)
- **정의**: 고객이 한 번 주문할 때 평균적으로 지출하는 금액.
- **산출 로직**: `SUM(payment_value_sum) / COUNT(DISTINCT order_id)`
- **유형**: [Output Metric]

## L2: 주문과 고객, AOV의 구성 요소
### L2-A: 총 고객 수 (Total Customers)
- **정의**: 특정 기간 동안 한 번이라도 구매한 순수 고객의 수.
- **산출 로직**: `COUNT(DISTINCT customer_unique_id)`
- **유형**: [Output Metric]
### L2-B: 고객당 평균 주문 수 (Avg Orders per Customer)
- **정의**: 고객 한 명이 특정 기간 동안 평균적으로 몇 번 주문했는지를 나타내는 지표. 고객 충성도의 대리 지표.
- **산출 로직**: `COUNT(DISTINCT order_id) / COUNT(DISTINCT customer_unique_id)`
- **유형**: [Output Metric]
### L2-C: 주문당 평균 상품 판매가 (Avg Product Revenue per Order)
- **정의**: 하나의 주문에 포함된 상품들의 평균 판매가 합계.
- **산출 로직**: `SUM(main_product_price) / COUNT(DISTINCT order_id)`
- **유형**: [Output Metric]
### L2-D: 주문당 평균 배송비 (Avg Freight Revenue per Order)
- **정의**: 하나의 주문에 부과된 평균 배송비.
- **산출 로직**: `SUM(main_product_freight_value) / COUNT(DISTINCT order_id)`
- **유형**: [Input Metric]

## L3: 고객과 상품 판매가의 상세 분해
### L3-A: 신규 고객 수 (New Customers)
- **정의**: 분석 기간 내에 첫 구매를 한 고객의 수.
- **산출 로직**: `COUNT(DISTINCT customer_unique_id) WHERE (해당 고객의 첫 구매일이 분석 기간에 포함)`
- **유형**: [Output Metric]
### L3-B: 재구매 고객 수 (Repeat Customers)
- **정의**: 분석 기간 이전에 구매 이력이 있고, 해당 기간에 다시 구매한 고객의 수.
- **산출 로직**: `COUNT(DISTINCT customer_unique_id) WHERE (해당 고객의 첫 구매일이 분석 기간보다 이전)`
- **유형**: [Output Metric]
### L3-C: 주문당 평균 상품 수 (Avg Items per Order / Basket Size)
- **정의**: 고객이 한 번 주문할 때 평균적으로 몇 개의 상품을 구매하는지 나타내는 지표.
- **산출 로직**: `AVG(item_count)` 또는 `SUM(item_count) / COUNT(DISTINCT order_id)`
- **유형**: [Input Metric]
### L3-D: 상품 평균 단가 (Average Item Price)
- **정의**: 판매되는 상품 한 개의 평균적인 가격.
- **산출 로직**: `SUM(main_product_price) / SUM(item_count)`
- **유형**: [Input Metric]

## L4: 핵심 Input 지표의 상세 분해
### L4-A: 지역별 신규 고객 수 (New Customers by Region)
- **정의**: 특정 지역(`customer_state`)에서 유입된 신규 고객의 수. 지역별 마케팅 효율성을 측정하는 데 사용.
- **산출 로직**: `GROUP BY customer_state | COUNT(DISTINCT customer_unique_id) WHERE (첫 구매)`
- **유형**: [Input Metric]
### L4-B: 카테고리별 주문당 상품 수 (Avg Items per Order by Category)
- **정의**: 특정 상품 카테고리가 포함된 주문의 평균 상품 수. 크로스셀링 전략의 효과를 측정.
- **산출 로직**: `GROUP BY product_category_name_english | AVG(item_count)`
- **유형**: [Input Metric]
### L4-C: 카테고리별 상품 평균 단가 (Avg Item Price by Category)
- **정의**: 특정 상품 카테고리에 속한 상품들의 평균 단가. 고/저가 상품군 파악.
- **산출 로직**: `GROUP BY product_category_name_english | SUM(main_product_price) / SUM(item_count)`
- **유형**: [Input Metric]

## L5: 실행 가능한 최하위 지표
### L5-A: 도시별 신규 고객 수 (New Customers by City)
- **정의**: 특정 도시(`customer_city`)에서 유입된 신규 고객의 수. 더 세분화된 지역 타겟팅 성과 측정.
- **산출 로직**: `GROUP BY customer_state, customer_city | COUNT(DISTINCT customer_unique_id) WHERE (첫 구매)`
- **유형**: [Input Metric]
### L5-B: 판매자별 상품 평균 단가 (Avg Item Price by Seller)
- **정의**: 특정 판매자(`seller_id`)가 판매하는 상품들의 평균 단가. 판매자별 가격 정책 및 소싱 능력 파악.
- **산출 로직**: `GROUP BY seller_id | SUM(main_product_price) / SUM(item_count)`
- **유형**: [Input Metric]
### L5-C: 판매자별/카테고리별 주문당 상품 수 (Avg Items per Order by Seller/Category)
- **정의**: 특정 판매자가 특정 카테고리에서 판매한 주문의 평균 상품 수. 판매자의 상품 구색 및 판매 전략 파악.
- **산출 로직**: `GROUP BY seller_id, product_category_name_english | AVG(item_count)`
- **유형**: [Input Metric]

---

## 3. Data Implementation Strategy

`olist_merged_dataset_deduped.csv`의 컬럼들을 활용하여 KPI Tree의 복합 지표들을 구현하기 위한 논리적 가이드는 다음과 같습니다.

- **신규/재구매 고객 (New/Repeat Customer) 구분 로직**:
  1. 전체 데이터를 `customer_unique_id`로 그룹화하고, 각 고객의 `order_purchase_timestamp`를 시간순으로 정렬합니다.
  2. 각 `customer_unique_id`별로 첫 번째 `order_purchase_timestamp`를 '첫 구매일'로 정의하고, 나머지 구매는 '재구매'로 정의합니다.
  3. 분석하려는 특정 기간을 기준으로, 고객의 '첫 구매일'이 해당 기간 내에 있으면 '신규 고객'으로, 기간 이전에 있으면 '재구매 고객'으로 분류합니다.

- **배송 효율성 및 고객 만족도 (Delivery Efficiency & Customer Satisfaction) 연계 분석**:
  - **정시 배송 여부**: `order_delivered_customer_date`와 `order_estimated_delivery_date`를 비교하여 계산합니다. `(order_estimated_delivery_date - order_delivered_customer_date)`가 양수이면 정시 혹은 조기 배송, 음수이면 지연 배송으로 새로운 컬럼을 생성할 수 있습니다.
  - **만족도 연관 분석**: 위에서 생성한 '정시 배송 여부' 컬럼과 `review_score`를 함께 분석하여, 배송 품질이 고객 만족도에 미치는 영향을 파악할 수 있습니다. 예를 들어, 지연 배송된 주문들의 `review_score` 평균이 정시 배송된 주문들보다 유의미하게 낮은지 검증합니다. 이는 `L2-D (주문당 평균 배송비)`와 연계하여 배송 정책 최적화의 근거로 활용될 수 있습니다.

- **상품 카테고리 확장 분석 (Product Category Deep-dive)**:
  - `product_category_name_english`를 기준으로 데이터를 그룹화하여, `L4-B`와 `L4-C` 같은 지표를 산출합니다.
  - 이를 통해 어떤 카테고리가 높은 '상품 평균 단가'를 가지는지, 혹은 어떤 카테고리가 '주문당 평균 상품 수'를 높이는 데 기여하는지(크로스셀링에 유리한지) 파악할 수 있습니다.
  - 이 분석은 상품 구색(MD) 전략 및 프로모션 기획의 기초 자료로 사용됩니다.
