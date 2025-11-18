import React from "react";
import { useState } from "react";
import { apiClient } from "../../../../api/apiClient";

export default function AnnotationMode({ userWords, words }) {
  const [annotationMode, setAnnotationMode] = useState("fulltext");
  console.log("AnnotationMode:", words);

  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const handleChange = (e) => {
    setVocabulary(e.target.value);
  };

  const handleSave = () => {
    onSave(word, vocabulary);
  };

  return (
    <div className="annotation-mode-container">
      <div className="annotation-mode-bar">
        <button
          className="annotation-button"
          onClick={() => setAnnotationMode("fulltext")}
        >
          Full Text
        </button>
        <button
          className="annotation-button"
          onClick={() => setAnnotationMode("carousele")}
        >
          Carousele
        </button>
      </div>
      <div className="annotation-mode-content">
        {annotationMode === "fulltext" && (
          <div className="fulltext-annotation"></div>
        )}
        {annotationMode === "carousele" && (
          <div>
            <div className="carousele-annotation-question">
              Do you know this word?
            </div>
            <div className="carousele-annotation-word">
              {words[currentWordIndex][0]}
            </div>
            <div className="carousele-annotation-controls">
              <button className="annotation-button">Yes</button>
              <button className="annotation-button">No</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
