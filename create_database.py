
import sqlite3
import pandas as pd
from pathlib import Path

# Get the project directory
BASE_DIR = Path(__file__).resolve().parent

# Define file paths
DATA_PATH = BASE_DIR / "data" / "processed" / "products_cleaned.csv"
DB_PATH = BASE_DIR / "products.db"


def create_database():
    print("Loading cleaned product data...")

    # Read cleaned CSV
    products = pd.read_csv(DATA_PATH)

    print(f"Loaded {len(products)} products.")

    # Connect to SQLite database
    connection = sqlite3.connect(DB_PATH)

    try:
        # Store products in a SQLite table
        products.to_sql(
            name="products",
            con=connection,
            if_exists="replace",
            index=False
        )

        print("Products table created successfully!")

        # Verify the number of records
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]

        print(f"Total products stored in database: {count}")

    finally:
        connection.close()

    print(f"Database saved at: {DB_PATH}")


if __name__ == "__main__":
    create_database()
