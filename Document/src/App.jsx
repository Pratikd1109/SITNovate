import React, { useState } from "react";
import Sidebar from "./Sidebar";
import UploadPage from "./UploadPage";
import ResponseBox from "./ResponseBox"; // Import ResponseBox
import "./App.css";

function App() {
  const [selectedModel, setSelectedModel] = useState("Standard AI");
  const [responseText, setResponseText] = useState(""); // For streaming response

  return (
    <div className="app-container">
      <Sidebar setSelectedModel={setSelectedModel} />
      
      <div className="main-content">
        <h1>FUSION SUM UP (AI Document Summerizer)</h1>

        {/* Response Box at the top */}
        <ResponseBox responseText={responseText} />

        {/* Upload Box at the bottom */}
        <UploadPage selectedModel={selectedModel} setResponseText={setResponseText} />
      </div>
    </div>
  );
}

export default App;
