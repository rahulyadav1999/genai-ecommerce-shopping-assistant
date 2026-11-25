
import pandas as pd

# Dataset file paths
faq_path = "data/faq_data.csv"
product_path = "data/ecommerce_data_final.csv"

# Load datasets
faq_df = pd.read_csv(faq_path)
product_df = pd.read_csv(product_path)

# Function to inspect datasets
def inspect_dataset(df, name):
    print(f"\n{'=' * 50}")
    print(f"DATASET: {name}")
    print(f"{'=' * 50}")

    print("\nShape (rows, columns):")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 records:")
    print(df.head())


# Inspect both datasets
inspect_dataset(faq_df, "FAQ Dataset")
inspect_dataset(product_df, "Product Dataset")
