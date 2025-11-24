import React, { useMemo } from "react";
import { calculateIndexes } from "../../../utils/wordProcessing";
import "../../../../styles/QuizAnswerUnit.css";

const AnswerResult = ({ word, userAnswer }) => {
  // Use useMemo instead of useEffect + useState for better performance
  const {
    correct: correctIndexes,
    incorrect: incorrectIndexes,
    extraCorrect: extraCorrectIndexes,
    extraIncorrect: extraIncorrectIndexes,
  } = useMemo(() => {
    if (!userAnswer || !word) {
      return {
        correct: [],
        incorrect: [],
        extraCorrect: [],
        extraIncorrect: [],
      };
    }
    return calculateIndexes(word, userAnswer);
  }, [word, userAnswer]);

  if (!word || !userAnswer) {
    return null;
  }

  return (
    <div className="quiz-answers-container">
      <div className="quiz-correct-answer">
        {word.split("").map((letter, index) => (
          <span
            key={index}
            className={`quiz-letter ${
              correctIndexes.includes(index)
                ? "correct"
                : incorrectIndexes.includes(index)
                ? "incorrect"
                : extraCorrectIndexes.includes(index)
                ? "extra-correct"
                : ""
            }`}
          >
            {letter}
          </span>
        ))}
        {extraIncorrectIndexes.length > 0 &&
          extraIncorrectIndexes.map((index) => (
            <span
              key={`extra-correct-${index}`}
              className="quiz-letter extra-letter"
            >
              .
            </span>
          ))}
      </div>

      <div className="quiz-user-answer">
        {userAnswer.split("").map((letter, index) => (
          <span
            key={index}
            className={`quiz-letter ${
              correctIndexes.includes(index)
                ? "correct"
                : incorrectIndexes.includes(index)
                ? "extra-incorrect"
                : extraIncorrectIndexes.includes(index)
                ? "extra-incorrect"
                : ""
            }`}
          >
            {letter}
          </span>
        ))}
        {extraCorrectIndexes.length > 0 &&
          extraCorrectIndexes.map((index) => (
            <span
              key={`extra-incorrect-${index}`}
              className="quiz-letter extra-letter"
            >
              .
            </span>
          ))}
      </div>
    </div>
  );
};

export default AnswerResult;
