
import os
import json
from dotenv import load_dotenv
from groq import Groq


class IntentRouter:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file.")

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-120b"

        print("Intent Router initialized successfully!")

    def classify(self, question):

        system_prompt = """
        You are an intent classification system for an
        e-commerce customer support chatbot.

        The product catalogue contains women's shoes only.

        Classify the customer's question into exactly one
        of these categories:

        1. faq:
           Questions about return policies, refunds, damaged
           products, order tracking, cancellations, delivery,
           customer support, and other store policies.

        2. product:
           Questions about finding, searching, comparing,
           filtering, or recommending products from the
           women's shoe catalogue.

           Examples:
           - Show me Nike shoes.
           - Find shoes under 2000 rupees.
           - Which Puma shoes have the highest ratings?
           - Recommend walking shoes.

        3. out_of_scope:
           Questions unrelated to the supported FAQs or
           women's shoe catalogue.

        Rules:
        - Classify based on the customer's actual intent.
        - Do not confuse product searches with FAQ questions.
        - Return valid JSON only.
        - Do not answer the customer's question.

        Expected JSON:

        {
            "intent": "faq"
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
            max_completion_tokens=100,
            temperature=0
        )

        result = json.loads(
            response.choices[0].message.content
        )

        intent = result.get("intent")

        allowed_intents = {
            "faq",
            "product",
            "out_of_scope"
        }

        if intent not in allowed_intents:
            raise ValueError(
                f"Invalid intent returned by LLM: {intent}"
            )

        return intent
