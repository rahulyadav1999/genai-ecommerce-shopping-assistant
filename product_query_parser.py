
import os
import json
from dotenv import load_dotenv
from groq import Groq


class ProductQueryParser:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file.")

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-120b"

        print("Product Query Parser initialized successfully!")

    def parse(self, question):

        system_prompt = """
        You are a product search query parser for an
        e-commerce store that sells women's shoes.

        Extract the following filters from the customer's question:

        1. brand: Product brand, or null if not specified.
        2. max_price: Maximum price in INR, or null if not specified.
        3. min_rating: Minimum rating, or null if not specified.
        4. limit: Number of products requested.

        Rules:
        - Extract only filters clearly expressed by the customer.
        - Do not invent a brand, price, or rating.
        - If the customer says below or under ₹3000,
          max_price should be 3000.
        - If the customer says above 4.5 rating,
          min_rating should be 4.5.
        - Default limit is 5.
        - Maximum allowed limit is 20.
        - Do not generate SQL.
        - Return valid JSON only.

        Expected JSON structure:

        {
            "brand": null,
            "max_price": null,
            "min_rating": null,
            "limit": 5
        }
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=200,
            temperature=0
        )

        result = json.loads(
            response.choices[0].message.content
        )

        # Validate and normalize extracted filters
        brand = result.get("brand")

        if brand is not None:
            if not isinstance(brand, str):
                raise ValueError("Invalid brand returned by LLM.")

            brand = brand.strip() or None

        max_price = result.get("max_price")
        min_rating = result.get("min_rating")
        limit = result.get("limit", 5)

        if max_price is not None:
            if isinstance(max_price, bool) or not isinstance(max_price, (int, float)):
                raise ValueError("Invalid maximum price.")

            if max_price < 0:
                raise ValueError("Maximum price cannot be negative.")

            max_price = int(max_price)

        if min_rating is not None:
            if isinstance(min_rating, bool) or not isinstance(min_rating, (int, float)):
                raise ValueError("Invalid minimum rating.")

            if not 0 <= min_rating <= 5:
                raise ValueError("Rating must be between 0 and 5.")

            min_rating = float(min_rating)

        if isinstance(limit, bool) or not isinstance(limit, int):
            raise ValueError("Invalid product limit.")

        limit = max(1, min(limit, 20))

        return {
            "brand": brand,
            "max_price": max_price,
            "min_rating": min_rating,
            "limit": limit
        }
