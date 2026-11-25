
from llm_service import LLMService

llm = LLMService()

question = "What is your return policy?"

context = """
You can return products within 30 days of delivery.
"""

answer = llm.generate_response(question, context)

print("\n========== AI GENERATED ANSWER ==========")
print(answer)
