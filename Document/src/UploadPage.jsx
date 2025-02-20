import React, { useState } from "react";
import "./UploadPage.css";

const UploadPage = ({ selectedModel, setResponseText }) => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadStatus("");
    setResponseText("");
  };

  // Function to get API endpoint based on selected model
  const getApiEndpoint = () => {
    switch (selectedModel) {
      case "Articles":
        return "http://127.0.0.1:5000/summarize";
      case "Research Paper":
        return "http://127.0.0.1:5001/summarize";
      case "Legal Contracts":
        return "http://127.0.0.1:5002/summarize";
      default:
        return "http://127.0.0.1:5003/summarize"; // Default to Articles API
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus("❌ Please select a file first.");
      return;
    }

    setUploadStatus("⏳ Uploading...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(getApiEndpoint(), {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        setUploadStatus("⚠️ Server error.");
        return;
      }

      const data = await response.json();
      setResponseText(data.summary); // Set the summarized response text

      setUploadStatus("✅ Summary Ready!");
    } catch (error) {
      setUploadStatus("❌ Error during upload.");
      console.error("Upload Error:", error);
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
