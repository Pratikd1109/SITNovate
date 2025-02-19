import React, { useState } from "react";
import "./UploadPage.css";

const UploadPage = ({ selectedModel }) => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [progress, setProgress] = useState(0);
  const [responseText, setResponseText] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadStatus("");
    setProgress(0);
    setResponseText("");
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus("Please select a file first.");
      return;
    }

    setUploadStatus("Uploading...");
    setProgress(0);
    setResponseText("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("model", selectedModel);

    try {
      const response = await fetch("https://api.example.com/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.body) {
        throw new Error("No response stream available");
      }

      setUploadStatus("Processing...");
      
      // Process streaming response
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let receivedText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        receivedText += chunk;
        setResponseText(receivedText); // Update UI dynamically
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
      <button onClick={handleUpload} className="upload-button">Upload & Send to AI</button>
      {uploadStatus && <p className="status-message">{uploadStatus}</p>}
      {responseText && <div className="response-box">{responseText}</div>}
    </div>
  );
};

export default UploadPage;
