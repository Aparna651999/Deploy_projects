import fitz  # PyMuPDF
import os


def extract_text_from_pdf(pdf_path, max_pages=50):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc[:max_pages]:
        text += page.get_text()
    return text

def get_all_texts():
    folder = "/home/user/Github/projects/GenAI/MediFi-GPT/data"
    texts = {}
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            path = os.path.join(folder, filename)
            texts[filename] = extract_text_from_pdf(path)
    return texts
