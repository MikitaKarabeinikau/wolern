import React from "react";
import "../../../../styles/QuizAnswerUnit.css";
import "../../../../styles/Vocabulary.css";

function QuizAnswerField({ onCheckAnswer }) {
  const [inputValue, setInputValue] = React.useState("");

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent the default form submission which reloads the page
    if (!inputValue.trim()) return; // Do not submit if the input is empty

    onCheckAnswer(inputValue);
    setInputValue(""); // Clear input after submitting
  };

  return (
    <form className="add-container" onSubmit={handleSubmit}>
      <div className="input">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your answer here"
          className="field"
        />
        <button type="submit" className="btn" disabled={!inputValue.trim()}>
          Submit
        </button>
      </div>
    </form>
  );
}

export default QuizAnswerField;
