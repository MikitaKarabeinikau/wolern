import React, { useEffect, useState } from "react";
import "../../../../styles/Exercise.css";
import MultiAnswerExercise from "./MultipleChooseExercise";
import AnswerInputExercise from "./AnswerInuptExercise";

const ExerciseField = ({ word, exercise, resetTrigger }) => {
  const [exerciseType, setExerciseType] = useState("input");
  const [userAnswer, setUserAnswer] = useState(""); // State for user's answer
  const [selectedOption, setSelectedOption] = useState(null); // For multiple choice

  useEffect(() => {
    console.log("Reset triggered"); // Debug log to ensure resetTrigger changes
    setUserAnswer("");
    setSelectedOption(null);
  }, [resetTrigger]);

  return (
    <div className="exercise-container">
      {/* Menu for selecting exercise type */}
      <div className="exercise-type-menu">
        <button
          className={`exercise-type-button ${
            exerciseType === "input" ? "active" : ""
          }`}
          onClick={() => setExerciseType("input")}
        >
          Answer Input
        </button>
        <button
          className={`exercise-type-button ${
            exerciseType === "multiple" ? "active" : ""
          }`}
          onClick={() => setExerciseType("multiple")}
        >
          Multiple Choice
        </button>
      </div>

      {/* Render the selected exercise type */}
      <div className="exercise-content">
        {exerciseType === "input" && (
          <AnswerInputExercise
            word={word}
            exercise={exercise}
            userAnswer={userAnswer}
            setUserAnswer={setUserAnswer} // Pass state for user's answer
          />
        )}
        {exerciseType === "multiple" && (
          <MultiAnswerExercise
            exercise={exercise}
            selectedOption={selectedOption}
            setSelectedOption={setSelectedOption}
          />
        )}
      </div>
    </div>
  );
};

export default ExerciseField;
