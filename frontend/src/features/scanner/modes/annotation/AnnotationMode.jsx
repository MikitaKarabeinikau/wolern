import React from "react";
import { useState } from "react";
import { apiClient } from "../../../../api/apiClient";
import { useAddWord } from "../../hooks/useAnnotations.js";

export default function AnnotationMode({ userWords, words }) {
  const [annotationMode, setAnnotationMode] = useState("fulltext");
  const { addWord, error, isLoading } = useAddWord();
  const unknownWords = words.filter(
    ([word, vocabulary]) => vocabulary === "unknown"
  );
  console.log("Unknown words:", unknownWords);

  const [currentWordIndex, setCurrentWordIndex] = useState(0);

  const handleAnnotationWord = (vocabulary) => {
    const word = unknownWords[currentWordIndex][0];
    addWord(word, vocabulary, () => {
      // On success, move to the next word
      setCurrentWordIndex((prevIndex) =>
        prevIndex + 1 < unknownWords.length ? prevIndex + 1 : prevIndex
      );
    });
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
            {isLoading ? (
              <div className="carousele-annotation-word">Loading data ...</div>
            ) : (
              <div className="carousele-annotation-word">
                {unknownWords[currentWordIndex][0]}
              </div>
            )}
            <div className="carousele-annotation-controls">
              <button
                disabled={isLoading}
                className="annotation-button"
                onClick={() => handleAnnotationWord("known")}
              >
                Yes
              </button>
              <button
                disabled={isLoading}
                className="annotation-button"
                onClick={() => handleAnnotationWord("new")}
              >
                No
              </button>
              <button
                disabled={isLoading}
                className="annotation-button"
                onClick={() =>
                  setCurrentWordIndex((prevIndex) =>
                    prevIndex + 1 < unknownWords.length
                      ? prevIndex + 1
                      : prevIndex
                  )
                }
              >
                Skip
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
