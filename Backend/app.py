from flask import Flask, request, jsonify, Response, stream_with_context
import torch
from transformers import LongT5ForConditionalGeneration, AutoTokenizer
import PyPDF2
import docx
from flask_cors import CORS
import time

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)

# ✅ Set Paths
pt_model_path = r"E:\Backend\Models\converted_model_correct.pt"  # Update your path

# ✅ Load Pretrained Model
model = LongT5ForConditionalGeneration.from_pretrained("google/long-t5-tglobal-base")
checkpoint = torch.load(pt_model_path, map_location="cpu")  # Load .pt file
model.load_state_dict(checkpoint, strict=False)  # Allow missing keys if necessary
model.eval()  # Set model to evaluation mode

# ✅ Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained("google/long-t5-tglobal-base")

# ✅ Set Device (Use GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 🔹 Extract text from file (PDF or DOCX)
def extract_text(file):
    text = ""
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file)
        text = " ".join([para.text for para in doc.paragraphs])
    return text

# 🔹 Format summary into 2-3 paragraphs
def format_summary(summary):
    words = summary.split()  # Split into words
    paragraph_size = max(50, len(words) // 3)  # Ensure at least 50 words per paragraph

    paragraphs = []
    for i in range(0, len(words), paragraph_size):
        paragraphs.append(" ".join(words[i : i + paragraph_size]))  # Group words into paragraphs

    return "\n\n".join(paragraphs)  # Ensure paragraphs are separated by double newlines

# 🔹 Streaming Response Generator
def generate_summary_stream(text):
    if not text:
        yield "No extractable text found.\n"
        return

    # ✅ Tokenize Input
    yield "Tokenizing input text...\n"
    inputs = tokenizer(text, return_tensors="pt", max_length=2048, truncation=True).to(device)
    time.sleep(1)  # Simulate processing delay

    # ✅ Generate Summary
    yield "Generating summary...\n"
    with torch.no_grad():
        summary_ids = model.generate(
            **inputs, max_length=250, min_length=100, length_penalty=2.0, num_beams=4
        )

    # ✅ Decode Summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # ✅ Format Summary into Paragraphs with HTML Breaks for Browser Rendering
    formatted_summary = format_summary(summary).replace("\n\n", "<br><br>")

    # ✅ Stream Final Output
    yield f"\n\n{formatted_summary}\n"

# 🔹 Define Summarization Endpoint
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        # ✅ Check if file is uploaded
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        # ✅ Extract text from the uploaded file
        input_text = extract_text(file)

        if not input_text.strip():
            return jsonify({"error": "No extractable text found"}), 400

        return Response(stream_with_context(generate_summary_stream(input_text)), content_type="text/html")  # Use text/html to ensure line breaks render properly

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
