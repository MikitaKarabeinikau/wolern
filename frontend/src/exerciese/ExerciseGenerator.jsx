import "react";
import { useState, useEffect } from "react";
import Exercise from "./Exercise";

function ExerciseGenerator() {
  const [exercises, setExercises] = useState(null);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [difficulty, setDifficulty] = useState(); // 'Beginner', 'Intermediate', 'Advanced'
  const [quota, setQuota] = useState(null); // number of exercises to generate

  const fetchQuota = async () => {};

  const generateExercise = async () => {};

  const getNextResetTime = () => {};

  return (
    <div>
      <h1>Exercise Generator</h1>
      <div>
        <h2>Quota number: {quota?.quota_remaining || 0}</h2>
        {quota?.quota_remaining === 0 && (
          <p>Quota exhausted. Next reset at: {getNextResetTime()}</p>
        )}
      </div>
      <div>
        <label htmlFor="difficulty-select">Select Difficulty:</label>
        <select
          id="difficulty-select"
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="Beginner">Beginner</option>
          <option value="Intermediate">Intermediate</option>
          <option value="Advanced">Advanced</option>
        </select>
      </div>

      <button onClick={generateExercise} disabled="generate-button">
        {isLoading ? "Loading..." : "Generate Exercise"}
      </button>

        {error && <div className="error-message"><p>Error: {error}</p></div>}
        {exercises && <Exercise data={exercises} />}
    </div>
  );
}

export default ExerciseGenerator;
