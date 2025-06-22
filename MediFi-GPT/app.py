import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from genai.llm_engine import generate_prompt_with_rag, stream_response
from genai.quiz_gen import generate_quiz
from genai.flashcards import generate_flashcards
from genai.rag_engine import query_multi_index_rag

st.set_page_config(page_title="🧠 MediFi GPT", layout="wide")

# ---------- Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- Sidebar ----------
st.sidebar.title("🧠 MediFi-GPT")
st.sidebar.caption("AI-powered tutor trained on Gray's, Guyton, and Netter")
mode = st.sidebar.radio("Select Mode", ["Chat Tutor", "Generate Quiz", "Flashcards"])

# ---------- Main App ----------
st.title("🧠 MediFi-GPT")
st.markdown("Ask your anatomy questions or generate study materials.")

if mode == "Chat Tutor":
    st.markdown("### 💬 Chat Tutor: Ask an anatomy-related question")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").markdown(f"💬 **You:**\n\n{msg['content']}")
        elif msg["role"] == "assistant":
            st.chat_message("assistant").markdown(f"🤖 **MediFi-GPT:**\n\n{msg['content']}")

    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.chat_message("user").markdown(f"💬 **You:**\n\n{user_input}")

        # Show source chunks inline (before calling GPT)
        sources = query_multi_index_rag(user_input, k=3)
        source_text = "\n\n".join([f"**[{book}]**\n{chunk}" for book, chunk in sources])

        with st.expander("📚 Show source context"):
            st.markdown(source_text)

        # Generate GPT prompt using those chunks
        prompt = generate_prompt_with_rag(user_input)
        full_response = ""
        with st.chat_message("assistant"):
            st.markdown("🤖 **MediFi-GPT:**")
            response_container = st.empty()
            for chunk in stream_response(prompt):
                full_response += chunk
                response_container.markdown(full_response)

        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    st.markdown("<div style='text-align: center; color: #999; font-size: 0.85rem; margin-top: 2rem;'>© 2025 MediFi-GPT | Built with ❤️ for future doctors</div>", unsafe_allow_html=True)

elif mode == "Generate Quiz":
    st.markdown("### 📝 Generate Quiz")
    topic = st.text_input("Enter a topic (e.g., Anatomy of the Heart)", key="quiz_topic")
    if st.button("Generate Quiz") and topic:
        with st.spinner("Generating quiz..."):
            quiz = generate_quiz(topic)
            st.markdown(quiz)

elif mode == "Flashcards":
    st.markdown("### 📘 Flashcards")
    topic = st.text_input("Enter a topic (e.g., Cranial Nerves)", key="card_topic")
    if st.button("Generate Flashcards") and topic:
        with st.spinner("Generating flashcards..."):
            cards = generate_flashcards(topic)
            st.markdown(cards)
