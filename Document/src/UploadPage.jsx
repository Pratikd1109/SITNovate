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

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus("Please select a file first.");
      return;
    }

    setUploadStatus("Uploading...");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("model", selectedModel);

    try {
      const response = await fetch("http://localhost:5000/extract-text", {
        method: "POST",
        body: formData,
      });

      if (!response.body) {
        setUploadStatus("No response from server.");
        return;
      }

      setUploadStatus("Processing...");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let resultText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        resultText += decoder.decode(value, { stream: true });
        setResponseText(resultText);
      }

      setUploadStatus("Processing complete!");
    } catch (error) {
      setUploadStatus("Error during upload or processing.");
      console.error("Error:", error);
    }
  };

  return (
    <div className="upload-container">
      <input type="file" onChange={handleFileChange} className="file-input" />
      <button onClick={handleUpload} className="upload-button">
        Upload & Summarize
      </button>
      {uploadStatus && <p className="status-message">{uploadStatus}</p>}
    </div>
  );
};

export default UploadPage;
