import React from "react";

const DIFFICULTY_LEVELS = ["Beginner", "Intermediate", "Advanced"];

const ExerciseGeneratorForm = ({
  currentWord,
  difficulty,
  setDifficulty,
  isLoading,
  error,
  canGenerate,
  onGenerate,
}) => {
  return (
    <div>
      <h2>Create a New Exercise</h2>
      <p>
        Generate a new vocabulary exercise for the word:{" "}
        <strong>{currentWord?.word || "..."}</strong>
      </p>

      <div className="form-group">
        <label htmlFor="difficulty-select">Difficulty</label>
        <select
          id="difficulty-select"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          disabled={isLoading}
        >
          {DIFFICULTY_LEVELS.map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>
      </div>

      {error && <p className="error-message">{error}</p>}

      <button
        className="generate-button"
        onClick={onGenerate}
        disabled={!canGenerate}
      >
        {isLoading ? "Generating..." : "Generate Exercise"}
      </button>
    </div>
  );
};

export default ExerciseGeneratorForm;
