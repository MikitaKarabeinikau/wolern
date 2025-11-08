import React from "react";
import "../../styles/QuizAnswerUnit.css";
import HintUnit from "./HintUnit";

function Exercise({ data }) {
  return (
    <>
      <div className="exercise-container">
        <div className="exercise-content">
          <div className="exercise-header"></div>
          <div className="exercise-body"></div>
        </div>
        <div className="exercise-hints">
          {data.hints.map((hint, index) => (
            <div key={index} className="exercise-hint">
              <HintUnit hint={hint} />
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default Exercise;
