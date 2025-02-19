from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import torch
import fitz  # PyMuPDF for PDFs
import docx
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def hello():
    return "hello"



# Load AI Models
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

# Function to check allowed file types
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from uploaded documents
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

# API Route to Summarize Documents
@app.route("/summarize", methods=["POST"])
def summarize():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    model_type = request.form.get("model_type", "articles")

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

    # Process text using AI model
    model = models[model_type]
    input_tensor = torch.tensor([ord(c) for c in text[:1000]]).unsqueeze(0)  # Example processing
    with torch.no_grad():
        output = model(input_tensor)  # Model makes prediction

    summary = "Generated summary..."  # Replace with actual model output processing
    return jsonify({"extracted_text": text[:1000], "summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
