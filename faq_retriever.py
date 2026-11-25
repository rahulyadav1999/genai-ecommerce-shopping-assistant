
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


class FAQRetriever:

    def __init__(self):

        print("Initializing FAQ Retriever...")

        # Project directory
        BASE_DIR = Path(__file__).resolve().parent

        # ChromaDB directory
        CHROMA_PATH = BASE_DIR / "chroma_db"

        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Connect to persistent ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        # Load existing FAQ collection
        self.collection = self.client.get_collection(
            name="flipkart_faq"
        )

        print("FAQ Retriever initialized successfully!")

    def search(self, question, top_k=3, threshold=0.50):

        # Convert customer question into embedding
        query_embedding = self.model.encode(
            [question]
        ).tolist()

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(top_k, self.collection.count())
        )

        # Prepare search results
        retrieved_faqs = []

        for i in range(len(results["documents"][0])):

            faq = {
                "question": results["documents"][0][i],
                "answer": results["metadatas"][0][i]["answer"],
                "distance": results["distances"][0][i]
            }

            retrieved_faqs.append(faq)

        # Return empty list if no FAQs were found
        if not retrieved_faqs:
            return []

        # Check relevance of the best match
        if retrieved_faqs[0]["distance"] > threshold:
            return []

        return retrieved_faqs
