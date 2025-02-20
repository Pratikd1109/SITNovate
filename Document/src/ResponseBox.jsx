import React from "react";
import "./ResponseBox.css";

const ResponseBox = ({ responseText }) => {
  return (
    <div className="response-box">
      <h3>📄 Summarized Text:</h3>
      <p>{responseText || "⏳ Waiting for response..."}</p>
    </div>
  );
};

export default ResponseBox;
