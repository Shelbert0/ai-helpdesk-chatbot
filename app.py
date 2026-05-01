from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a Level 1 IT support assistant for a fictional company.

Provide clear, simple troubleshooting instructions.
Format answers using short numbered steps.
Do not use markdown symbols like **bold**.
Keep answers friendly, professional, and concise.

You help with:
- Password resets
- Slow internet
- Clearing browser cache and cookies
- Email setup on a phone or laptop
- Printer troubleshooting
"""

@app.route("/")
def home():
    return send_from_directory("static", "chatbot.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)