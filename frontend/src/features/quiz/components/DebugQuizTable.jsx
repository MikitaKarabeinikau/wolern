import React from "react";

const DebugQuizTable = ({ data }) => {
  if (!data || data.length === 0) {
    return <p>No debug data available.</p>;
  }

  const formatDateTime = (dateString) => {
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      day: "2-digit",
      month: "2-digit",
    });
  };

  return (
    <div style={{ marginTop: "2rem", fontFamily: "monospace" }}>
      <h3>Debug Info</h3>
      <table border="1" style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Word</th>
            <th>Stage</th>
            <th>Correct</th>
            <th>Correct (Row)</th>
            <th>Wrong</th>
            <th>Wrong (Row)</th>
            <th>Next Review</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id}>
              <td>{item.word}</td>
              <td>{item.progress.learning_stage || "N/A"}</td>
              <td>{item.progress.correct_answers || 0}</td>
              <td>{item.progress.correct_answers_in_a_row || 0}</td>
              <td>{item.progress.wrong_answers || 0}</td>
              <td>{item.progress.wrong_answers_in_a_row || 0}</td>
              <td>{formatDateTime(item.progress.next_review_date)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DebugQuizTable;
