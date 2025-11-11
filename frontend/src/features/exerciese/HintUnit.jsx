import React, { useState } from "react";

const HintUnit = ({ index, hint }) => {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };
  return (
    <div className="hint-unit">
      <div className="hints-list-header" onClick={toggleCollapse}>
        <span>Hint {index + 1}</span>
        <span className="collapse-icon">{isCollapsed}</span>
      </div>
      {!isCollapsed && <div className="hint-content">{hint}</div>}
    </div>
  );
};

export default HintUnit;
