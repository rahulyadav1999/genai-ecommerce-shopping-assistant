
from faq_retriever import FAQRetriever
from llm_service import LLMService
from product_search import ProductSearchService
from intent_router import IntentRouter


class FlipkartChatbot:

    def __init__(self):

        print("Initializing Flipkart Chatbot...")

        self.faq_retriever = FAQRetriever()
        self.llm = LLMService()
        self.product_search = ProductSearchService()
        self.router = IntentRouter()

        print("Flipkart Chatbot initialized successfully!")

    def chat(self, question):

        # Step 1: Identify customer intent
        intent = self.router.classify(question)

        print(f"\nDetected Intent: {intent}")

        
        # Step 2: Handle FAQ questions
        if intent == "faq":

            retrieved_faqs = self.faq_retriever.search(
                question,
                top_k=3
            )

            # Check whether relevant FAQs were found
            if not retrieved_faqs:

                return (
                    "I'm sorry, I couldn't find relevant information "
                    "in our FAQ database. I can help you with store "
                    "policies, returns, cancellations, refunds, "
                    "shipping, and other supported topics."
                    "What is the capital of India?",
                    "Can I get my money back?",
                    "My shoes arrived broken."
                )

            # Prepare FAQ context
            context = "\n\n".join(
                [
                    f"FAQ Question: {faq['question']}\n"
                    f"FAQ Answer: {faq['answer']}"
                    for faq in retrieved_faqs
                ]
            )

            # Generate response using the LLM
            answer = self.llm.generate_response(
                question=question,
                context=context
            )

            return answer


        
        # Step 3: Handle product questions
        elif intent == "product":

            products = self.product_search.search(question)

            if not products:
                return []

            return products


        # Step 4: Handle unsupported questions
        else:

            return (
                "I'm sorry, I can currently help with questions "
                "about our store policies and our women's shoe "
                "catalogue. Please ask me something related to "
                "these topics."
            )


if __name__ == "__main__":

    chatbot = FlipkartChatbot()

    test_questions = [
        # FAQ variations
        "Do you accept returns?",

        # Product searches
        "Show me Nike shoes under 5000",
        "Find shoes with a rating above 4.5",

        # No matching products
        "Show me Adidas shoes below 1000",

        # Unsupported product category
        "What is the price of iPhone 17?",

        # Completely unrelated question
        "Who won the cricket match yesterday?"
    ]

    for question in test_questions:

        print("\n" + "=" * 60)
        print("CUSTOMER:", question)

        response = chatbot.chat(question)

        print("\nCHATBOT:", response)
