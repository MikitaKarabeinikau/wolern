import React from "react";
import { useGeneratedExercises } from "../hooks/useGeneratedExercises";
import ExerciseField from "./ExerciseField";

const GeneratedBase = () => {
  const {
    currentExercise,
    isLoading,
    error,
    resetTrigger,
    handleNextExercise,
    hasExercises,
  } = useGeneratedExercises();

  if (error) {
    return (
      <div className="exercise-container error">
        <p className="error-message">{error}</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="exercise-container">
        <p>Loading exercises...</p>
      </div>
    );
  }

  if (!currentExercise) {
    return (
      <div className="exercise-container">
        <p>No exercises available.</p>
      </div>
    );
  }

  return (
    <div className="exercise-container">
      <ExerciseField
        word={currentExercise.word}
        exercise={currentExercise}
        resetTrigger={resetTrigger}
      />

      <button
        className="btn next-exercise-btn"
        onClick={handleNextExercise}
        disabled={isLoading || !hasExercises}
      >
        {isLoading ? "Loading..." : "Next Exercise"}
      </button>
    </div>
  );
};

export default GeneratedBase;
