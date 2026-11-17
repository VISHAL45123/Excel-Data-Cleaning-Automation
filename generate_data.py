
import pandas as pd
import numpy as np
import os

os.makedirs("data/raw", exist_ok=True)

np.random.seed(42)

n = 1000

data = {
    "Order_ID": [f"ORD{i:04d}" for i in range(1, n + 1)],
    "Customer_Name": np.random.choice(
        ["Rahul", "Priya", "Amit", "Neha", "John", None],
        n
    ),
    "Product": np.random.choice(
        ["Laptop", "Mobile", "Tablet", "Headphones"],
        n
    ),
    "Region": np.random.choice(
        ["North", "South", "East", "West"],
        n
    ),
    "Quantity": np.random.randint(1, 10, n),
    "Price": np.random.randint(500, 50000, n),
    "Order_Date": pd.date_range(
        "2025-01-01", periods=n, freq="D"
    ).astype(str)
}

df = pd.DataFrame(data)

# Introduce data quality problems
df.loc[5, "Customer_Name"] = None
df.loc[10, "Region"] = " north "
df.loc[15, "Product"] = " laptop "
df.loc[20, "Quantity"] = np.nan
df.loc[25, "Price"] = np.nan
df.loc[30, "Order_Date"] = "invalid_date"

# Add duplicate transactions
df = pd.concat(
    [df, df.iloc[:10]],
    ignore_index=True
)

df.to_excel(
    "data/raw/sales_data.xlsx",
    index=False
)

print("Dirty Excel dataset created successfully!")

