import React, { useState } from "react";

const HintUnit = ({ hint }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };
  return (
    <div className={`hint-unit ${isCollapsed ? "collapsed" : ""}`}>
      <h4 onClick={toggleCollapse}>{hint}</h4>
      <p>{isCollapsed ? null : hint}</p>
    </div>
  );
};

export default HintUnit;
