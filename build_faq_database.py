
import chromadb
import pandas as pd

from pathlib import Path
from sentence_transformers import SentenceTransformer


# 1. Define project paths
BASE_DIR = Path(__file__).resolve().parent

FAQ_PATH = BASE_DIR / "data" / "processed" / "faq_cleaned.csv"
CHROMA_PATH = BASE_DIR / "chroma_db"


def build_faq_database():

    # 2. Load cleaned FAQ dataset
    print("Loading FAQ dataset...")

    faq_data = pd.read_csv(FAQ_PATH)

    print(f"Loaded {len(faq_data)} FAQs.")

    # 3. Load embedding model
    print("\nLoading Sentence Transformer model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 4. Generate embeddings for FAQ questions
    questions = faq_data["question"].tolist()
    answers = faq_data["answer"].tolist()

    print("\nGenerating FAQ embeddings...")

    embeddings = model.encode(questions).tolist()

    # 5. Create persistent ChromaDB client
    print("\nConnecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    # 6. Delete the old collection if it exists
    try:
        client.delete_collection(name="flipkart_faq")
        print("Existing FAQ collection deleted.")

    except Exception:
        print("No existing FAQ collection found.")

    # 7. Create a fresh collection
    collection = client.create_collection(
        name="flipkart_faq",
        metadata={"hnsw:space": "cosine"}
    )

    # 8. Store questions, answers, and embeddings
    collection.add(
        ids=[f"faq_{i}" for i in range(len(questions))],
        documents=questions,
        embeddings=embeddings,
        metadatas=[
            {"answer": answer}
            for answer in answers
        ]
    )

    print("\nFAQ database created successfully!")

    print("Total FAQs stored:", collection.count())

    print("Database location:", CHROMA_PATH)


if __name__ == "__main__":
    build_faq_database()
