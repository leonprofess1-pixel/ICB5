
# Online Retail Dataset EDA Report

## 1. Data Overview
### Data Shape
<p>(397884, 9)</p>

### Data Head
|    |   InvoiceNo | StockCode   | Description                         |   Quantity | InvoiceDate         |   UnitPrice |   CustomerID | Country        |   TotalPrice |
|---:|------------:|:------------|:------------------------------------|-----------:|:--------------------|------------:|-------------:|:---------------|-------------:|
|  0 |      536365 | 85123A      | WHITE HANGING HEART T-LIGHT HOLDER  |          6 | 2010-12-01 08:26:00 |        2.55 |        17850 | United Kingdom |        15.3  |
|  1 |      536365 | 71053       | WHITE METAL LANTERN                 |          6 | 2010-12-01 08:26:00 |        3.39 |        17850 | United Kingdom |        20.34 |
|  2 |      536365 | 84406B      | CREAM CUPID HEARTS COAT HANGER      |          8 | 2010-12-01 08:26:00 |        2.75 |        17850 | United Kingdom |        22    |
|  3 |      536365 | 84029G      | KNITTED UNION FLAG HOT WATER BOTTLE |          6 | 2010-12-01 08:26:00 |        3.39 |        17850 | United Kingdom |        20.34 |
|  4 |      536365 | 84029E      | RED WOOLLY HOTTIE WHITE HEART.      |          6 | 2010-12-01 08:26:00 |        3.39 |        17850 | United Kingdom |        20.34 |

### Data Info
<pre><class 'pandas.core.frame.DataFrame'>
Index: 397884 entries, 0 to 541908
Data columns (total 9 columns):
 #   Column       Non-Null Count   Dtype         
---  ------       --------------   -----         
 0   InvoiceNo    397884 non-null  object        
 1   StockCode    397884 non-null  object        
 2   Description  397884 non-null  object        
 3   Quantity     397884 non-null  int64         
 4   InvoiceDate  397884 non-null  datetime64[ns]
 5   UnitPrice    397884 non-null  float64       
 6   CustomerID   397884 non-null  object        
 7   Country      397884 non-null  object        
 8   TotalPrice   397884 non-null  float64       
dtypes: datetime64[ns](1), float64(2), int64(1), object(5)
memory usage: 30.4+ MB
</pre>

## 2. Analysis Methods and Criteria
This report analyzes the Online Retail dataset to understand sales patterns and customer behavior. The analysis was conducted using the following methods and criteria:
1.  **Data Loading and Initial Exploration**
2.  **Data Cleaning and Preprocessing**
3.  **Exploratory Data Analysis (EDA)**
4.  **Visualization**

## 3. Data Cleaning and Preprocessing
### Missing Values
<pre>
InvoiceNo           0
StockCode           0
Description      1454
Quantity            0
InvoiceDate         0
UnitPrice           0
CustomerID     135080
Country             0
</pre>

After handling missing values:
<pre>
InvoiceNo      0
StockCode      0
Description    0
Quantity       0
InvoiceDate    0
UnitPrice      0
CustomerID     0
Country        0
TotalPrice     0
</pre>

## 4. Descriptive Statistics
|       |    Quantity |    UnitPrice |   TotalPrice |
|:------|------------:|-------------:|-------------:|
| count | 397884      | 397884       |   397884     |
| mean  |     12.9882 |      3.11649 |       22.397 |
| min   |      1      |      0.001   |        0.001 |
| 25%   |      2      |      1.25    |        4.68  |
| 50%   |      6      |      1.95    |       11.8   |
| 75%   |     12      |      3.75    |       19.8   |
| max   |  80995      |   8142.75    |   168470     |
| std   |    179.332  |     22.0979  |      309.071 |

## 5. User Activity Analysis (DAU/MAU)
### 1. 일일 활성 사용자 (DAU)
<p>Average DAU: 54.96</p>

### 2. 월간 활성 사용자 (MAU)
[Image: 월간 활성 사용자 (MAU)]
| YearMonth   |   CustomerID |
|:------------|-------------:|
| 2010-12     |          885 |
| 2011-01     |          741 |
| 2011-02     |          758 |
| 2011-03     |          974 |
| 2011-04     |          856 |
| 2011-05     |         1056 |
| 2011-06     |          991 |
| 2011-07     |          949 |
| 2011-08     |          935 |
| 2011-09     |         1266 |
| 2011-10     |         1364 |
| 2011-11     |         1664 |
| 2011-12     |          615 |

### 11. 시간-요일별 히트맵
[Image: 시간-요일별 히트맵]

### 12. 월단위 구매 고객 리텐션
[Image: 월단위 구매 고객 리텐션]

---

### Streamlit 대시보드 생성 프롬프트 (v2)

**목표:** `online-retail` 데이터셋의 EDA 결과를 시각화하는 대화형 웹 대시보드를 `streamlit`과 `plotly`를 사용하여 제작합니다. 이 대시보드는 탭(Tab) 구조를 통해 콘텐츠를 명확하게 분리하고, 데이터 검색 기능을 제공해야 합니다.

**전제 조건:**
- `eda.py` 파일에 정의된 데이터 전처리 및 분석 함수를 재사용하여 데이터를 준비합니다.
- 모든 시각화는 `plotly` 라이브러리만을 사용하여 생성합니다.
- 대시보드는 사용자가 데이터를 쉽게 탐색할 수 있도록 명확한 섹션으로 나누고, 적절한 제목과 설명을 포함해야 합니다.

**대시보드 구성 요구사항:**

1.  **사이드바 (Sidebar):**
    - 페이지 상단에 "Online Retail EDA Dashboard"라는 제목을 추가합니다.
    - 사용자가 전체 대시보드에 표시될 데이터를 필터링할 수 있도록 **국가(Country)**를 선택할 수 있는 멀티-선택(multi-select) 메뉴와 **날짜 범위(Date range)**를 선택할 수 있는 슬라이더를 배치합니다.

2.  **메인 화면 - 탭 구조:**
    - `st.tabs`를 사용하여 분석 내용을 "데이터 개요", "매출 분석", "고객 및 상품 분석", "사용자 활동 분석" 4개의 탭으로 분리합니다.

    - **"데이터 개요" 탭:**
        - "데이터 검색" 부제를 추가합니다.
        - `st.text_input`을 사용하여 사용자가 상품 설명(`Description`)을 검색할 수 있는 검색창을 추가합니다. 검색은 대소문자를 구분하지 않아야 합니다.
        - 검색 결과 또는 전체 데이터를 `st.dataframe`을 사용하여 테이블 형태로 보여줍니다.
        - 데이터의 전체 행과 열 개수(Shape)를 `st.metric`을 사용하여 표시합니다.

    - **"매출 분석" 탭:**
        - "매출 트렌드 분석"이라는 부제를 표시합니다.
        - **월별 매출 추이:** `plotly.express.line`을 사용하여 월별 총매출액(TotalPrice)을 보여주는 라인 차트를 생성합니다.
        - **요일별 매출:** `plotly.express.bar`를 사용하여 요일별 총매출액을 보여주는 바 차트를 생성합니다.
        - **시간-요일별 히트맵:** `plotly.express.imshow`를 사용하여 시간과 요일 조합에 따른 매출액을 히트맵으로 시각화합니다.

    - **"고객 및 상품 분석" 탭:**
        - "주요 고객 및 상품 분석"이라는 부제를 표시합니다.
        - **매출 상위 10개국:** `plotly.express.bar`를 사용하여 총매출액 기준 상위 10개 국가를 보여주는 수평 바 차트와, `plotly.express.choropleth`를 사용한 세계 지도를 함께 표시합니다.
        - **판매량 상위 10개 상품:** `plotly.express.bar`를 사용하여 총판매량(Quantity) 기준 상위 10개 상품을 보여주는 수평 바 차트를 생성합니다.
        - **단가와 수량의 관계:** `plotly.express.scatter`를 사용하여 단가와 수량 간의 관계를 나타내는 산점도를 생성합니다.

    - **"사용자 활동 분석" 탭:**
        - "사용자 활동 분석"이라는 부제를 표시합니다.
        - **월간 활성 사용자 (MAU):** 월별 활성 사용자 수를 `plotly.express.bar`를 사용하여 바 차트로 시각화합니다.
        - **월별 고객 리텐션:** 월별 코호트(cohort)를 기반으로 한 고객 리텐션을 `plotly.express.imshow`를 사용한 히트맵으로 시각화합니다. 각 셀에는 리텐션 비율(%)을 텍스트로 표시합니다.
