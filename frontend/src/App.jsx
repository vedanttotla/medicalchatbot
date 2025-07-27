import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import RecordForm from "./components/RecordForm";
import RecordViewer from "./components/RecordViewer";
import SearchBox from "./components/SearchBox";

export default function App() {
  const [activeSection, setActiveSection] = useState("search");

  return (
    <div className="app-container">
      <Sidebar setActiveSection={setActiveSection} />
      <main className="main-content">
        {activeSection === "search" && <SearchBox />}
        {["create", "update", "delete", "get"].includes(activeSection) && (
          <RecordForm mode={activeSection} />
        )}
        {activeSection === "viewer" && <RecordViewer />}
      </main>
    </div>
  );
}