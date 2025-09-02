import os
from flask import Flask, render_template, request, jsonify
import requests

# Import our element service
from services.elements_service import get_all_elements


def create_app():
    app = Flask(__name__)

    # -------------------
    # Home / index
    # -------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    # -------------------
    # Periodic Table page
    # -------------------
    @app.route("/periodic-table")
    def periodic_table():
        return render_template("periodic_table.html")

    # Serve JSON with all 118 elements (grid data)
    @app.route("/api/elements")
    def api_elements():
        return jsonify(get_all_elements())

    # -------------------
    # AI endpoint (Hugging Face as example)
    # -------------------
    @app.route("/api/ask", methods=["POST"])
    def ask():
        data = request.get_json()
        question = data.get("question", "")

        hf_api_key = os.environ.get("HF_API_KEY")
        if not hf_api_key:
            return jsonify({"error": "HF_API_KEY not set"}), 500

        # Example: using Hugging Face Inference API (small model for text generation)
        response = requests.post(
            "https://api-inference.huggingface.co/models/distilgpt2",
            headers={"Authorization": f"Bearer {hf_api_key}"},
            json={"inputs": question},
            timeout=30,
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to reach Hugging Face API"}), 500

        output = response.json()
        # Hugging Face returns a list of dicts with "generated_text"
        answer = ""
        if isinstance(output, list) and "generated_text" in output[0]:
            answer = output[0]["generated_text"]

        return jsonify({"answer": answer})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
