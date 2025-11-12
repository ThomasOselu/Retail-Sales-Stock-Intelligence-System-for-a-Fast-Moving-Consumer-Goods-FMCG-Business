"""
FMCG Data Generator Script
--------------------------
Generates synthetic datasets for FMCG Data Analysis:
1. Daily Sales Data
2. Stock Levels
3. Supplier GRVs vs Invoices
4. Recipes and Raw Materials
5. Menu Pricing
6. Store Cash Spot Checks
"""

import pandas as pd
import numpy as np
import random
import os

# Set reproducibility
np.random.seed(42)
random.seed(42)

# ------------------------
# BASIC CONFIG
# ------------------------
stores = ["Harare_Main", "Harare_North", "Borrowdale", "Avondale", "Chitungwiza"]
skus = ["Bread_Standard", "Bread_Premium", "Buns_6pk", "Rolls_6pk", "Doughnut", "Cake_Slice"]
ingredients = ["Flour_kg", "Yeast_g", "Sugar_kg", "Oil_L", "Packaging_unit"]
dates = pd.date_range("2025-01-01", "2025-01-31")

# Ingredient cost and recipes
ingredient_costs = {
    "Flour_kg": 1.20,
    "Yeast_g": 0.002,
    "Sugar_kg": 0.90,
    "Oil_L": 1.50,
    "Packaging_unit": 0.10,
}

recipe_bom = {
    "Bread_Standard": {"Flour_kg": 0.5, "Yeast_g": 5, "Sugar_kg": 0.02, "Oil_L": 0.01, "Packaging_unit": 1},
    "Bread_Premium": {"Flour_kg": 0.6, "Yeast_g": 7, "Sugar_kg": 0.03, "Oil_L": 0.015, "Packaging_unit": 1},
    "Buns_6pk": {"Flour_kg": 0.4, "Yeast_g": 4, "Sugar_kg": 0.05, "Oil_L": 0.01, "Packaging_unit": 1},
    "Rolls_6pk": {"Flour_kg": 0.35, "Yeast_g": 4, "Sugar_kg": 0.04, "Oil_L": 0.01, "Packaging_unit": 1},
    "Doughnut": {"Flour_kg": 0.12, "Yeast_g": 3, "Sugar_kg": 0.03, "Oil_L": 0.02, "Packaging_unit": 1},
    "Cake_Slice": {"Flour_kg": 0.1, "Yeast_g": 0, "Sugar_kg": 0.08, "Oil_L": 0.03, "Packaging_unit": 1},
}

menu_prices = {
    "Bread_Standard": 1.00,
    "Bread_Premium": 1.40,
    "Buns_6pk": 1.10,
    "Rolls_6pk": 1.00,
    "Doughnut": 0.50,
    "Cake_Slice": 0.80,
}

# Create output folder
OUT = os.getcwd()
print(f"✅ Output directory: {OUT}")

# ------------------------
# 1. DAILY SALES DATA
# ------------------------
sales = []
for date in dates:
    for store in stores:
        for sku in skus:
            base_qty = random.randint(80, 200)
            if date.weekday() >= 5:  # weekend boost
                base_qty = int(base_qty * 1.3)
            qty = np.random.poisson(base_qty)
            price = menu_prices[sku]
            sales.append({
                "date": date,
                "store": store,
                "sku": sku,
                "quantity_sold": qty,
                "unit_price": price,
                "sales_amount": round(qty * price, 2)
            })

sales_df = pd.DataFrame(sales)
sales_df.to_csv(os.path.join(OUT, "daily_sales.csv"), index=False)

# ------------------------
# 2. STOCK LEVELS
# ------------------------
stocks = []
for date in dates:
    for store in stores:
        for sku in skus:
            opening = random.randint(300, 700)
            deliveries = random.randint(50, 200)
            sold = sales_df[(sales_df["date"] == date) & (sales_df["store"] == store) & (sales_df["sku"] == sku)]["quantity_sold"].iloc[0]
            closing = max(opening + deliveries - sold, 0)
            stocks.append({
                "date": date,
                "store": store,
                "sku": sku,
                "opening_stock": opening,
                "deliveries": deliveries,
                "sales": sold,
                "closing_stock": closing
            })

stock_df = pd.DataFrame(stocks)
stock_df.to_csv(os.path.join(OUT, "stock_levels.csv"), index=False)

# ------------------------
# 3. SUPPLIER GRVs & INVOICES
# ------------------------
grv = []
for sku in skus:
    for i in range(40):
        grv_qty = random.randint(500, 900)
        invoice_qty = grv_qty + random.choice([0, 0, 5, -5, 10])
        grv.append({
            "grv_id": f"GRV-{sku[:3]}-{i}",
            "sku": sku,
            "grv_quantity": grv_qty,
            "invoice_quantity": invoice_qty,
            "difference": invoice_qty - grv_qty
        })

grv_df = pd.DataFrame(grv)
grv_df.to_csv(os.path.join(OUT, "grv_supplier_invoices.csv"), index=False)

# ------------------------
# 4. RECIPES & COSTING
# ------------------------
recipes = []
for sku, materials in recipe_bom.items():
    for ingredient, qty in materials.items():
        recipes.append({
            "sku": sku,
            "ingredient": ingredient,
            "quantity_per_unit": qty,
            "cost_per_unit": round(qty * ingredient_costs[ingredient], 4)
        })

recipes_df = pd.DataFrame(recipes)
recipes_df.to_csv(os.path.join(OUT, "recipes_and_raw_materials.csv"), index=False)

# ------------------------
# 5. MENU PRICING
# ------------------------
menu_df = pd.DataFrame([
    {"sku": sku, "selling_price": price}
    for sku, price in menu_prices.items()
])
menu_df.to_csv(os.path.join(OUT, "menu_pricing.csv"), index=False)

# ------------------------
# 6. CASH SPOT CHECKS
# ------------------------
spot = []
for date in dates:
    for store in stores:
        expected = random.randint(800, 2000)
        actual = expected + random.choice([0, 0, -20, -10, 10, 15])
        spot.append({
            "date": date,
            "store": store,
            "expected_cash": expected,
            "actual_cash": actual,
            "variance": actual - expected
        })

spot_df = pd.DataFrame(spot)
spot_df.to_csv(os.path.join(OUT, "store_cash_spotchecks.csv"), index=False)

# ------------------------
# FINISH
# ------------------------
print("✅ FMCG Data Generation Complete!")
print("📂 Files created:")
for file in [
    "daily_sales.csv",
    "stock_levels.csv",
    "grv_supplier_invoices.csv",
    "recipes_and_raw_materials.csv",
    "menu_pricing.csv",
    "store_cash_spotchecks.csv"
]:
    print("-", file)
