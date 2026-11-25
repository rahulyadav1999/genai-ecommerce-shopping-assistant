
import sqlite3
from pathlib import Path

# Locate the database
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "products.db"


def test_queries():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        # Query 1: Find Nike products
        print("\n========== NIKE PRODUCTS ==========")

        cursor.execute("""
            SELECT title, brand, price, avg_rating
            FROM products
            WHERE LOWER(brand) = 'nike'
            LIMIT 5
        """)

        for row in cursor.fetchall():
            print(row)

        # Query 2: Products below ₹2,000
        print("\n========== PRODUCTS BELOW ₹2,000 ==========")

        cursor.execute("""
            SELECT title, brand, price
            FROM products
            WHERE price < 2000
            ORDER BY price ASC
            LIMIT 5
        """)

        for row in cursor.fetchall():
            print(row)

        # Query 3: Products with ratings above 4
        print("\n========== PRODUCTS RATED ABOVE 4 ==========")

        cursor.execute("""
            SELECT title, brand, avg_rating, total_ratings
            FROM products
            WHERE avg_rating > 4.0
            ORDER BY avg_rating DESC, total_ratings DESC
            LIMIT 5
        """)

        for row in cursor.fetchall():
            print(row)

        # Query 4: Five most expensive products
        print("\n========== FIVE MOST EXPENSIVE PRODUCTS ==========")

        cursor.execute("""
            SELECT title, brand, price
            FROM products
            ORDER BY price DESC
            LIMIT 5
        """)

        for row in cursor.fetchall():
            print(row)

    finally:
        connection.close()


if __name__ == "__main__":
    test_queries()
