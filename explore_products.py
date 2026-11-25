
import pandas as pd

df = pd.read_csv("data/ecommerce_data_final.csv")

print("\n========== PRODUCT EXPLORATION ==========")

print("\n1. Total unique brands:")
print(df["brand"].nunique())

print("\n2. Products by brand:")
print(df["brand"].value_counts().head(10))

print("\n3. Price statistics:")
print(df["price"].describe())

print("\n4. Minimum price:")
print(df["price"].min())

print("\n5. Maximum price:")
print(df["price"].max())

print("\n6. Average price:")
print(round(df["price"].mean(), 2))

print("\n7. Top 10 highest-rated products:")
print(
    df.sort_values("avg_rating", ascending=False)[
        ["title", "brand", "price", "avg_rating", "total_ratings"]
    ].head(10).to_string(index=False)
)
