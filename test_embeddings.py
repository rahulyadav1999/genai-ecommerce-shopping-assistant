
from sentence_transformers import SentenceTransformer

# Load the embedding model
print("Loading Sentence Transformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Example sentences
sentences = [
    "My order arrived damaged.",
    "I received a broken product.",
    "How can I track my shipment?"
]

# Convert sentences into embeddings
embeddings = model.encode(sentences)

print("\nEmbedding test completed!")

print("Number of sentences:", len(sentences))
print("Embedding shape:", embeddings.shape)

print("\nFirst sentence embedding:")
print(embeddings[0][:10])
