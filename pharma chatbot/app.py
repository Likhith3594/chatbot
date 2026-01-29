from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment")

# ✅ FIXED __name__
app = Flask(__name__)
client = Groq(api_key=API_KEY)

# 💊 PHARMA CHATBOT SYSTEM PROMPT
SYSTEM_PROMPT = """
You are a Pharma / Medical Education Chatbot.

Your role:
- Explain pharmaceutical and medical concepts clearly.
- Help students, pharmacy learners, and professionals.
- Answer questions on:
  - Pharmacology
  - Drug mechanisms of action
  - Dosage forms
  - Side effects
  - Drug interactions (theoretical)
  - Pharmaceutical chemistry
  - Pharmaceutics
  - Clinical pharmacy basics
  - Pharma career guidance

Safety Rules:
- Do NOT give medical diagnosis.
- Do NOT prescribe medicines.
- Always suggest consulting a doctor for treatment decisions.

Guidelines:
- Use simple, student-friendly language.
- Be accurate and factual.
- If a question is unclear, ask one short clarification.
- Avoid hallucinations.

Tone:
- Professional, supportive, teacher-like.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please ask a pharmacy or medical-related question."})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=350,
            temperature=0.3
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Something went wrong. Please try again."}), 500


# ✅ FIXED __main__
if __name__ == "__main__":
    app.run(debug=True)
