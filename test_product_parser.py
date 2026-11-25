
from product_query_parser import ProductQueryParser

parser = ProductQueryParser()

questions = [
    "Show me Puma shoes below 3000 rupees",

    "Find Nike shoes with a rating above 4.5",

    "Show me the top 10 shoes under 2000 rupees"
]

for question in questions:

    print("\nCustomer Question:", question)

    filters = parser.parse(question)

    print("Extracted Filters:", filters)
