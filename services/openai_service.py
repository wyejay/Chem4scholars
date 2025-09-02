import os
from huggingface_hub import InferenceClient

HF_API_KEY = os.getenv("HF_API_KEY")

# Initialize Hugging Face client with token
hf_client = InferenceClient(token=HF_API_KEY)

def ai_answer(prompt: str) -> str:
    """
    Generate an AI response using Hugging Face Inference API.
    """
    try:
        response = hf_client.text_generation(
            model="openai-community/gpt2",  # ✅ valid HF model repo
            prompt=prompt,
            max_new_tokens=200,
        )
        return response
    except Exception as e:
        return f"Error generating AI response: {str(e)}"
