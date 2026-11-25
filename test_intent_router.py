
from intent_router import IntentRouter

router = IntentRouter()

questions = [
    "What is your return policy?",

    "How can I track my order?",

    "Show me Nike shoes below 5000 rupees.",

    "Find shoes with a rating above 4.5.",

    "Tell me about the latest smartphones.",

    "Recommend some Puma walking shoes."
]

for question in questions:

    intent = router.classify(question)

    print("\nCustomer Question:", question)
    print("Detected Intent:", intent)
