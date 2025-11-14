import React, { useState } from "react";
import "../../../styles/Exercise.css";
import "../../../styles/Buttons.css";

import ExerciseGenerator from "./components/ExerciseGenerator";
import GeneratedBase from "./components/GeneratedBase";

export function ExercisesPanel() {
  const [chosenPanel, setChosenPanel] = useState("generator");

  return (
    <>
      <div className="exercise-panel-container">
        <div>
          <div className="menu-container">
            <div className="menu-type-selector">
              <button
                className={chosenPanel === "generator" ? "active" : ""}
                onClick={() => setChosenPanel("generator")}
              >
                <strong>Exercise Generator</strong>
              </button>
              <button
                className={chosenPanel === "generatedBase" ? "active" : ""}
                onClick={() => setChosenPanel("generatedBase")}
              >
                <strong>Generated Exercises Base</strong>
              </button>
            </div>
          </div>
        </div>
        <div className="exercise-display">
          {chosenPanel === "generator" && <ExerciseGenerator />}
          {chosenPanel === "generatedBase" && <GeneratedBase />}
        </div>
      </div>
    </>
  );
}
export default ExercisesPanel;
