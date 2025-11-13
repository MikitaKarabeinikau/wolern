import React, { useState } from "react";
import "../../../styles/Exercise.css";
import ExerciseGenerator from "./components/ExerciseGenerator";
import GeneratedBase from "./components/GeneratedBase";

export function ExercisesPanel() {
  const [isGenerating, setIsGenerating] = useState(true);
  const [isGeneratedBase, setIsGeneratedBase] = useState(false);

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
          <div
            className="menu-item"
            onClick={() => {
              setIsGeneratedBase(!isGeneratedBase);
              if (isGenerating) setIsGenerating(false);
            }}
          >
            Base of Exercises
          </div>
        </div>
        <div className="exercise-display">
          {isGenerating && <ExerciseGenerator />}
          {isGeneratedBase && <GeneratedBase />}
        </div>
      </div>
    </>
  );
}
export default ExercisesPanel;
