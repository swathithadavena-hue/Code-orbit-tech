import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

catalog = {
    "Electronics":    {"Laptop": 750, "Smartphone": 500, "Headphones": 80, "Smartwatch": 150},
    "Furniture":      {"Office Chair": 120, "Desk": 220, "Bookshelf": 95},
    "Clothing":       {"Jacket": 70, "Sneakers": 65, "T-Shirt": 20},
    "Home & Kitchen": {"Blender": 45, "Coffee Maker": 60, "Air Fryer": 85},
}

dates = pd.date_range("2026-01-01", "2026-09-30")
rows = []

for i in range(1, 251):
    cat = rng.choice(list(catalog), p=[.35, .2, .25, .2])
    prod = rng.choice(list(catalog[cat]))
    rows.append([
        f"ORD-{1000 + i}",
        pd.Timestamp(dates[rng.integers(len(dates))]).date(),
        cat,
        prod,
        rng.choice(["North", "South", "East", "West"]),
        int(rng.integers(1, 6)),
        catalog[cat][prod],
    ])

df = pd.DataFrame(rows, columns=["Order ID", "Order Date", "Category",
                                 "Product", "Region", "Quantity", "Unit Price"])
df["Sales"] = df["Quantity"] * df["Unit Price"]
df.sort_values("Order Date").to_csv("sales_data.csv", index=False)
print("Created sales_data.csv with", len(df), "rows")