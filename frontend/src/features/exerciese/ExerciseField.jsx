import React, { useState } from "react";
import "../../../styles/Exercise.css";
import MultiAnswerExercise from "./MultiAnswerExercise";

const ExerciseField = ({ exercise }) => {
  // Use a single state to manage the exercise type
  const [exerciseType, setExerciseType] = useState("input");

  return (
    <div className="exercise-field-container">
      <div className="exercise-type-selector">
        <button
          className={exerciseType === "input" ? "active" : ""}
          onClick={() => setExerciseType("input")}
        >
          <strong>Answer Input</strong>
        </button>
        <button
          className={exerciseType === "multiple" ? "active" : ""}
          onClick={() => setExerciseType("multiple")}
        >
          <strong>Multiple Choice</strong>
        </button>
      </div>

      <div className="exercise-content">
        {exerciseType === "input" && (
          <div>
            <p>This is the Answer Input exercise area.</p>
          </div>
        )}
        {exerciseType === "multiple" && (
          <div>
            <MultiAnswerExercise exercise={exercise} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ExerciseField;
