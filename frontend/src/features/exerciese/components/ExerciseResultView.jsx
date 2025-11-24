import React from "react";
import AnswerResult from "./AnswerResult";

function ExerciseResultView({
  partOfSpeech,
  question,
  word,
  userAnswer,
  explanation,
}) {
  return (
    <div className="exercise-content">
      <div className="exercise-header">
        <span className="part-of-speech">{partOfSpeech}</span>
        <p className="question">{question}</p>
      </div>
      <AnswerResult word={word} userAnswer={userAnswer} />
      <div className="exercise-body">
        <p className="explanation">{explanation}</p>
      </div>
    </div>
  );
}
export default ExerciseResultView;
