import React, { useState } from "react";
import { useAddWord } from "../../hooks/useAnnotations.js";
import FullTextAnnotation from "./FullTextAnnotation.jsx";
import CarouselAnnotation from "./CarouselAnnotation.jsx";

const ANNOTATION_MODES = {
  FULL_TEXT: "fulltext",
  CAROUSEL: "carousel",
};

export default function AnnotationMode({
  userWords,
  words,
  text,
  vocabularies,
}) {
  const [annotationMode, setAnnotationMode] = useState(
    ANNOTATION_MODES.FULL_TEXT
  );
  const { addWord, error, isLoading } = useAddWord();
  const unknownWords = words.filter(
    ([, vocabulary]) => vocabulary === "unknown"
  );

  return (
    <>
      <div className="annotation-mode-container">
        <div className="annotation-mode-bar">
          <button
            className="annotation-button"
            onClick={() => setAnnotationMode(ANNOTATION_MODES.FULL_TEXT)}
          >
            Full Text
          </button>
          <button
            className="annotation-button"
            onClick={() => setAnnotationMode(ANNOTATION_MODES.CAROUSEL)}
          >
            Carousel
          </button>
        </div>
        {error && <div className="error-message">Error: {error}</div>}
        <div className="annotation-mode-content">
          {annotationMode === ANNOTATION_MODES.FULL_TEXT && (
            <FullTextAnnotation
              text={text}
              userWords={userWords}
              vocabularies={vocabularies}
            />
          )}
          {annotationMode === ANNOTATION_MODES.CAROUSEL && (
            <CarouselAnnotation
              unknownWords={unknownWords}
              onAnnotate={addWord}
              isLoading={isLoading}
            />
          )}
        </div>
      </div>
    </>
  );
}
