# genai/quiz_gen.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from genai.llm_engine import generate_response

def generate_quiz(topic: str) -> str:
    prompt =  prompt = f"""
You are MediFi-GPT, a medical quiz generator based on Gray's Anatomy.

Create 5 multiple-choice questions on the topic: "{topic}".

Guidelines:
- Each question should be medically accurate and fact-based.
- Provide 4 options (A–D) per question.
- Mark the correct answer clearly using the format: **Answer: B**
- Do NOT include explanations unless asked.
- Format strictly as:

Q1. What structure passes through the foramen magnum?
A. Optic nerve  
B. Medulla oblongata  
C. Vagus nerve  
D. Internal carotid artery  
**Answer: B**

Now begin.
"""
    return generate_response(prompt)
