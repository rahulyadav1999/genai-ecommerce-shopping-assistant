
import pandas as pd

df = pd.read_csv("data/ecommerce_data_final.csv")

print("\n========== BRAND FORMATTING ==========")

print("\nOriginal brand examples:")
print(sorted(df["brand"].unique())[:30])

print("\nBrand names after capitalization:")
print(sorted(df["brand"].str.strip().str.title().unique())[:30])

print("\n========== DISCOUNT ANALYSIS ==========")

print("\nDiscount statistics:")
print(df["discount"].describe())

print("\nUnique discount values:")
print(df["discount"].nunique())

print("\nDiscount examples:")
print(df["discount"].head(10).tolist())

print("\n========== RATING VALIDATION ==========")

print("\nMinimum rating:", df["avg_rating"].min())
print("Maximum rating:", df["avg_rating"].max())

print("\n========== PRODUCT TITLE CHECK ==========")

print("Empty product titles:", df["title"].str.strip().eq("").sum())
print("Empty brand names:", df["brand"].str.strip().eq("").sum())
