
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# Read API key securely
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)

print("Connecting to Groq...")

# Send a test message
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful e-commerce customer support assistant."
        },
        {
            "role": "user",
            "content": "A customer received damaged shoes. Explain the next steps politely."
        }
    ],
    max_completion_tokens=300
)

# Display response
print("\n========== GROQ RESPONSE ==========")
print(response.choices[0].message.content)
print("\nGroq connection successful!")
