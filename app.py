import os
import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.5-flash-lite"

@app.route("/")
def home():
    return render_template("index.html")

def ask_gemini(message):
    models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
    last_error = None

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=message
                )
                return response.text
            except Exception as e:
                last_error = str(e)
                time.sleep(2)

    return f"Temporary Gemini error: {last_error}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message first."})

    reply = ask_gemini(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)