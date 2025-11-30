# groq_client.py
import os
import requests

# Correct Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_workout(prompt: str) -> dict:
    """
    Send prompt to Groq AI using Chat Completions API and return the generated text.
    """

    if not GROQ_API_KEY:
        raise ValueError("❌ GROQ_API_KEY is not set in environment variables!")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama3-70b-8192",   # valid Groq model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    # Make request
    response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)

    # If bad request, print debug info
    if response.status_code != 200:
        print("\n===== GROQ API ERROR =====")
        print("Status:", response.status_code)
        print("Reason:", response.reason)
        print("Response body:", response.text)
        print("===========================\n")

    response.raise_for_status()

    data = response.json()

    # Extract message content correctly
    text = data["choices"][0]["message"]["content"]

    return {"raw_text": text, "response": data}
