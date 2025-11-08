import { useState, useEffect } from "react";
import Exercise from "./Exercise";
import { useApi } from "../utils/utils";
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
      const response = await fetch(`http://localhost:8000/exercise/quota`, {
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
      setQuota(data);
    } catch (err) {
      console.log("Error fetching quota:", err);
      setError(err.message);
    }
  };

  const generateExercise = async () => {
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

  const getNextResetTime = () => {
    if (!quota?.reset_time) return null;
    const resetDate = new Date(quota.reset_time);
    resetDate.setHours(resetDate.getHours() + 24);
    return resetDate.toLocaleString();
  };

  return (
    <>
      <div>
        <h1>Exercise Generator</h1>
        <div>
          <h2>Quota number: {quota?.exercises_remaining || 0}</h2>
          {quota?.quota_remaining === 0 && (
            <p>Quota exhausted. Next reset at: {getNextResetTime()}</p>
          )}
        </div>
        <div>
          <h1>Word for Exercise: {word}</h1>
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

        <button onClick={generateExercise} disabled={false}>
          {isLoading ? "Loading..." : "Generate Exercise"}
        </button>
        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}
        {exercises && <Exercise data={exercises["exercise"]} />}
      </div>
    </>
  );
}

export default ExerciseGenerator;
