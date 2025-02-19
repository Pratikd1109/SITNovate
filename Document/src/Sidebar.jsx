import React from "react";
import ModelSelector from "./ModelSelector";
import "./Sidebar.css";

const Sidebar = ({ setSelectedModel }) => {
  return (
    <div className="sidebar">
     
      <ModelSelector setSelectedModel={setSelectedModel} />
    </div>
  );
};

export default Sidebar;
