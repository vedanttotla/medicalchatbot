import React, { useState } from "react";
import axios from '../api';



export default function SearchBox() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const res = await axios.post("/search-query", { query });
      setResults(res.data);
    } catch (err) {
      alert("Search error: " + err.message);
    }
  };

  return (
    <div className="search-container">
      <h2>Semantic Search</h2>
      <input value={query} onChange={e => setQuery(e.target.value)} placeholder="e.g., cough" />
      <button onClick={handleSearch}>Search</button>
      <ul>
        {results.length > 0 && (
  <table className="search-results-table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Complaint</th>
        <th>Diagnosis</th>
        <th>Prescription</th>
        <th>Similarity</th>
      </tr>
    </thead>
    <tbody>
      {results.map((r, i) => (
        <tr key={i}>
          <td>{r.name}</td>
          <td>{r.complaint}</td>
          <td>{r.diagnosis}</td>
          <td>{r.prescription}</td>
          <td>{r.similarity_score}</td>
        </tr>
      ))}
    </tbody>
  </table>
)}

      </ul>
    </div>
  );
}