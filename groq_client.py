# groq_client.py
import os
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_workout(prompt: str) -> dict:
    """
    Send prompt to Groq AI using Chat Completions API and return the generated text.
    Loads GROQ_API_KEY dynamically at runtime.
    """

    # Load key dynamically here, not at import time
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("❌ GROQ_API_KEY is not set in environment variables!")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)

    if response.status_code != 200:
        print("===== GROQ API ERROR =====")
        print("Status:", response.status_code)
        print("Response:", response.text)
        print("==========================")
    response.raise_for_status()

    data = response.json()
    text = data["choices"][0]["message"]["content"]

    return {"raw_text": text, "response": data}
