
from faq_retriever import FAQRetriever

retriever = FAQRetriever()

test_questions = [
    # Relevant FAQ questions
    "Can I return a product?",
    "How do I cancel my order?",
    "My product arrived damaged. What should I do?",
    "How can I track my order?",

    # Unrelated questions
    "What is the capital of India?",
    "Who is the president of the United States?",
    "Explain machine learning.",
    "What is the weather today?"
]

print("\n========== FAQ RELEVANCE TEST ==========")

for question in test_questions:

    results = retriever.search(question, top_k=3)

    print("\nCustomer Question:", question)

    for index, faq in enumerate(results, start=1):

        print(f"\n  Match {index}: {faq['question']}")
        print(f"  Cosine Distance: {faq['distance']:.4f}")
