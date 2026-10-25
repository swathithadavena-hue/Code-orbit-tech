"""Sales Data Analysis with Pandas"""
import pandas as pd

# ---- 1. Load the data ----
df = pd.read_csv("sales_data.csv", parse_dates=["Order Date"])

# ---- 2. Inspect and clean ----
print(df.head(), "\n")
print(df.info())
print("Missing values:\n", df.isna().sum(), "\n")

df = df.drop_duplicates(subset="Order ID").dropna()
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

# ---- 3. Key metrics ----
total_sales = df["Sales"].sum()
num_orders = df["Order ID"].nunique()
avg_order_value = total_sales / num_orders
top_products = (df.groupby("Product")["Sales"].sum()
                  .sort_values(ascending=False).head(5))

print(f"Total Sales        : ${total_sales:,.0f}")
print(f"Number of Orders   : {num_orders}")
print(f"Average Order Value: ${avg_order_value:,.2f}")
print("\nTop 5 Products by Sales:\n", top_products, "\n")

# ---- 4. Group and summarize ----
by_category = (df.groupby("Category")["Sales"]
                 .agg(["sum", "count", "mean"])
                 .sort_values("sum", ascending=False))
by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
by_month = df.groupby("Month")["Sales"].sum()

print("Sales by Category:\n", by_category.round(2), "\n")
print("Sales by Region:\n", by_region, "\n")
print("Sales by Month:\n", by_month, "\n")

# ---- 5. Short report ----
best_cat = by_category.index[0]
best_reg = by_region.index[0]
best_month = by_month.idxmax()
worst_month = by_month.idxmin()

report = f"""SALES ANALYSIS REPORT
=====================
Period: {df['Order Date'].min():%d %b %Y} to {df['Order Date'].max():%d %b %Y}

Key metrics
- Total sales: ${total_sales:,.0f} across {num_orders} orders
- Average order value: ${avg_order_value:,.2f}
- Top product: {top_products.index[0]} (${top_products.iloc[0]:,.0f})

Findings
- {best_cat} is the top category with ${by_category['sum'].iloc[0]:,.0f} ({by_category['sum'].iloc[0]/total_sales:.0%} of sales).
- {best_reg} is the strongest region (${by_region.iloc[0]:,.0f}); {by_region.index[-1]} is the weakest (${by_region.iloc[-1]:,.0f}).
- Monthly sales peaked in {best_month} (${by_month.max():,.0f}) and were lowest in {worst_month} (${by_month.min():,.0f}).
- The top 5 products generate {top_products.sum()/total_sales:.0%} of total revenue.

Recommendations
- Keep inventory and marketing focus on {best_cat}.
- Investigate why {by_region.index[-1]} lags and run a regional promotion.
- Plan stock and campaigns around the {best_month} peak.
"""

print(report)
with open("sales_report.txt", "w") as f:
    f.write(report)