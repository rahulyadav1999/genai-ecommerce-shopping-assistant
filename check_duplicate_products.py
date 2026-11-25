
import sqlite3

connection = sqlite3.connect("products.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT
        title,
        brand,
        COUNT(*) AS occurrences
    FROM products
    GROUP BY title, brand
    HAVING COUNT(*) > 1
    ORDER BY occurrences DESC
    LIMIT 10
""")

duplicates = cursor.fetchall()

print("\n========== DUPLICATE PRODUCT TITLES ==========")

for product in duplicates:
    print(
        f"Title: {product[0]}\n"
        f"Brand: {product[1]}\n"
        f"Occurrences: {product[2]}\n"
    )

connection.close()
