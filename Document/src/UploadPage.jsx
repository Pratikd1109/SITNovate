import React, { useState } from "react";
import "./UploadPage.css";

const UploadPage = ({ setResponseText, selectedModel }) => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadStatus("");
    setResponseText("");
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus("❌ Please select a file first.");
      return;
    }

    setUploadStatus("⏳ Uploading...");

    const formData = new FormData();
    formData.append("file", file);

    // Determine the correct API endpoint
    const apiUrl = selectedModel === "Legal Contracts" 
      ? "http://127.0.0.1:5000/summarize" 
      : "http://127.0.0.1:5001/summarize";

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        body: formData,
      });

      if (!response.body) {
        setUploadStatus("⚠️ No response from server.");
        return;
      }

      setUploadStatus("🔄 Processing...");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let resultText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        resultText += decoder.decode(value, { stream: true });
        setResponseText(resultText); // Update the response box in real-time
      }

      setUploadStatus("✅ Processing complete!");
    } catch (error) {
      setUploadStatus("❌ Error during upload or processing.");
      console.error("Error:", error);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-controls">
        <input type="file" onChange={handleFileChange} className="file-input" />
        <button onClick={handleUpload} className="upload-button">
          Upload & Summarize
        </button>
      </div>
      {uploadStatus && <p className="status-message">{uploadStatus}</p>}
    </div>
  );
};

export default UploadPage;
