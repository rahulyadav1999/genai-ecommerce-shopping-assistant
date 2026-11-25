
from product_retriever import ProductRetriever


retriever = ProductRetriever()

print("\n========== TEST 1: PRODUCTS ABOVE 4.5 RATING ==========")

products = retriever.search_products(
    min_rating=4.5,
    limit=10
)

for index, product in enumerate(products, start=1):
    print(f"\n{index}. {product['title']}")
    print(f"   Brand: {product['brand']}")
    print(f"   Price: ₹{product['price']}")
    print(f"   Rating: {product['avg_rating']}")
    print(f"   Total Reviews: {product['total_ratings']}")


print("\n========== TEST 2: PUMA PRODUCTS UNDER ₹3000 ==========")

products = retriever.search_products(
    brand="Puma",
    max_price=3000,
    limit=5
)

for index, product in enumerate(products, start=1):
    print(f"\n{index}. {product['title']}")
    print(f"   Brand: {product['brand']}")
    print(f"   Price: ₹{product['price']}")
    print(f"   Rating: {product['avg_rating']}")
    print(f"   Total Reviews: {product['total_ratings']}")
