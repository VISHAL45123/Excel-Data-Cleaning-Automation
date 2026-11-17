
from generate_report import generate_report
from clean_data import clean_sales_data

def main():

    print("=" * 45)
    print("EXCEL DATA CLEANING & REPORTING AUTOMATION")
    print("=" * 45)

    print("\nStep 1: Cleaning Excel data...")

    cleaned_df = clean_sales_data()

    print("\nStep 2: Generating sales report...")

    generate_report(cleaned_df)

    print("\nStep 3: Process completed!")

    print("\nCheck these folders:")
    print("1. data/processed/")
    print("2. reports/")
    print("3. charts/")
    print("4. logs/")

if __name__ == "__main__":
    main()
