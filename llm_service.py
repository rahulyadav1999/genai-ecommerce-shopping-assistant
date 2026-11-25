
import os
from dotenv import load_dotenv
from groq import Groq


class LLMService:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file.")

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-120b"

        print("LLM Service initialized successfully!")

    def generate_response(self, question, context):

        system_prompt = """
        You are a helpful e-commerce customer support assistant.

        Answer customer questions using ONLY the information
        provided in the context.

        Follow these rules:
        1. Do not invent company policies or product information.
        2. Do not make assumptions about refunds, replacements,
           delivery dates, or other services.
        3. If the context does not contain the answer, politely
           say that you do not have enough information.
        4. Keep your answers clear, polite, and concise.
        5. Do not mention internal technical details.
        """

        user_prompt = f"""
        Context:
        {context}

        Customer Question:
        {question}

        Provide a helpful answer based only on the context.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_completion_tokens=500,
            temperature=0.2
        )

        return response.choices[0].message.content
