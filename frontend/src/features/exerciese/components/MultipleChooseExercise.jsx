import React, { useEffect, useState, useMemo } from "react";
import "../../../../styles/Exercise.css";
import HintUnit from "./HintUnit";

function MultipleChooseExercise({
  exercise,
  selectedOption,
  setSelectedOption,
}) {
  const [isAnswered, setIsAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const { question, part_of_speech, explanation, hints, multiple_choice } =
    exercise || {};
  const { options = [], correct_answer } = multiple_choice || {};

  const correctAnswerIndex = useMemo(
    () => parseInt(correct_answer, 10),
    [correct_answer]
  );

  // Reset states whenever a new exercise is loaded
  useEffect(() => {
    setIsAnswered(false);
    setSelectedOption(null);
    setIsCorrect(false);
  }, [exercise, setSelectedOption]);

  const handleAnswerSelect = (index) => {
    if (isAnswered) return;

    setSelectedOption(index);
    setIsAnswered(true);
    setIsCorrect(index === correctAnswerIndex);
  };

  const getOptionClassName = (index) => {
    let className = "option-button";

    if (isAnswered) {
      if (index === correctAnswerIndex) {
        className += " correct";
      } else if (index === selectedOption) {
        className += " incorrect";
      }
    }

    return className;
  };

  if (!exercise || !multiple_choice) {
    return (
      <div className="exercise-container">
        <p>No exercise available.</p>
      </div>
    );
  }

  return (
    <div className="exercise-container">
      <div className="exercise-content">
        <div className="exercise-header">
          <span className="part-of-speech">{part_of_speech}</span>
        </div>
        <div className="middle-section">
          <p className="question">{question}</p>
        </div>

        <div className="mc-options">
          {options.map((option, index) => (
            <button
              key={index}
              className={getOptionClassName(index)}
              onClick={() => handleAnswerSelect(index)}
              disabled={isAnswered}
              aria-label={`Option ${index + 1}: ${option}`}
            >
              {option}
            </button>
          ))}
        </div>

        {isAnswered && !isCorrect && (
          <div className="explanation-section">
            <h4>Explanation</h4>
            <p>{explanation}</p>
          </div>
        )}
      </div>

      <div className="exercise-hints">
        <div className="hints-list">
          {hints?.map((hint, index) => (
            <HintUnit key={`hint-${index}`} index={index} hint={hint} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default MultipleChooseExercise;
