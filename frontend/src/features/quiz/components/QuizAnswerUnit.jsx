import React, { useState } from "react";
import "../../../../styles/QuizAnswerUnit.css";

// Renamed component for clarity, as it displays hints, not answers.
function HintUnit({ hintType, hintInfo, onClick, isFirst }) {
  // Simplified initial state logic. The first hint is not collapsed.
  const [isCollapsed, setIsCollapsed] = useState(!isFirst);

  const toggleCollapse = () => {
    setIsCollapsed((prev) => !prev);
    // Execute the parent's onClick handler if it was provided.
    if (onClick) {
      onClick();
    }
  };

  return (
    <div
      className={`answer-unit-container ${isCollapsed ? "collapsed" : ""} ${
        isFirst ? "first-child" : ""
      }`}
      onClick={toggleCollapse}
    >
      <div className="hint-header">{hintType}</div>
      {!isCollapsed && <div className="hint-body">{hintInfo}</div>}
    </div>
  );
}

export default HintUnit;
