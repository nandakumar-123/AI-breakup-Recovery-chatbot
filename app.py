import os
from dotenv import load_dotenv
import requests
from flask import Flask, render_template, request, flash

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
print("API Key loaded:", OPENROUTER_API_KEY is not None)  # Should print True if loaded

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "openai/gpt-oss-20b:free"

# -------------------------
# Flask setup
# -------------------------
app = Flask(__name__)
app.secret_key = "breakup-recovery-secret"

# -------------------------
# Helper function to call API
# -------------------------
def ask_model(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        return "❌ Missing OpenRouter API key."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a breakup recovery assistant. Give advice in Markdown format with bullet points."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

# -------------------------
# Flask routes
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    therapist = closure = planner = honesty = None

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()

        if not user_input:
            flash("⚠ Please share your breakup story first.", "error")
            return render_template("index.html")

        # Generate outputs
        therapist = ask_model(f"Empathetic breakup advice with 2–3 bold headings and bullet points. Max 150 words. Story: {user_input}")
        closure = ask_model(f"Short closure letter to an ex. Calm, emotional tone. Max 120 words. Story: {user_input}")
        planner = ask_model(f"7-day breakup recovery plan. Bold day headings, 2 bullet points per day. Story: {user_input}")
        honesty = ask_model(f"Brutally honest breakup advice. 2–3 bold headings, 4–5 bullet points. Direct but caring. Story: {user_input}")

    return render_template("index.html", therapist=therapist, closure=closure, planner=planner, honesty=honesty)

# -------------------------
# Run Flask
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
