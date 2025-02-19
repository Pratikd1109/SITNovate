import React, { useState } from "react";
import "./UploadPage.css";

const UploadPage = ({ selectedModel }) => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [responseText, setResponseText] = useState("");

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
    formData.append("model", selectedModel); // Send selected model type

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setUploadStatus("Processing complete!");
        setResponseText(result.summary);
      } else {
        setUploadStatus("Error: " + result.error);
      }
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
      {responseText && <div className="response-box">{responseText}</div>}
    </div>
  );
};

export default UploadPage;
