from flask import Flask, request, jsonify
from transformers import BartForConditionalGeneration, BartTokenizer

# Initialize Flask app
app = Flask(__name__)

# Define model path (your "Model" folder)
MODEL_PATH = r"C:\Users\sivya\OneDrive\Documents\sitnovate\SITNovate\Model"

# Load tokenizer and model
tokenizer = BartTokenizer.from_pretrained(MODEL_PATH, local_files_only=True, use_fast=False)
model = BartForConditionalGeneration.from_pretrained(MODEL_PATH, local_files_only=True)

@app.route("/")
def home():
    return "BART Summarization API is running!"

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        # Get JSON data
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Tokenize input
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)

        # Generate summary
        summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)

        # Decode and return summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
