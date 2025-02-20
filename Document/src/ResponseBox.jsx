import React, { useEffect, useRef } from "react";
import "./ResponseBox.css";

const ResponseBox = ({ responseText }) => {
  const responseRef = useRef(null);

  // Ensure smooth scrolling as new text streams in
  useEffect(() => {
    if (responseRef.current) {
      responseRef.current.innerHTML = responseText || "⏳ Waiting for response...";
    }
  }, [responseText]);

  return (
    <div className="response-box">
      <h3>📄 Summarized Text:</h3>
      <p ref={responseRef}></p>
    </div>
  );
};

export default ResponseBox;
