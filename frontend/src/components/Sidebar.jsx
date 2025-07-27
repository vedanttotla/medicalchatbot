import React from "react";

export default function Sidebar({ setActiveSection }) {
  return (
    <div className="sidebar">
      <button onClick={() => setActiveSection("search")}>Semantic Search</button>
      <button onClick={() => setActiveSection("create")}>Create Record</button>
      <button onClick={() => setActiveSection("update")}>Update Record</button>
      <button onClick={() => setActiveSection("delete")}>Delete Record</button>
      <button onClick={() => setActiveSection("get")}>Get Record</button>
    </div>
  );
}