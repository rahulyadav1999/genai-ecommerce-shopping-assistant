
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "products.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Check Nike records
cursor.execute("""
    SELECT brand, COUNT(*), MIN(price), MAX(price)
    FROM products
    WHERE LOWER(brand) LIKE '%nike%'
    GROUP BY brand
""")

print("\nNike records:")
for row in cursor.fetchall():
    print(row)

# Check Nike products under ₹2,000
cursor.execute("""
    SELECT COUNT(*)
    FROM products
    WHERE LOWER(brand) LIKE '%nike%'
    AND price <= 2000
""")

print("\nNike products under ₹2,000:", cursor.fetchone()[0])

connection.close()
