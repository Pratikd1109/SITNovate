import React, { useState } from "react";
import Sidebar from "./Sidebar";
import UploadPage from "./UploadPage";
import "./App.css";

function App() {
  const [selectedModel, setSelectedModel] = useState("Standard AI");

  return (
    <div className="app-container">
      <Sidebar setSelectedModel={setSelectedModel} />
      <div className="main-content">
        <h1>AI Document Processor</h1>
        <UploadPage selectedModel={selectedModel} />
      </div>
    </div>
  );
}

export default App;
