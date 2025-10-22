import React from "react";
import '../../styles/QuizAnswerUnit.css';

function QuizAnswerField({onCheckAnswer}) {
  const [inputValue, setInputValue] = React.useState("");

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleAnswer();
    }
  };

  const handleAnswer = () => {
    // Here you can add logic to check the answer if needed
    onCheckAnswer(inputValue);
    setInputValue(""); // Clear input after submitting
  };

  return (
    <div className="quiz-answer-field">
        <input 
        type="text" 
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Type your answer here" 
        onKeyDown={handleKeyDown}
        />
        <button onClick={handleAnswer}>Submit</button>
    </div>
  )
}

export default QuizAnswerField;