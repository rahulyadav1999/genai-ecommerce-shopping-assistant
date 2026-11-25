
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Create an in-memory ChromaDB client
client = chromadb.Client()

# 3. Create a collection
collection = client.create_collection(
    name="faq_test"
)

# 4. Prepare sample FAQ questions
questions = [
    "What should I do if I receive a damaged product?",
    "How can I track my order?",
    "What is the return policy?",
    "How can I cancel my order?",
    "What payment methods are accepted?"
]

# 5. Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(questions).tolist()

# 6. Store questions and embeddings in ChromaDB
collection.add(
    ids=[f"faq_{i}" for i in range(len(questions))],
    documents=questions,
    embeddings=embeddings
)

print("FAQ questions stored successfully!")

# 7. Search using a customer question
customer_question = "My product arrived broken. What can I do?"

query_embedding = model.encode(
    [customer_question]
).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

# 8. Display search results
print("\n========== SEARCH RESULTS ==========")

for i, document in enumerate(results["documents"][0]):
    print(f"\nResult {i + 1}:")
    print("FAQ:", document)
    print("Distance:", results["distances"][0][i])

print("\nChromaDB test completed!")
