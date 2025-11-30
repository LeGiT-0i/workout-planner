# groq_client.py
import os
import requests
from typing import Dict, Any

GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.ai/v1/generate")  # placeholder
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

def generate_workout(prompt: str, model: str = "groq-1") -> Dict[str, Any]:
    """
    Send prompt to Groq AI and return parsed JSON.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 800,
        # add other params if Groq supports them
    }
    resp = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # The exact structure depends on Groq; adapt as needed.
    # Example: if response text is in data["text"] or data["choices"][0]["text"]
    text = data.get("text") or (data.get("choices") and data["choices"][0].get("text"))
    return {"raw_text": text, "response": data}
