import os
from huggingface_hub import InferenceClient

# Load Hugging Face API key from environment variables
HF_API_KEY = os.getenv("HF_API_KEY")

# Initialize client
hf_client = InferenceClient(api_key=HF_API_KEY)


def ai_answer(prompt: str) -> str:
    """
    Generate a text response from Hugging Face model.
    """

    try:
        # Call Hugging Face text generation API
        response = hf_client.text_generation(
            model="gpt2",            # you can replace this with another HF model
            prompt=prompt,
            max_new_tokens=200,
            temperature=0.7
        )

        return response

    except Exception as e:
        return f"Error while generating AI response: {e}"
