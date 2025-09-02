
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
SYSTEM_PROMPT = "You are a helpful chemistry tutor. Explain concepts clearly and safely."

def ai_answer(question: str) -> str:
    if not os.environ.get("OPENAI_API_KEY"):
        return "AI is not configured. Set OPENAI_API_KEY to enable the assistant."
    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":question}],
        temperature=0.5,
    )
    try:
        return resp.output[0].content[0].text.strip()
    except Exception:
        return "I couldn't parse the AI response. Please try again."
