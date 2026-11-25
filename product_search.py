
from product_query_parser import ProductQueryParser
from product_retriever import ProductRetriever


class ProductSearchService:

    def __init__(self):

        print("Initializing Product Search Service...")

        self.parser = ProductQueryParser()
        self.retriever = ProductRetriever()

        print("Product Search Service initialized successfully!")

    def search(self, question):

        # Step 1: Understand the customer's question
        filters = self.parser.parse(question)

        print("\nExtracted Filters:", filters)

        # Step 2: Retrieve matching products from SQLite
        products = self.retriever.search_products(**filters)

        return products


if __name__ == "__main__":

    product_search = ProductSearchService()

    question = "Show me Puma shoes below 3000 rupees"

    print("\nCustomer Question:", question)

    products = product_search.search(question)

    print("\n========== PRODUCT SEARCH RESULTS ==========")

    if not products:
        print("Sorry, no matching products were found.")

    else:
        for index, product in enumerate(products, start=1):

            print(f"\nProduct {index}")
            print("Name:", product["title"])
            print("Brand:", product["brand"])
            print("Price: ₹", product["price"])
            print("Rating:", product["avg_rating"])
            print("Reviews:", product["total_ratings"])
            print("Link:", product["product_link"])
