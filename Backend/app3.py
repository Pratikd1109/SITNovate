from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os
import fitz  # PyMuPDF for PDFs
import docx
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend communication

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract text from document
def extract_text(file_path):
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

# Generator function for streaming response
def generate_summary(text):
    words = text.split()
    for word in words:
        yield word + " "
        time.sleep(0.05)  # Simulate streaming delay

# API Endpoint for Streaming Text Extraction
@app.route("/extract-text", methods=["POST"])
def extract_text_api():
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

    return Response(generate_summary(text), content_type="text/plain")  # Stream response

if __name__ == "__main__":
    app.run(debug=True)
