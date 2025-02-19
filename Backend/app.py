from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import torch
import fitz  # PyMuPDF for PDFs
import docx
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend communication

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load AI Model Function
def load_model(model_path):
    model = torch.load(model_path, map_location=torch.device("cpu"))
    model.eval()
    return model

# Load all models
# models = {
#     "articles": load_model("models/articles_model.pth"),
#     "research_papers": load_model("models/research_papers_model.pth"),
#     "legal_contracts": load_model("models/legal_contracts_model.pth"),
# }

# Allowed file types
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

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    model_type = request.form.get("model", "articles")  # Get selected model type from frontend

    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    if model_type not in models:
        return jsonify({"error": "Invalid model type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    text = extract_text(file_path)
    if not text:
        return jsonify({"error": "Failed to extract text"}), 400

    # Process text using AI model (Example processing, update as per your model logic)
    model = models[model_type]
    input_tensor = torch.tensor([ord(c) for c in text[:1000]]).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)  # Replace with actual model processing logic

    summary = "Generated summary..."  # Replace with actual AI model output
    return jsonify({"extracted_text": text[:1000], "summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
