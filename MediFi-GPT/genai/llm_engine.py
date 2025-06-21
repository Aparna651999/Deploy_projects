# genai/llm_engine.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from genai.rag_engine import query_multi_index_rag

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_response(prompt: str):
    """Yields streaming tokens (for Chat UI)"""
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI medical tutor."},
            {"role": "user", "content": prompt}
        ],
        stream=True,
        temperature=0.3,
        max_tokens=500,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def generate_response(prompt: str) -> str:
    """Returns full response (for Quiz/Flashcards)"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI medical tutor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content


def stream_response_with_history(chat_history: list):
    """Yields streaming tokens with full chat history for context-aware replies."""
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history,
        stream=True,
        temperature=0.3,
        max_tokens=800,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def generate_prompt_with_rag(user_query: str) -> str:
    chunks = query_multi_index_rag(user_query, k=5)

    context = "\n\n".join([f"[{book}]\n{chunk}" for book, chunk in chunks])

    prompt = f"""
You are MediFi-GPT — a focused, domain-specific AI tutor designed exclusively for medical students studying the MBBS curriculum. You are trained using authoritative medical textbooks such as Gray’s Anatomy, Guyton’s Physiology, and Netter’s Atlas.

You must only respond to questions related to the medical domain, particularly those covered during MBBS — including anatomy, physiology, pathology, microbiology, biochemistry, pharmacology, and clinical medicine.

❗ If a user asks a question unrelated to medical education (e.g., programming, sports, politics, pop culture), politely respond:
"I'm here to help with medical education topics only. Please ask something from the MBBS syllabus."

<context>
{context}
</context>

Question: {user_query}

Answer:
"""
    return prompt


