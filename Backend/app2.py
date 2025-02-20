# import torch
# from flask import Flask, request, jsonify, Response, stream_with_context
# from transformers import PegasusForConditionalGeneration, AutoTokenizer
# import time
# from flask_cors import CORS



# # ✅ Initialize Flask App
# app = Flask(__name__)
# CORS(app)
# # ✅ Load Model and Tokenizer
# pt_model_path = r"E:\Backend\Models\pegasus_xsum_model.pt"

# model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
# checkpoint = torch.load(pt_model_path, map_location="cpu")
# model.load_state_dict(checkpoint, strict=False)

# # ✅ Move Model to GPU (if available)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)
# model.eval()

# tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")

# # ✅ Text Extraction Function
# def extract_text_from_request(req):
#     """
#     Extract text from a JSON request payload.
#     """
#     data = req.get_json()
#     return data.get("text", "")

# def extract_text_from_request(req):
#     """
#     Extract text from a JSON request payload.
#     Handles missing or incorrect content types.
#     """
#     try:
#         data = req.get_json(force=True)  # ✅ Force JSON parsing (handles incorrect Content-Type)
#         return data.get("text", "")
#     except Exception:
#         return ""
# # ✅ Streaming Response Generator
# def generate_summary_stream(text):
#     """
#     Generates summary in a streaming fashion for real-time response.
#     """
#     if not text:
#         yield "No input text provided.\n"
#         return

#     # ✅ Encode Input
#     yield "Encoding input text...\n"
#     inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
#     inputs = {k: v.to(device) for k, v in inputs.items()}
#     time.sleep(1)  # Simulate processing delay

#     # ✅ Generate Summary
#     yield "Generating summary...\n"
#     with torch.no_grad():
#         summary_ids = model.generate(**inputs, max_length=60, num_beams=5, early_stopping=True)
    
#     # ✅ Decode Summary
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
#     # ✅ Stream Final Output
#     yield f"\n🔹 **Original Text:**\n{text}\n\n"
#     yield f"🔹 **Generated Summary:**\n{summary}\n"

# @app.route('/summarize', methods=['POST'])
# def summarize():
#     try:
#         text = extract_text_from_request(request)
#         return Response(stream_with_context(generate_summary_stream(text)), content_type='text/plain')

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # ✅ Run Flask App
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, threaded=True)

import torch
from flask import Flask, request, Response, stream_with_context
from transformers import PegasusForConditionalGeneration, AutoTokenizer
import PyPDF2
import docx
import time
from flask_cors import CORS

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)

# ✅ Load Model and Tokenizer
pt_model_path = r"E:\Backend\Models\pegasus_xsum_model.pt"

model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
checkpoint = torch.load(pt_model_path, map_location="cpu")
model.load_state_dict(checkpoint, strict=False)

# ✅ Move Model to GPU (if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")


# ✅ Extract text from JSON or file
def extract_text(req):
    """Extract text from JSON payload or uploaded file (PDF, DOCX)."""
    if "file" in request.files:
        file = request.files["file"]

        if file.filename.endswith(".pdf"):
            return extract_text_from_pdf(file)
        elif file.filename.endswith(".docx"):
            return extract_text_from_docx(file)
        else:
            return ""

    # If no file, extract from JSON request
    try:
        data = req.get_json(force=True)  # Force JSON parsing
        return data.get("text", "")
    except Exception:
        return ""


# ✅ Extract text from PDF
def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip()
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"


# ✅ Extract text from DOCX
def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file)
        text = " ".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"Error extracting text from DOCX: {str(e)}"


# ✅ Streaming Response Generator
def generate_summary_stream(text):
    """Generates summary in a streaming fashion for real-time response."""
    if not text:
        yield "No input text provided.\n"
        return

    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    time.sleep(1)  # Simulate processing delay

    with torch.no_grad():
        summary_ids = model.generate(**inputs, max_length=200, num_beams=5, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    yield summary  # ✅ Only send the summary (No original text)


@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        text = extract_text(request)

        if not text.strip():
            return Response("No extractable text found.\n", content_type="text/plain"), 400

        return Response(stream_with_context(generate_summary_stream(text)), content_type="text/plain")

    except Exception as e:
        return Response(f"Error: {str(e)}\n", content_type="text/plain"), 500


# ✅ Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
