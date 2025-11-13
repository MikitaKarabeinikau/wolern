import React, { useEffect } from "react";
import { calculateIndexes } from "../../../utils/wordProcessing";
import "../../../../styles/QuizAnswerUnit.css";

const AnswerResult = ({ word, userAnswer }) => {
  if (word === undefined || word === null) {
    return null;
  }
  const [correctIndexes, setCorrectIndexes] = React.useState([]);
  const [incorrectIndexes, setIncorrectIndexes] = React.useState([]);
  const [extraCorrectIndexes, setExtraCorrectIndexes] = React.useState([]);
  const [extraIncorrectIndexes, setExtraIncorrectIndexes] = React.useState([]);

  useEffect(() => {
    if (!userAnswer) return;

    const { correct, incorrect, extraCorrect, extraIncorrect } =
      calculateIndexes(word, userAnswer);

    setCorrectIndexes(correct);
    setIncorrectIndexes(incorrect);
    setExtraCorrectIndexes(extraCorrect);
    setExtraIncorrectIndexes(extraIncorrect);
  }, [word, userAnswer]);

  return (
    <div>
      <div className="quiz-answers-container">
        <div className="quiz-correct-answer">
          {/* 6. Use the correct variable for the answer */}
          {(userAnswer || "").split("").map((l, index) => (
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
              {l}
            </span>
          ))}
        </div>
        <div className="quiz-user-answer">
          {(userAnswer || "").split("").map((l, index) => (
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
              {l}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnswerResult;
