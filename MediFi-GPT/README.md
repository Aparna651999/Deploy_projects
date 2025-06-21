✅ README.md
markdown
Copy
Edit
# 🧠 MediFi-GPT

**MediFi-GPT** is an AI-powered tutor designed for medical students studying the **MBBS curriculum**. Built using OpenAI GPT models and enhanced with Retrieval-Augmented Generation (RAG), it draws context directly from authoritative medical textbooks like:

- **Gray's Anatomy** (16th Ed)
- **Guyton and Hall Textbook of Medical Physiology** (14th Ed)
- **Netter’s Atlas of Human Anatomy**

---

## 🚀 Features

- 💬 **Chat Tutor** — Ask anatomy-related questions and get context-aware answers.
- 📋 **Quiz Generator** — Instantly generate MCQs from any topic.
- 📘 **Flashcard Creator** — Create concise flashcards for rapid review.
- 📚 **Multi-book RAG** — Answers are grounded in actual medical textbooks.
- 🔐 **MBBS-only focus** — Filters out unrelated/general queries.

---

## 🖼️ Preview

![screenshot](static/logo.jpeg)

---

## 📦 Tech Stack

- [OpenAI GPT-4o](https://platform.openai.com/)
- [Streamlit](https://streamlit.io)
- [FAISS](https://github.com/facebookresearch/faiss) + [Sentence Transformers](https://www.sbert.net/)
- PyMuPDF for PDF parsing

---

## 🧑‍⚕️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/MediFi-GPT.git
cd MediFi-GPT
2. Create a virtual environment
bash
Copy
Edit
python3 -m venv gen_env
source gen_env/bin/activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set your OpenAI API key
Create a .env file:

ini
Copy
Edit
OPENAI_API_KEY=your-openai-key-here
5. Build the indexes (one-time setup)
bash
Copy
Edit
python genai/rebuild_index.py gray
python genai/rebuild_index.py guyton
python genai/rebuild_index.py netter
6. Launch the app
bash
Copy
Edit
streamlit run app/app.py
🌐 How to Deploy (Streamlit Cloud)
Push this repo to GitHub

Go to streamlit.io/cloud → Log in → New App

Select your GitHub repo, set app/app.py as the entry point

Click Deploy ✅

📬 Feedback
This is an early MVP. We're looking for feedback from:

MBBS students

Educators and clinicians

Anatomy or physiology learners

👉 Submit your suggestions here

🛡 Disclaimer
MediFi-GPT is for educational purposes only. It is not a substitute for clinical judgment, medical advice, or peer-reviewed content.

❤️ Built by
Aparna Badavane
AI/ML Engineer | Building GenAI tools for medical education

