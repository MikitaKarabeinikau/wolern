import React, { useState } from "react";
import { useAddWord } from "../hooks/useAnnotations.js";
import VocabularySelectionModal from "./VocabularySelectionModal.jsx";
import WordInfo from "./WordInfo.jsx";

function Word({ word, mod, userWords }) {
  const [isHovering, setIsHovering] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const { addWord, error, isLoading } = useAddWord();
  const vocabulary = userWords[word.toLowerCase()]?.vocabulary || "unknown";

  // Get related info from infoMaps if needed
  const translations = userWords[word.toLowerCase()]?.translations || [];
  const definitions = userWords[word.toLowerCase()]?.definitions || [];
  const examples = userWords[word.toLowerCase()]?.examples || [];

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
        <WordInfo translations={translations} definitions={definitions} />
      </div>
    </div>
  );
}

export default Word;
