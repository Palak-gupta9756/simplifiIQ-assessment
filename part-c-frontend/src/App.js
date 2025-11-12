import React, { useEffect, useState } from "react";
import Papa from "papaparse";

function App() {
  const [data, setData] = useState([]);
  const [search, setSearch] = useState("");
  const [filteredData, setFilteredData] = useState([]);

  // Load CSV from public folder
  const loadCSV = () => {
    Papa.parse("/scraped_summary.csv", {
      download: true,
      header: true,
      complete: (result) => {
        setData(result.data);
        setFilteredData(result.data);
      },
    });
  };

  useEffect(() => {
    loadCSV();
  }, []);

  // Handle search filter
  useEffect(() => {
    const lowerSearch = search.toLowerCase();
    const filtered = data.filter(
      (row) =>
        row.title?.toLowerCase().includes(lowerSearch) ||
        row.meta_description?.toLowerCase().includes(lowerSearch) ||
        row.ai_summary?.toLowerCase().includes(lowerSearch)
    );
    setFilteredData(filtered);
  }, [search, data]);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2>🔍 Web Summary Dashboard</h2>

      <div style={{ marginBottom: "15px" }}>
        <input
          type="text"
          placeholder="Search by keyword..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            padding: "8px",
            width: "300px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            marginRight: "10px",
          }}
        />
        <button
          onClick={loadCSV}
          style={{
            padding: "8px 12px",
            borderRadius: "5px",
            border: "none",
            backgroundColor: "#007bff",
            color: "white",
            cursor: "pointer",
          }}
        >
          🔄 Refresh
        </button>
      </div>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          fontSize: "14px",
        }}
      >
        <thead>
          <tr style={{ backgroundColor: "#f2f2f2" }}>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>URL</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Title</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Meta Description</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>AI Summary</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((row, idx) => (
            <tr key={idx}>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                <a href={row.url} target="_blank" rel="noreferrer">
                  {row.url}
                </a>
              </td>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>{row.title}</td>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>{row.meta_description}</td>
              <td style={{ border: "1px solid #ddd", padding: "8px" }}>{row.ai_summary}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
