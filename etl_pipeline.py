import pandas as pd
import os

# ── CONFIG ──────────────────────────────────────────────────────────────────
RAW_PATH = r"C:\Users\gaura\Downloads\nfs\archive (1)"
OUT_PATH  = r"C:\Users\gaura\Downloads\olist_clean"
os.makedirs(OUT_PATH, exist_ok=True)

# ── LOAD RAW TABLES ─────────────────────────────────────────────────────────
orders    = pd.read_csv(os.path.join(RAW_PATH, "olist_orders_dataset.csv"))
payments  = pd.read_csv(os.path.join(RAW_PATH, "olist_order_payments_dataset.csv"))
items     = pd.read_csv(os.path.join(RAW_PATH, "olist_order_items_dataset.csv"))
customers = pd.read_csv(os.path.join(RAW_PATH, "olist_customers_dataset.csv"))
products  = pd.read_csv(os.path.join(RAW_PATH, "olist_products_dataset.csv"))
sellers   = pd.read_csv(os.path.join(RAW_PATH, "olist_sellers_dataset.csv"))
reviews   = pd.read_csv(os.path.join(RAW_PATH, "olist_order_reviews_dataset.csv"))

print("✅ All files loaded successfully")
print(f"   Orders:    {len(orders):,} rows")
print(f"   Payments:  {len(payments):,} rows")
print(f"   Items:     {len(items):,} rows")
print(f"   Customers: {len(customers):,} rows")
print(f"   Products:  {len(products):,} rows")
print(f"   Sellers:   {len(sellers):,} rows")
print(f"   Reviews:   {len(reviews):,} rows")

# ── CLEAN: FACT_ORDERS ───────────────────────────────────────────────────────
date_cols = ["order_purchase_timestamp","order_approved_at",
             "order_delivered_carrier_date","order_delivered_customer_date",
             "order_estimated_delivery_date"]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

orders["purchase_year"]    = orders["order_purchase_timestamp"].dt.year
orders["purchase_month"]   = orders["order_purchase_timestamp"].dt.month
orders["purchase_quarter"] = orders["order_purchase_timestamp"].dt.quarter
orders["days_to_deliver"]  = (
    orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
).dt.days

fact_orders = orders[[
    "order_id","customer_id","order_status",
    "order_purchase_timestamp","purchase_year","purchase_month","purchase_quarter",
    "days_to_deliver"
]].drop_duplicates()

# ── CLEAN: FACT_PAYMENTS ─────────────────────────────────────────────────────
payments["is_installment"] = (payments["payment_installments"] > 1).astype(int)
fact_payments = payments[[
    "order_id","payment_type","payment_installments",
    "payment_value","is_installment"
]].drop_duplicates()

# ── CLEAN: FACT_ITEMS ────────────────────────────────────────────────────────
fact_items = items[["order_id","product_id","seller_id","price","freight_value"]].copy()
fact_items["total_item_value"] = fact_items["price"] + fact_items["freight_value"]

# ── CLEAN: DIM_CUSTOMERS ─────────────────────────────────────────────────────
dim_customers = customers[[
    "customer_id","customer_unique_id","customer_city","customer_state"
]].drop_duplicates()

# ── CLEAN: DIM_PRODUCTS ──────────────────────────────────────────────────────
products["product_category_name"] = products["product_category_name"].fillna("unknown")
dim_products = products[[
    "product_id","product_category_name","product_weight_g","product_length_cm"
]].drop_duplicates()

# ── CLEAN: DIM_SELLERS ───────────────────────────────────────────────────────
dim_sellers = sellers[["seller_id","seller_city","seller_state"]].drop_duplicates()

# ── CLEAN: DIM_REVIEWS ───────────────────────────────────────────────────────
dim_reviews = reviews[[
    "order_id","review_score","review_creation_date"
]].drop_duplicates(subset="order_id")

# ── EXPORT CLEAN CSVs ────────────────────────────────────────────────────────
fact_orders.to_csv(os.path.join(OUT_PATH, "fact_orders.csv"), index=False)
fact_payments.to_csv(os.path.join(OUT_PATH, "fact_payments.csv"), index=False)
fact_items.to_csv(os.path.join(OUT_PATH, "fact_items.csv"), index=False)
dim_customers.to_csv(os.path.join(OUT_PATH, "dim_customers.csv"), index=False)
dim_products.to_csv(os.path.join(OUT_PATH, "dim_products.csv"), index=False)
dim_sellers.to_csv(os.path.join(OUT_PATH, "dim_sellers.csv"), index=False)
dim_reviews.to_csv(os.path.join(OUT_PATH, "dim_reviews.csv"), index=False)

print("\n✅ Star schema exported to:", OUT_PATH)
print("   fact_orders.csv")
print("   fact_payments.csv")
print("   fact_items.csv")
print("   dim_customers.csv")
print("   dim_products.csv")
print("   dim_sellers.csv")
print("   dim_reviews.csv")
print("\n🎯 Ready to import into Power BI Desktop!")
import pandas as pd
import os

RAW_PATH = r"C:\Users\gaura\Downloads\nfs\archive (1)"
OUT_PATH  = r"C:\Users\gaura\Downloads\olist_clean"

customers = pd.read_csv(os.path.join(RAW_PATH, "olist_customers_dataset.csv"))

# Check what columns actually exist
print("Columns in raw file:", customers.columns.tolist())
print(customers.head(3))