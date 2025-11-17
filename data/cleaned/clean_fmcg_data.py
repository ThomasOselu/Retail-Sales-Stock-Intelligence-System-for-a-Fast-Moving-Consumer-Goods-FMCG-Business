"""
FMCG Data Cleaning Script
-------------------------
Cleans all generated CSV datasets:
1. daily_sales.csv
2. stock_levels.csv
3. grv_supplier_invoices.csv
4. recipes_and_raw_materials.csv
5. menu_pricing.csv
6. store_cash_spotchecks.csv
"""

import os
import pandas as pd
import numpy as np


BASE_PATH = os.path.dirname(os.path.dirname(__file__))  # goes up one folder
RAW_PATH = os.path.join(BASE_PATH, "raw")
CLEAN_PATH = os.path.join(BASE_PATH, "cleaned")

os.makedirs(CLEAN_PATH, exist_ok=True)

def save_clean(df, name):
    """Helper to save cleaned dataframe"""
    path = os.path.join(CLEAN_PATH, name)
    df.to_csv(path, index=False)
    print(f"✅ Cleaned {name} saved to {path}")

# ------------------------
# 1. DAILY SALES
# ------------------------
sales = pd.read_csv(os.path.join(RAW_PATH, "daily_sales.csv"))
print("🧹 Cleaning: daily_sales.csv")

# Remove duplicates
sales = sales.drop_duplicates()

# Ensure correct dtypes
sales["date"] = pd.to_datetime(sales["date"], errors="coerce")
sales["quantity_sold"] = pd.to_numeric(sales["quantity_sold"], errors="coerce").fillna(0).astype(int)
sales["unit_price"] = pd.to_numeric(sales["unit_price"], errors="coerce")
sales["sales_amount"] = pd.to_numeric(sales["sales_amount"], errors="coerce")

# Fix negatives or impossible values
sales.loc[sales["quantity_sold"] < 0, "quantity_sold"] = 0
sales.loc[sales["unit_price"] < 0, "unit_price"] = sales["unit_price"].median()

save_clean(sales, "daily_sales_cleaned.csv")

# ------------------------
# 2. STOCK LEVELS
# ------------------------
stock = pd.read_csv(os.path.join(RAW_PATH, "stock_levels.csv"))
print("🧹 Cleaning: stock_levels.csv")

stock = stock.drop_duplicates()
stock["date"] = pd.to_datetime(stock["date"], errors="coerce")

for col in ["opening_stock", "deliveries", "sales", "closing_stock"]:
    stock[col] = pd.to_numeric(stock[col], errors="coerce").fillna(0).astype(int)
    stock.loc[stock[col] < 0, col] = 0

# Logical consistency check
stock["closing_stock"] = np.where(
    stock["closing_stock"] < 0,
    0,
    stock["closing_stock"]
)

save_clean(stock, "stock_levels_cleaned.csv")

# ------------------------
# 3. GRV & SUPPLIER INVOICES
# ------------------------
grv = pd.read_csv(os.path.join(RAW_PATH, "grv_supplier_invoices.csv"))
print("🧹 Cleaning: grv_supplier_invoices.csv")

grv = grv.drop_duplicates()
grv["grv_quantity"] = pd.to_numeric(grv["grv_quantity"], errors="coerce").fillna(0).astype(int)
grv["invoice_quantity"] = pd.to_numeric(grv["invoice_quantity"], errors="coerce").fillna(0).astype(int)
grv["difference"] = grv["invoice_quantity"] - grv["grv_quantity"]

save_clean(grv, "grv_supplier_invoices_cleaned.csv")

# ------------------------
# 4. RECIPES & RAW MATERIALS
# ------------------------
recipes = pd.read_csv(os.path.join(RAW_PATH, "recipes_and_raw_materials.csv"))
print("🧹 Cleaning: recipes_and_raw_materials.csv")

recipes = recipes.drop_duplicates()
recipes["quantity_per_unit"] = pd.to_numeric(recipes["quantity_per_unit"], errors="coerce").fillna(0)
recipes["cost_per_unit"] = pd.to_numeric(recipes["cost_per_unit"], errors="coerce").fillna(0)

save_clean(recipes, "recipes_and_raw_materials_cleaned.csv")

# ------------------------
# 5. MENU PRICING
# ------------------------
menu = pd.read_csv(os.path.join(RAW_PATH, "menu_pricing.csv"))
print("🧹 Cleaning: menu_pricing.csv")

menu = menu.drop_duplicates()
menu["selling_price"] = pd.to_numeric(menu["selling_price"], errors="coerce").fillna(menu["selling_price"].median())
menu.loc[menu["selling_price"] < 0, "selling_price"] = menu["selling_price"].median()

save_clean(menu, "menu_pricing_cleaned.csv")

# ------------------------
# 6. STORE CASH SPOTCHECKS
# ------------------------
spot = pd.read_csv(os.path.join(RAW_PATH, "store_cash_spotchecks.csv"))
print("🧹 Cleaning: store_cash_spotchecks.csv")

spot = spot.drop_duplicates()
spot["date"] = pd.to_datetime(spot["date"], errors="coerce")

for col in ["expected_cash", "actual_cash", "variance"]:
    spot[col] = pd.to_numeric(spot[col], errors="coerce").fillna(0)
spot["variance"] = spot["actual_cash"] - spot["expected_cash"]

save_clean(spot, "store_cash_spotchecks_cleaned.csv")

# ------------------------
# SUMMARY
# ------------------------
print("\n🎉 All datasets cleaned successfully!")
print(f"📁 Cleaned data stored in: {CLEAN_PATH}")
