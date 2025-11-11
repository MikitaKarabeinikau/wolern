import React from "react";
import "../../../../styles/QuizAnswerUnit.css";
import "../../../../styles/Vocabulary.css";

function QuizAnswerField({ onCheckAnswer }) {
  const [inputValue, setInputValue] = React.useState("");

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleAnswer();
    }
  };

  const handleAnswer = () => {
    // Here you can add logic to check the answer if needed
    onCheckAnswer(inputValue);
    setInputValue(""); // Clear input after submitting
  };

  return (
    <div className="add-container">
      <div className="input">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your answer here"
          onKeyDown={handleKeyDown}
          className="field"
        />
        <button onClick={handleAnswer} className="btn">
          Submit
        </button>
      </div>
    </div>
  );
}

export default QuizAnswerField;
