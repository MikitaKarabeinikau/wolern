import React, { useState } from "react";
import { useAddWord } from "../hooks/useAnnotations.js";
import VocabularySelectionModal from "./VocabularySelectionModal.jsx";

function Word({ word, vocabulary, mod, vocabularies }) {
  const [isHovering, setIsHovering] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const { addWord, error, isLoading } = useAddWord();

  const handleConfirm = (newVocabulary) => {
    addWord(word, newVocabulary);
    setShowModal(false);
  };

  if (mod === "edit") {
    return (
      <>
        <div
          className={`word word-${vocabulary}`}
          onClick={() => setShowModal(true)}
          style={{ cursor: "pointer" }}
        >
          {word}
        </div>
        <VocabularySelectionModal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          onConfirm={handleConfirm}
          word={word}
          initialVocabulary={vocabulary}
          vocabularies={vocabularies}
        />
      </>
    );
  }

  // Default to "read" mode
  return (
    <div className="word-container">
      <div
        className={`word word-${vocabulary}`}
        onMouseEnter={() => setIsHovering(true)}
        onMouseLeave={() => setIsHovering(false)}
      >
        {word}
      </div>
      <div className={`word-info ${isHovering ? "visible" : "hidden"}`}>
        INFO BLOCK
      </div>
    </div>
  );
}

export default Word;
