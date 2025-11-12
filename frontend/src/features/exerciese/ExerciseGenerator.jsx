import { useState, useEffect } from "react";
import Exercise from "./Exercise";
import { useApi } from "../../utils/utils";
import { useAuth } from "@clerk/clerk-react";

function ExerciseGenerator() {
  const [exercises, setExercises] = useState("");
  const [multipleChoice, setMultipleChoice] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [difficulty, setDifficulty] = useState("Beginner"); // 'Beginner', 'Intermediate', 'Advanced'
  const [quota, setQuota] = useState(null); // number of exercises to generate
  const [word, setWord] = useState("");
  const { makeRequest } = useApi();
  const [isGenerated, setIsGenerated] = useState(false);
  const [wordId, setWordId] = useState(null);
  const { getToken } = useAuth();

  const getWordForExercise = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/exercise/word/random`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error("Failed to fetch random word");
      }
      const data = await response.json();
      setWord(data.word);
      setWordId(data.id);
    } catch (err) {
      console.log("Error fetching word:", err);
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchQuota();
    getWordForExercise();
  }, []);

  const fetchQuota = async () => {
    try {
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quota/`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error("Failed to fetch quota");
      }
      const data = await response.json();
      console.log("Quota data:", data);
      setQuota(data);
    } catch (err) {
      console.log("Error fetching quota:", err);
      setError(err.message);
    }
  };

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/exercise/generate-exercise/${wordId}`, // Include wordId in the URL path
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ word, difficulty }), // Send both word and difficulty in the request body
        }
      );
      if (!response.ok) {
        throw new Error("Failed to generate exercise");
      }
      const data = await response.json();
      setExercises(data);
      setMultipleChoice(data["multiple_choice"] || false);
      setIsGenerated(true);
      fetchQuota(); // Update quota after generating exercise
    } catch (err) {
      console.log("Error generating exercise:", err);
      setError(
        err.message || "An error occurred while generating the exercise."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateAnother = () => {
    setIsGenerated(false);
    setExercises("");
    getWordForExercise();
  };

  const getNextResetTime = () => {
    if (!quota?.reset_time) return null;
    const resetDate = new Date(quota.reset_time);
    resetDate.setHours(resetDate.getHours() + 24);
    return resetDate.toLocaleString();
  };

  return (
    <div className="generator-card">
      <div className="quota-display">
        <p>Quota: {quota?.exercises_remaining ?? "..."}</p>
        {quota?.exercises_remaining === 0 && (
          <span>Next reset: {getNextResetTime()}</span>
        )}
      </div>

      {isGenerated && exercises ? (
        // --- DISPLAY VIEW ---
        <div>
          <h2>Current Generated Exercise</h2>
          <Exercise exercise={exercises.exercise} />
          <button className="generate-button" onClick={handleGenerateAnother}>
            {isLoading ? "Loading..." : "Generate Another Exercise"}
          </button>
        </div>
      ) : (
        // --- GENERATE VIEW ---
        <div>
          <h2>Create a New Exercise</h2>
          <p>
            Generate a new vocabulary exercise for the word:{" "}
            <strong>{word || "..."}</strong>
          </p>

          <div className="form-group">
            <label htmlFor="difficulty-select">Difficulty</label>
            <select
              id="difficulty-select"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              disabled={isLoading}
            >
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>

          {error && <p className="error-message">{error}</p>}

          <button
            className="generate-button"
            onClick={handleGenerate}
            disabled={isLoading || quota?.exercises_remaining === 0}
          >
            {isLoading ? "Generating..." : "Generate Exercise"}
          </button>
        </div>
      )}
    </div>
  );
}

export default ExerciseGenerator;
