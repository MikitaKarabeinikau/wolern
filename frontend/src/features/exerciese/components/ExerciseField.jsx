import React, { useEffect, useState } from "react";
import "../../../../styles/Exercise.css";
import MultiAnswerExercise from "./MultipleChooseExercise";
import AnswerInputExercise from "./AnswerInuptExercise";

const EXERCISE_TYPES = {
  INPUT: "input",
  MULTIPLE: "multiple",
};

const ExerciseField = ({ word, exercise, resetTrigger }) => {
  const [exerciseType, setExerciseType] = useState(EXERCISE_TYPES.INPUT);
  const [userAnswer, setUserAnswer] = useState("");
  const [selectedOption, setSelectedOption] = useState(null);

  // Reset state when exercise changes
  useEffect(() => {
    setUserAnswer("");
    setSelectedOption(null);
  }, [resetTrigger]);

  const renderExercise = () => {
    switch (exerciseType) {
      case EXERCISE_TYPES.INPUT:
        return (
          <AnswerInputExercise
            word={word}
            exercise={exercise}
            userAnswer={userAnswer}
            setUserAnswer={setUserAnswer}
          />
        );
      case EXERCISE_TYPES.MULTIPLE:
        return (
          <MultiAnswerExercise
            exercise={exercise}
            selectedOption={selectedOption}
            setSelectedOption={setSelectedOption}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="exercise-container">
      <div className="exercise-type-menu">
        <button
          className={`exercise-type-button ${
            exerciseType === EXERCISE_TYPES.INPUT ? "active" : ""
          }`}
          onClick={() => setExerciseType(EXERCISE_TYPES.INPUT)}
        >
          Answer Input
        </button>
        <button
          className={`exercise-type-button ${
            exerciseType === EXERCISE_TYPES.MULTIPLE ? "active" : ""
          }`}
          onClick={() => setExerciseType(EXERCISE_TYPES.MULTIPLE)}
        >
          Multiple Choice
        </button>
      </div>

      <div className="exercise-content">{renderExercise()}</div>
    </div>
  );
};

export default ExerciseField;
