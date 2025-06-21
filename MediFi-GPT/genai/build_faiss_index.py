import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pickle
from sentence_transformers import SentenceTransformer
import faiss

from genai.pdf_reader import extract_text_from_pdf
from genai.text_splitter import split_into_chunks
import json

BOOKS = {
    "gray": "data/books/Medicina - Gray's Anatomy 16th ed.pdf",
    "guyton": "data/books/Guyton_and_Hall_Textbook_of_Medical_Physiology_14th_Ed.pdf",
    "netter": "data/books/Netter - Atlas Of Human Anatomy.pdf"
}

OUTPUT_DIR = "genai/indexes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_index_for_book(book_key, pdf_path):
    print(f"→ Indexing: {book_key}")
    raw_text = extract_text_from_pdf(pdf_path)
    chunks = split_into_chunks(raw_text)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

   
    # Save FAISS index separately
    faiss.write_index(index, f"{OUTPUT_DIR}/{book_key}_faiss.index")

    # Save chunks with metadata
    with open(f"{OUTPUT_DIR}/{book_key}_chunks.json", "w") as f:
        json.dump(chunks, f)
    print(f"✅ Saved index: {book_key}_index.pkl")

for book_key, pdf_path in BOOKS.items():
    build_index_for_book(book_key, pdf_path)
