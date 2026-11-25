
import sqlite3
from pathlib import Path


class ProductRetriever:

    def __init__(self):

        # Locate the SQLite database
        self.db_path = Path(__file__).parent / "products.db"

        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Product database not found: {self.db_path}"
            )

        print("Product Retriever initialized successfully!")

    def search_products(
        self,
        brand=None,
        max_price=None,
        min_rating=None,
        limit=5
    ):

        # Start building SQL query
        query = """
            SELECT
                title,
                brand,
                price,
                discount,
                avg_rating,
                total_ratings,
                product_link
            FROM products
            WHERE 1=1
        """

        parameters = []

        # Filter by brand
        if brand:
            query += " AND LOWER(brand) LIKE LOWER(?)"
            parameters.append(f"%{brand}%")

        # Filter by maximum price
        if max_price is not None:
            query += " AND price <= ?"
            parameters.append(max_price)

        # Filter by minimum rating
        if min_rating is not None:
            query += " AND avg_rating >= ?"
            parameters.append(min_rating)

        # Sort and limit results using Bayesian average
        query += """
            ORDER BY
                (
                    (total_ratings * avg_rating)
                    +
                    (
                        50.0 *
                        (SELECT AVG(avg_rating) FROM products)
                    )
                ) / (total_ratings + 50.0) DESC,
                total_ratings DESC
            LIMIT ?
        """

        parameters.append(limit)

        # Execute SQL query
        with sqlite3.connect(self.db_path) as connection:

            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            cursor.execute(query, parameters)

            results = cursor.fetchall()

        return [dict(row) for row in results]



if __name__ == "__main__":

    retriever = ProductRetriever()

    # Test 1: Products under ₹1,000
    print("\n===== PRODUCTS UNDER ₹1,000 =====")

    products = retriever.search_products(
        max_price=1000,
        limit=5
    )

    for product in products:
        print(
            product["title"],
            "|", product["brand"],
            "| ₹", product["price"]
        )

    # Test 2: Products with rating >= 4.5
    print("\n===== PRODUCTS RATED 4.5 OR ABOVE =====")

    products = retriever.search_products(
        min_rating=4.5,
        limit=5
    )

    for product in products:
        print(
            product["title"],
            "|", product["brand"],
            "| Rating:", product["avg_rating"],
            "| Reviews:", product["total_ratings"]
        )

    # Test 3: Puma products under ₹3,000
    print("\n===== PUMA PRODUCTS UNDER ₹3,000 =====")

    products = retriever.search_products(
        brand="Puma",
        max_price=3000,
        limit=5
    )

    for product in products:
        print(
            product["title"],
            "|", product["brand"],
            "| ₹", product["price"]
        )
