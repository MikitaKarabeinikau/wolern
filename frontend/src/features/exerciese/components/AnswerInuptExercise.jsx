import React, { useState, useEffect } from "react"; // 1. Import useEffect
import "../../../../styles/Exercise.css";
import HintUnit from "./HintUnit";
// 2. Correct the import name if it's plural
import { calculateIndexes } from "../../../utils/wordProcessing";
import "../../../../styles/QuizAnswerUnit.css";
import AnswerResult from "./AnswerResult";

const AnswerInputExercise = ({ word, exercise }) => {
  // 3. Destructure the correct answer from the exercise prop (assuming it's named 'answer')
  const { question, part_of_speech, explanation, hints, correctAnswer } =
    exercise;
  console.log("Correct Answer", correctAnswer);
  const [isAnswered, setIsAnswered] = useState(false);
  const [userAnswer, setUserAnswer] = useState("");

  // 4. Add state to hold the calculated indexes
  const [correctIndexes, setCorrectIndexes] = useState([]);
  const [incorrectIndexes, setIncorrectIndexes] = useState([]);
  const [extraCorrectIndexes, setExtraCorrectIndexes] = useState([]);
  const [extraIncorrectIndexes, setExtraIncorrectIndexes] = useState([]);

  const handleAnswer = () => {
    // Only mark as answered if the user has typed something
    if (userAnswer.trim()) {
      setIsAnswered(true);
    }
  };

  if (!exercise) {
    return null;
  }

  return (
    <>
      {/* --- Input View (Before Answer) --- */}
      {!isAnswered && (
        <div className="exercise-container two-column">
          {/* --- Left Panel --- */}
          <div className="left-panel">
            <div className="top-section">
              <div className="exercise-header">
                {" "}
                <span className="part-of-speech">{part_of_speech}</span>{" "}
              </div>
            </div>
            <div className="middle-section">
              <p className="question">{question}</p>
            </div>
            <div className="bottom-section">
              <div className="answer-input-wrapper">
                <input
                  type="text"
                  placeholder="Type your answer..."
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleAnswer()}
                />
                <button onClick={handleAnswer}>Check</button>
              </div>
            </div>
          </div>

          {/* --- Right Panel --- */}
          <div className="right-panel">
            <div className="exercise-hints">
              <div className="hints-list">
                {hints.map((hint, index) => (
                  <HintUnit key={index} index={index} hint={hint} />
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* --- Result View (After Answer) --- */}
      {isAnswered && (
        <div className="exercise-container">
          <div className="exercise-content">
            <div className="exercise-header">
              <span className="part-of-speech">{part_of_speech}</span>
              <p className="question">{question}</p>
            </div>
            {/* Pass the correct answer to the AnswerResult component */}
            <AnswerResult word={correctAnswer} userAnswer={userAnswer} />
            <div className="exercise-body">
              <p className="explanation">{explanation}</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default AnswerInputExercise;
