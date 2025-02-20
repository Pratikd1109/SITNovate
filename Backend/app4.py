from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os
import time
import fitz  # PyMuPDF for PDFs
import docx
import torch
import PyPDF2
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Upload folder configuration
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# Load the summarization model
MODEL_PATH = "LegalContracts"  # Update with your actual path
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

def allowed_file(filename):
    """Check if file type is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT file."""
    ext = file_path.rsplit(".", 1)[1].lower()

    if ext == "pdf":
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
        return text.strip()
    
    elif ext == "docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    elif ext == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    return None

def generate_summary_stream(text, max_length=200):
    """Generate a summarized text stream using the model."""
    inputs = tokenizer(text, return_tensors="pt", max_length=4096, truncation=True)
    summary_ids = model.generate(**inputs, max_length=max_length, num_beams=5)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    for word in summary.split():
        yield word + " "
        torch.cuda.empty_cache()  # Free up memory
        time.sleep(0.05)  # Simulate streaming

@app.route("/extract-text", methods=["POST"])
def extract_text_api():
    """API endpoint for extracting text from an uploaded document."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    text = extract_text(file_path)
    if not text:
        return jsonify({"error": "Failed to extract text"}), 400

    return Response(text, content_type="text/plain")

@app.route("/summarize", methods=["POST"])
def summarize():
    """API endpoint for summarizing extracted text."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    
    try:
        print("🔍 File received:", file.filename)

        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Extract text
        text = extract_text(file_path)
        if not text:
            return jsonify({"error": "Failed to extract text"}), 400

        print("📜 Extracted Text:", text[:500])  # Print first 500 chars for debugging
        
        # Debug model loading
        print("🧠 Running summarization model...")
        return Response(generate_summary_stream(text), mimetype="text/plain")

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    """API home route."""
    return "📜 Intelligent Document Summarization API is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
