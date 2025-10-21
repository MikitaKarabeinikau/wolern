import React, { useState } from 'react';
import '../../styles/QuizAnswerUnit.css';

function QuizAnswerUnit({ hintType, hintInfo, onClick, isFirst}) {
  const [isCollapsed, setIsCollapsed] = useState(isFirst ? false : true);

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className={`answer-unit-container ${isCollapsed ? 'collapsed' : ''} ${isFirst ? 'first-child' : ''}`}
      onClick={toggleCollapse}
    >
      <div className="hint-header">{hintType}</div>
      {!isCollapsed && <div className="hint-body">{hintInfo}</div>}
    </div>
  );
}

export default QuizAnswerUnit;