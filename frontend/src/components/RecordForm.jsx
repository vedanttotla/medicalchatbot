import React, { useState } from "react";
import axios from '../api'; 

export default function RecordForm({ mode }) {
  const [id, setId] = useState("");
  const [name, setName] = useState("");
  const [complaint, setComplaint] = useState("");
  const [diagnosis, setDiagnosis] = useState("");
  const [prescription, setPrescription] = useState("");
  const [similarity, setSimilarity] = useState("");

  const handleSubmit = async () => {
    try {
      if (mode === "create") {
        await axios.post(`/create-record/${id}`, { name, medical_condition: diagnosis });
      } else if (mode === "update") {
        await axios.put(`/update-record/${id}`, { name, medical_condition: diagnosis });
      } else if (mode === "delete") {
        await axios.delete(`/delete-record/${id}`);
      } else if (mode === "get") {
        const res = await axios.get(`/get-record/${id}`);
        setName(res.data.name);
        setComplaint(res.data.complaint);
        setDiagnosis(res.data.diagnosis);
        setPrescription(res.data.prescription);
        setSimilarity(res.data.similarity_score);
      }
      alert(`${mode} operation successful`);
    } catch (error) {
      alert(`Error: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div className="form-container">
      <h2>{mode.toUpperCase()} RECORD</h2>
      <input
        type="text"
        placeholder="Visit ID"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />

      {(mode === "create" || mode === "update") && (
        <>
          <input
            type="text"
            placeholder="Patient Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            type="text"
            placeholder="Condition"
            value={diagnosis}
            onChange={(e) => setDiagnosis(e.target.value)}
          />
        </>
      )}

      {mode === "get" && (
        <div className="record-details">
          <p><strong>Name:</strong> {name}</p>
          <p><strong>Complaint:</strong> {complaint}</p>
          <p><strong>Diagnosis:</strong> {diagnosis}</p>
          <p><strong>Prescription:</strong> {prescription}</p>
          <p><strong>Similarity Score:</strong> {similarity}</p>
        </div>
      )}

      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}
