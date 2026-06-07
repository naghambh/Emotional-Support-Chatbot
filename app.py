from flask import Flask, request, jsonify, send_from_directory
import subprocess

app = Flask(__name__)


SYSTEM_PROMPT = """
You are an empathetic university assistant chatbot.
You emotionally support students after academic results.
Be kind, motivating, and respectful.
Never judge the student.
"""

# Full path to ollama.exe
oll = r"C:\Users\DELL\AppData\Local\Programs\Ollama\ollama.exe"

@app.route("/")
def home():
    # Serve the index.html page
    return send_from_directory(".", "index.html")

import requests

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    prompt = SYSTEM_PROMPT + "\nStudent: " + user_message + "\nAssistant:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        reply = response.json().get("response", "No response")

    except Exception as e:
        print("Error:", e)
        reply = "Sorry, AI is not responding right now."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
