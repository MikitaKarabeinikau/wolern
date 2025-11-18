import React, { useState } from "react";

function Word({ word, vocabulary }) {
  const [isHovering, setIsHovering] = useState(false);

  const handleMouseEnter = () => {
    setIsHovering(true);
  };

  const handleMouseLeave = () => {
    setIsHovering(false);
  };

  return (
    <div className="word-container">
      <div
        className={`word word-${vocabulary}`}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {word}
      </div>
      <div className={`word-info ${isHovering ? "visible" : "hidden"}`}>
        INFO BLOCK afadsfasdf
      </div>
    </div>
  );
}

export default Word;
