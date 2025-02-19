import React, { useState } from "react";
import "./ModelSelector.css";

const ModelSelector = ({ setSelectedModel }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentModel, setCurrentModel] = useState("Document Type");

  const models = [
    { name: "Articles", description: "Great for everyday tasks" },
    { name: "Research Paper", description: "More powerful with deeper analysis" },
    { name: "Legal Contracts", description: "Best for complex problem-solving" },
    
  ];

  const handleSelect = (model) => {
    setCurrentModel(model.name);
    setSelectedModel(model.name);
    setIsOpen(false);
  };

  return (
    <div className="dropdown">
      <div className="dropdown-header" onClick={() => setIsOpen(!isOpen)}>
        <span>{currentModel}</span>
        <span className="arrow">{isOpen ? "▲" : "▼"}</span>
      </div>
      {isOpen && (
        <ul className="dropdown-list">
          {models.map((model, index) => (
            <li
              key={index}
              className={`dropdown-item ${currentModel === model.name ? "selected" : ""}`}
              onClick={() => handleSelect(model)}
            >
              <div className="model-name">{model.name}</div>
              <div className="model-description">{model.description}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ModelSelector;
