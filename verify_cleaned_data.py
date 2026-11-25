
import pandas as pd

faq = pd.read_csv("data/processed/faq_cleaned.csv")
products = pd.read_csv("data/processed/products_cleaned.csv")

print("\n========== CLEANED DATA VERIFICATION ==========")

print("\nFAQ Dataset:")
print("Shape:", faq.shape)
print("Missing values:", faq.isnull().sum().sum())
print("Duplicate questions:", faq["question"].duplicated().sum())

print("\nProduct Dataset:")
print("Shape:", products.shape)
print("Missing values:", products.isnull().sum().sum())
print("Duplicate product links:", products["product_link"].duplicated().sum())

print("\nBrand examples:")
print(products["brand"].unique()[:10])

print("\nProduct data types:")
print(products.dtypes)

print("\nVerification completed!")
