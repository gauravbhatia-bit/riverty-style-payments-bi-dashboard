
# 💳 Payments BI Dashboard — Riverty-Style Financial Analytics

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-FF6B6B?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)

A 3-page interactive Power BI dashboard analysing **100,000+ real e-commerce payment transactions**, 
built to demonstrate BI self-service skills relevant to FinTech payment analytics — 
modelled after the kind of reporting used at companies like Riverty (Bertelsmann Group).

---

## 📊 Dashboard Pages

### Page 1 — Executive Overview
- Total Revenue: **$15.99M** across 99K orders
- Delivery Success Rate: **97.02%**
- Average Review Score: **4.09 / 5**
- Monthly revenue trend by year (2016–2018)
- Revenue breakdown by payment type (credit card dominates at 78%)
- Order volume by fulfilment status

### Page 2 — Payment & BNPL Analysis
- Instalment Rate: **51%** of orders use instalments
- Average Order Value: **$154.85**
- Average Instalments: **2.86**
- Revenue by payment type (credit card, boleto, voucher, debit card)
- Instalment rate trend across months
- Payment value vs instalment count distribution

### Page 3 — Delivery Performance
- Average Delivery Time: **12.09 days**
- Delivery time distribution (histogram) — peak at 5–10 days
- Monthly delivery trend showing seasonal patterns
- Geographic breakdown: **RR state averages 29 days vs SP at 9 days**

---

## 🗂️ Data Model — Star Schema
fact_orders ──── dim_customers
│
├────────── fact_payments
│
├────────── fact_items ──── dim_products
│ └──── dim_sellers
│
└────────── dim_reviews


**3 Fact Tables:** `fact_orders`, `fact_payments`, `fact_items`  
**4 Dimension Tables:** `dim_customers`, `dim_products`, `dim_sellers`, `dim_reviews`

---

## 🧮 DAX Measures

```dax
Total Revenue = SUM(fact_payments[payment_value])

Delivery Success Rate = 
FORMAT(DIVIDE([Delivered Orders], [Total Orders], 0), "0.00%")

Instalment Rate = 
FORMAT(DIVIDE([Instalment Orders], [Total Orders], 0), "0%")

Revenue YoY Growth = 
VAR CurrentYear = CALCULATE(SUM(fact_payments[payment_value]))
VAR PrevYear = CALCULATE(SUM(fact_payments[payment_value]), 
               SAMEPERIODLASTYEAR(fact_orders[order_purchase_timestamp]))
RETURN DIVIDE(CurrentYear - PrevYear, PrevYear, 0)
```

---

## ⚙️ ETL Pipeline (Python)

Raw data → cleaned using `pandas` → exported as star schema CSVs → imported into Power BI
olist_raw/ olist_clean/
├── olist_orders_dataset ├── fact_orders.csv
├── olist_order_payments ───► ├── fact_payments.csv
├── olist_order_items ├── fact_items.csv
├── olist_customers ├── dim_customers.csv
├── olist_products ├── dim_products.csv
├── olist_sellers ├── dim_sellers.csv
└── olist_order_reviews └── dim_reviews.csv


---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Power BI Desktop | Dashboard, DAX measures, data modelling |
| Python (pandas) | ETL pipeline, data cleaning, star schema export |
| DAX | KPI measures, YoY growth, rate calculations |
| Star Schema | Optimised relational data model |

---

## 📁 Repository Structure
riverty-style-payments-bi-dashboard/
├── data/
│ └── (download from Kaggle: olistbr/brazilian-ecommerce)
├── etl_pipeline.py
├── olist_payments_dashboard.pbix
├── screenshots/
│ ├── page1_executive.png
│ ├── page2_payments.png
│ └── page3_delivery.png
└── README.md


---

## 📦 Dataset

**Brazilian E-Commerce Public Dataset by Olist**  
Source: [Kaggle — olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
100,000 orders | 2016–2018 | 8 relational tables

---

## 👤 Author

**Gaurav Bhatia**  
MSc Data Science — GISMA University, Berlin  
[LinkedIn](https://linkedin.com/in/gaurav-bhatia-5a5a83184) | [GitHub](https://github.com/gauravbhatia-bit)
