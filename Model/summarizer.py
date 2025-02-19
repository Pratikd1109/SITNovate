from transformers import BartForConditionalGeneration, BartTokenizer

# Set MODEL_PATH to the 'Model' folder (not a subfolder)
MODEL_PATH = "C:/Users/sivya/OneDrive/Desktop/Model"

# Load model and tokenizer from Model folder
tokenizer = BartTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = BartForConditionalGeneration.from_pretrained(MODEL_PATH, local_files_only=True)

print("✅ Model loaded successfully!")

# Get user input
text = input("\nEnter text to summarize:\n")

# Tokenize input
inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)

# Generate summary
summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)

# Decode and print summary
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print("\n🔹 Summary:\n", summary)
