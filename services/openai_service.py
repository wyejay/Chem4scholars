import os
from transformers import pipeline

# Load Hugging Face API Key
HF_API_KEY = os.environ.get("HF_API_KEY", "")

# Initialize Hugging Face model
generator = pipeline(
    "text-generation",
    model="google/flan-t5-large",
    token=HF_API_KEY if HF_API_KEY else None
)

SYSTEM_PROMPT = "You are a helpful chemistry tutor. Explain concepts clearly and safely."

def ai_answer(question: str) -> str:
    try:
        # Construct input with system prompt
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {question}\nAssistant:"
        
        # Generate answer
        response = generator(full_prompt, max_length=300, temperature=0.5, num_return_sequences=1)
        
        return response[0]["generated_text"].strip()
    except Exception as e:
        return f"AI Error: {str(e)}"
