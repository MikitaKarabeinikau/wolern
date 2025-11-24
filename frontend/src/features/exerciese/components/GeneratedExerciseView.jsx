import React from "react";
import ExerciseField from "./ExerciseField";

const GeneratedExerciseView = ({
  currentWord,
  exercise,
  resetTrigger,
  isLoading,
  onGenerateAnother,
}) => {
  return (
    <div>
      <ExerciseField
        word={currentWord?.word}
        exercise={exercise}
        resetTrigger={resetTrigger}
      />
      <button
        className="generate-button"
        onClick={onGenerateAnother}
        disabled={isLoading}
      >
        {isLoading ? "Loading..." : "Generate Another Exercise"}
      </button>
    </div>
  );
};

export default GeneratedExerciseView;
