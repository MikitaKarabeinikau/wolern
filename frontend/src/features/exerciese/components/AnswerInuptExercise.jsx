import React, { useState, useEffect } from "react";
import "../../../../styles/Exercise.css";
import "../../../../styles/QuizAnswerUnit.css";
import ExerciseResultView from "./ExerciseResultView";
import ExerciseInputView from "./ExerciseInputView";

const AnswerInputExercise = ({ word, exercise, userAnswer, setUserAnswer }) => {
  const [isAnswered, setIsAnswered] = useState(false);

  const { question, part_of_speech, explanation, hints } = exercise || {};

  // Reset state when exercise changes
  useEffect(() => {
    setIsAnswered(false);
    setUserAnswer("");
  }, [exercise, setUserAnswer]);

  const handleAnswer = () => {
    if (userAnswer?.trim()) {
      setIsAnswered(true);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleAnswer();
    }
  };

  if (!exercise) {
    return <div className="exercise-container">No exercise available.</div>;
  }

  return (
    <div className="exercise-container">
      {!isAnswered ? (
        <ExerciseInputView
          partOfSpeech={part_of_speech}
          question={question}
          hints={hints}
          userAnswer={userAnswer}
          setUserAnswer={setUserAnswer}
          handleAnswer={handleAnswer}
          handleKeyPress={handleKeyPress}
        />
      ) : (
        <ExerciseResultView
          partOfSpeech={part_of_speech}
          question={question}
          word={word}
          userAnswer={userAnswer}
          explanation={explanation}
        />
      )}
    </div>
  );
};

export default AnswerInputExercise;
