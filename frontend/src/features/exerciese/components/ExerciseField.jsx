import React, { useState } from "react";
import "../../../../styles/Exercise.css";
import MultiAnswerExercise from "./MultiAnswerExercise";
import AnswerInputExercise from "./AnswerInuptExercise";

const ExerciseField = ({ word, exercise }) => {
  // Use a single state to manage the exercise type
  const [exerciseType, setExerciseType] = useState("input");
  console.log("Rendering AnswerInputExercise with word:", word);
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
            <AnswerInputExercise word={word} exercise={exercise} />
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
