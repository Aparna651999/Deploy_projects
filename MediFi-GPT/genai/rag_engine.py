import os
import json
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_all_indexes():
    """Load FAISS indexes and their corresponding chunks for all 3 books."""
    base_path = "genai/indexes"
    books = ["gray", "guyton", "netter"]
    indexes = {}

    for book in books:
        faiss_path = os.path.join(base_path, f"{book}.faiss")
        chunks_path = os.path.join(base_path, f"{book}_chunks.json")

        if not os.path.exists(faiss_path) or not os.path.exists(chunks_path):
            print(f"⚠️ Missing files for {book}, skipping...")
            continue

        index = faiss.read_index(faiss_path)

        with open(chunks_path, "r") as f:
            chunks = json.load(f)

        indexes[book] = {
            "index": index,
            "chunks": chunks
        }

    return indexes

def query_multi_index_rag(query: str, k: int = 4):
    """Search across all books and return the top-k results from each."""
    indexes = load_all_indexes()
    query_vec = model.encode([query])
    results = []

    for book, data in indexes.items():
        D, I = data["index"].search(query_vec, k)
        for i in I[0]:
            if i < len(data["chunks"]):
                results.append((book.upper(), data["chunks"][i]))

    return results
