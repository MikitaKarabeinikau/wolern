import React, { useState } from "react";
import Exercise from "./Exercise";
import "../../styles/Exercise.css";
import ExerciseGenerator from "./ExerciseGenerator";

export function ExercisesPanel() {
  const [isGenerating, setIsGenerating] = useState(false);

  return (
    <>
      <div className="exercise-panel-container">
        <div className="exercise-menu">
          <div
            className="menu-item"
            onClick={() => {
              setIsGenerating(!isGenerating);
            }}
          >
            Generate Exercise
          </div>
          <div className="menu-item">View Exercises</div>
        </div>
        <div className="exercise-display">
          {isGenerating && <ExerciseGenerator />}
        </div>
      </div>
    </>
  );
}
s;
