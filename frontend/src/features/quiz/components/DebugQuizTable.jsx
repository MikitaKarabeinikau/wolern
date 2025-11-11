import React from "react";

const DebugQuizTable = () => {
  return (
    <div style={{ flex: 1, padding: "20px", borderLeft: "1px solid #ccc" }}>
      <h3>Progress Data</h3>
      {progress.length > 0 ? (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            tableLayout: "auto",
          }}
        >
          <thead>
            <tr>
              <th>Word</th>
              <th>Correct Answers</th>
              <th>Wrong Answers</th>
              <th>Learning Stage</th>
              <th>Correct Answers in a Row</th>
              <th>Wrong Answers in a Row</th>
              <th>Time to Repeat</th>
            </tr>
          </thead>
          <tbody>
            {progress.map((p) => {
              const word =
                words.find((w) => w.id === p.word_id)?.word || "Unknown Word";
              return (
                <tr key={p.word_id}>
                  <td>{word}</td>
                  <td>{p.correct_answers || 0}</td>
                  <td>{p.wrong_answers || 0}</td>
                  <td>{p.learning_stage || 0}</td>
                  <td>{p.correct_answers_in_a_row || 0}</td>
                  <td>{p.wrong_answers_in_a_row || 0}</td>
                  <td>{formatDateTime(p.time_to_repeat)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      ) : (
        <p>No progress data available.</p>
      )}
    </div>
  );
};

export default DebugQuizTable;
