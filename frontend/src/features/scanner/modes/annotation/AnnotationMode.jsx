import React, { useState } from "react";
import { useAddWord } from "../../hooks/useAnnotations.js";
import Annotation from "./Annotation.jsx";

export default function AnnotationMode({ userWords, words, vocabularies }) {
  const { addWord, error, isLoading } = useAddWord();
  const unknownWords = words.filter(
    ([, vocabulary]) => vocabulary === "unknown"
  );

  return (
    <>
      <div className="annotation-mode-container">
        {error && <div className="error-message">Error: {error}</div>}
        <div className="annotation-mode-content">
          <Annotation
            unknownWords={unknownWords}
            onAnnotate={addWord}
            isLoading={isLoading}
          />
        </div>
      </div>
    </>
  );
}
