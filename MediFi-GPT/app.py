# app.py

import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import streamlit as st
from genai.llm_engine import generate_prompt_with_rag, stream_response
from genai.quiz_gen import generate_quiz
from genai.flashcards import generate_flashcards
from genai.rag_engine import query_multi_index_rag

# ------------------ Page Setup ------------------
st.set_page_config(page_title="🧠 MediFi-GPT", layout="wide")

st.markdown("<h1 style='text-align:center;'>🧠 MediFi-GPT</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color: gray;'>AI-Powered Tutor for MBBS Students</h3>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ Session Init ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

tab1, tab2, tab3 = st.tabs(["💬 Chat Tutor", "📝 Quiz Generator", "📘 Flashcards"])

# ------------------ CHAT TUTOR ------------------
with tab1:
    st.subheader("💬 Chat with MediFi-GPT")

    user_input = st.chat_input("Ask a medical question (e.g., What is cardiac output?)")

    if user_input:
        # Save user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Show user message
        st.chat_message("user").markdown(user_input)

        # RAG: Retrieve sources
        chunks = query_multi_index_rag(user_input, k=3)
        context_text = "\n\n".join([f"**[{book}]**\n{chunk}" for book, chunk in chunks])

        # Generate full prompt
        prompt = generate_prompt_with_rag(user_input)

        # Stream bot reply
        full_response = ""
        with st.chat_message("assistant"):
            with st.expander("📚 View source content", expanded=False):
                st.markdown(context_text)

            response_container = st.empty()
            for chunk in stream_response(prompt):
                full_response += chunk
                response_container.markdown(full_response)

        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    # Show previous messages (except current session)
    for msg in st.session_state.chat_history[:-2]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ------------------ QUIZ GENERATOR ------------------
with tab2:
    st.subheader("📝 Generate a Quiz from Topic")

    quiz_topic = st.text_input("Enter quiz topic", key="quiz_topic", placeholder="e.g., Brainstem anatomy")
    if st.button("Generate Quiz"):
        if not quiz_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating quiz..."):
                quiz = generate_quiz(quiz_topic)
                st.markdown(quiz)

# ------------------ FLASHCARDS ------------------
with tab3:
    st.subheader("📘 Flashcard Generator")

    flashcard_topic = st.text_input("Enter flashcard topic", key="card_topic", placeholder="e.g., Pulmonary Ventilation")
    if st.button("Generate Flashcards"):
        if not flashcard_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating flashcards..."):
                output = generate_flashcards(flashcard_topic)

                # Extract Q/A pairs using regex
                pattern = r"Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|\Z)"
                matches = re.findall(pattern, output, re.DOTALL)

                if matches:
                    for i, (q, a) in enumerate(matches, 1):
                        st.markdown(f"**Q{i}:** {q.strip()}")
                        st.markdown(f"*A{i}:* {a.strip()}")
                        st.markdown("---")
                else:
                    # fallback to raw display
                    st.markdown(output)

# ------------------ Footer ------------------
st.markdown(
    "<div style='text-align:center; color:gray; font-size:0.85rem; margin-top:2rem;'>"
    "© 2025 MediFi-GPT — Built with ❤️ for medical learners"
    "</div>",
    unsafe_allow_html=True
)
