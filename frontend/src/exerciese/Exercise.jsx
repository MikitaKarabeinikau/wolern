import React, { useState } from "react";
import "../../styles/Exercise.css";
import HintUnit from "./HintUnit";

function Exercise({ exercise }) {
  const [selectedOption, setSelectedOption] = useState(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const { question, part_of_speech, explanation, hints, multiple_choice } =
    exercise;
  const { options, correct_answer } = multiple_choice;

  const handleAnswerSelect = (option, index) => {
    if (isAnswered) return; // Prevent re-answering

    setSelectedOption(index);
    setIsAnswered(true);

    // --- FIX: Check answer and update state HERE ---
    const isAnswerCorrect = index === parseInt(correct_answer, 10);
    setIsCorrect(isAnswerCorrect);
  };

  return (
    <div className="exercise-container">
      <div className="exercise-content">
        <div className="exercise-header">
          <span className="part-of-speech">{part_of_speech}</span>
          <p className="question">{question}</p>
        </div>

        <div className="mc-options">
          {options.map((option, index) => {
            const isCorrectAnswer = index === parseInt(correct_answer, 10);
            const isSelectedAnswer = index === selectedOption;
            let buttonClass = "option-button";

            // --- FIX: REMOVED state update from render logic ---
            if (isAnswered) {
              if (isCorrectAnswer) {
                buttonClass += " correct";
              } else if (isSelectedAnswer) {
                buttonClass += " incorrect";
              }
            }

            return (
              <button
                key={index}
                className={buttonClass}
                onClick={() => handleAnswerSelect(option, index)}
                disabled={isAnswered}
              >
                {option}
              </button>
            );
          })}
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
          {hints.map((hint, index) => (
            <HintUnit key={index} index={index} hint={hint} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default Exercise;
