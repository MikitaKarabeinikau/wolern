import React, { useState } from "react";
import "../../../../../styles/Scanner.css";

function Annotation({ unknownWords, onAnnotate, isLoading }) {
  const [currentWordIndex, setCurrentWordIndex] = useState(0);

  const advanceToNextWord = () => {
    setCurrentWordIndex((prevIndex) =>
      prevIndex + 1 < unknownWords.length ? prevIndex + 1 : prevIndex
    );
  };

  const handleAnnotation = (vocabulary) => {
    const word = unknownWords[currentWordIndex][0];
    onAnnotate(word, vocabulary, advanceToNextWord);
  };

  if (unknownWords.length === 0 || currentWordIndex >= unknownWords.length) {
    return (
      <div className="carousele-annotation-word">
        No more unknown words to annotate.
      </div>
    );
  }

  return (
    <div>
      <div className="carousele-annotation-question">
        Do you know this word?
      </div>
      {isLoading ? (
        <div className="carousele-annotation-word">Loading...</div>
      ) : (
        <div className="carousele-annotation-word">
          {unknownWords[currentWordIndex][0]}
        </div>
      )}
      <div className="carousele-annotation-controls">
        <button
          disabled={isLoading}
          className="annotation-button"
          onClick={() => handleAnnotation("known")}
        >
          Yes
        </button>
        <button
          disabled={isLoading}
          className="annotation-button"
          onClick={() => handleAnnotation("new")}
        >
          No
        </button>
        <button
          disabled={isLoading}
          className="annotation-button"
          onClick={advanceToNextWord}
        >
          Skip
        </button>
      </div>
    </div>
  );
}
export default Annotation;
