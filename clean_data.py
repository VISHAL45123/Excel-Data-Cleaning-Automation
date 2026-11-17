
import pandas as pd
import numpy as np
import os
import logging

os.makedirs("data/processed", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/cleaning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def clean_sales_data():

    input_file = "data/raw/sales_data.xlsx"

    df = pd.read_excel(input_file)

    logging.info(f"Original records: {len(df)}")

    # 1. Remove duplicate Order IDs
    df = df.drop_duplicates(
        subset=["Order_ID"],
        keep="first"
    )

    # 2. Clean text columns
    text_columns = [
        "Customer_Name", "Product", "Region"
    ]

    for col in text_columns:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
        )

    # 3. Standardize capitalization
    df["Customer_Name"] = (
        df["Customer_Name"].str.title()
    )

    df["Product"] = df["Product"].str.title()
    df["Region"] = df["Region"].str.title()

    # 4. Handle missing customer names
    df["Customer_Name"] = (
        df["Customer_Name"].fillna("Unknown")
    )

    # 5. Convert numeric columns
    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )

    df["Price"] = pd.to_numeric(
        df["Price"], errors="coerce"
    )

    # 6. Remove records with missing or invalid values
    df = df.dropna(
        subset=["Order_ID", "Quantity", "Price"]
    )

    df = df[
        (df["Quantity"] > 0) &
        (df["Price"] >= 0)
    ]

    # 7. Convert date format
    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"], errors="coerce"
    )

    df = df.dropna(subset=["Order_Date"])

    # 8. Calculate total sales
    df["Total_Sales"] = (
        df["Quantity"] * df["Price"]
    )

    # 9. Export cleaned data
    output_file = (
        "data/processed/cleaned_sales_data.xlsx"
    )

    df.to_excel(output_file, index=False)

    logging.info(f"Cleaned records: {len(df)}")
    logging.info("Cleaning completed successfully")

    print("Data cleaning completed!")
    print("Final records:", len(df))
    print("Saved:", output_file)

    return df


if __name__ == "__main__":
    clean_sales_data()
