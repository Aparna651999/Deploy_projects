import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import faiss
from sentence_transformers import SentenceTransformer
from genai.pdf_reader import extract_text_from_pdf
from genai.text_splitter import split_into_chunks

BOOK_PATHS = {
    "gray": "data/books/Medicina - Gray's Anatomy 16th ed.pdf",
    "guyton": "data/books/Guyton_and_Hall_Textbook_of_Medical_Physiology_14th_Ed.pdf",
    "netter": "data/books/Netter - Atlas Of Human Anatomy.pdf"
}

def rebuild(book_key):
    if book_key not in BOOK_PATHS:
        print(f"❌ Unknown book key: {book_key}")
        return

    print(f"→ Rebuilding index for: {book_key}")
    pdf_path = BOOK_PATHS[book_key]
    text = extract_text_from_pdf(pdf_path)
    chunks = split_into_chunks(text)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    index_dir = "genai/indexes"
    os.makedirs(index_dir, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, f"{index_dir}/{book_key}.faiss")

    # Save chunks separately
    with open(f"{index_dir}/{book_key}_chunks.json", "w") as f:
        json.dump(chunks, f)

    print(f"✅ Saved: {book_key}.faiss + {book_key}_chunks.json")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python genai/rebuild_index.py [gray|guyton|netter]")
    else:
        rebuild(sys.argv[1])
