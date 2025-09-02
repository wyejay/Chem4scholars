# ai_service.py
"""
AI Service for Chemistry Web App
--------------------------------
- Uses OpenAI as the primary AI assistant.
- Falls back to Hugging Face hosted model if OpenAI quota is exceeded or unavailable.
"""

import os
import requests
import openai

# --- Load API Keys from Environment ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

# Configure OpenAI
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Hugging Face model (chemistry/science-friendly one)
HF_MODEL = "seyonec/ChemBERTa-zinc-base-v1"  # chemistry-specific NLP model


def ask_ai(prompt: str) -> str:
    """
    Get AI-generated response for a chemistry-related prompt.
    - First tries OpenAI
    - Falls back to Hugging Face if OpenAI fails
    """

    # --- 1. Try OpenAI ---
    if OPENAI_API_KEY:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # use GPT-4 mini (fast & cost-effective)
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[AI Service] OpenAI failed: {e}")

    # --- 2. Fallback: Hugging Face ---
    if HF_API_KEY:
        try:
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {"inputs": prompt}
            url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()

            data = resp.json()
            if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            else:
                return "⚠️ Hugging Face AI could not generate a proper answer."

        except Exception as hf_error:
            print(f"[AI Service] Hugging Face failed: {hf_error}")
            return "❌ AI service is temporarily unavailable. Please try again later."

    # --- 3. If no API keys set ---
    return "⚠️ No AI service available. Please configure OPENAI_API_KEY or HF_API_KEY."
