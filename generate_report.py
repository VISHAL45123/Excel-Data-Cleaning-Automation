
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)

def generate_report(df):

    # KPI calculations
    total_revenue = df["Total_Sales"].sum()
    total_orders = df["Order_ID"].nunique()
    total_units = df["Quantity"].sum()

    average_order_value = (
        total_revenue / total_orders
        if total_orders else 0
    )

    # Sales by region
    region_sales = (
        df.groupby("Region")["Total_Sales"]
        .sum()
        .reset_index()
    )

    # Sales by product
    product_sales = (
        df.groupby("Product")["Total_Sales"]
        .sum()
        .reset_index()
    )

    # Monthly sales
    df["Month"] = (
        df["Order_Date"].dt.to_period("M").astype(str)
    )

    monthly_sales = (
        df.groupby("Month")["Total_Sales"]
        .sum()
        .reset_index()
    )

    # Chart 1: Region sales
    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=region_sales,
        x="Region",
        y="Total_Sales"
    )

    plt.title("Sales by Region")
    plt.tight_layout()
    plt.savefig("charts/region_sales.png")
    plt.close()

    # Chart 2: Product sales
    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=product_sales,
        x="Product",
        y="Total_Sales"
    )

    plt.title("Sales by Product")
    plt.tight_layout()
    plt.savefig("charts/product_sales.png")
    plt.close()

    # Chart 3: Monthly sales
    plt.figure(figsize=(10, 5))

    sns.lineplot(
        data=monthly_sales,
        x="Month",
        y="Total_Sales",
        marker="o"
    )

    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("charts/monthly_sales.png")
    plt.close()

    # KPI sheet
    kpi = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Orders",
            "Total Units Sold",
            "Average Order Value"
        ],
        "Value": [
            total_revenue,
            total_orders,
            total_units,
            average_order_value
        ]
    })

    # Export report
    with pd.ExcelWriter(
        "reports/sales_report.xlsx",
        engine="openpyxl"
    ) as writer:

        kpi.to_excel(
            writer, sheet_name="KPI Summary",
            index=False
        )

        region_sales.to_excel(
            writer, sheet_name="Region Analysis",
            index=False
        )

        product_sales.to_excel(
            writer, sheet_name="Product Analysis",
            index=False
        )

        monthly_sales.to_excel(
            writer, sheet_name="Monthly Trends",
            index=False
        )

    print("Sales report generated successfully!")

    print("Total Revenue:", round(total_revenue, 2))
    print("Total Orders:", total_orders)
    print("Total Units:", total_units)
    print("Average Order Value:", round(
        average_order_value, 2
    ))


if __name__ == "__main__":
    from clean_data import clean_sales_data

    cleaned_df = clean_sales_data()
    generate_report(cleaned_df)
