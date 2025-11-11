import React from "react";
import { useVocabularies } from "./hooks/useVocabularies";
import AddWordContainer from "./components/AddWordForm";
import WordList from "./components/WordList";
import Vocabularies from "./components/Vocabularies";
import "../../../styles/Vocabulary.css";
import { useState, useEffect } from "react";

export function VocabulariesPanel() {
  const {
    isLoading,
    error,
    words,
    vocabularies,
    infoMaps,
    selectedVocabulary,
    handleVocabularySelect,
    handleWordAdded,
    getToken,
  } = useVocabularies();
  const [panelError, setPanelError] = useState(null);

  useEffect(() => {
    if (error) {
      setPanelError(error);
      setTimeout(() => setPanelError(null), 5000);
    }
  }, [error]);
  return (
    <div>
      <div className="notification-container">
        {panelError && (
          <div className="error-notification">
            <span>⚠️ {panelError}</span>
            <button
              className="close-button"
              onClick={() => setPanelError(null)}
            >
              ✕
            </button>
          </div>
        )}
      </div>
      <div className="add-word-container">
        <div className="left-panel">
          <Vocabularies
            vocabularies={vocabularies}
            onVocabularySelect={handleVocabularySelect}
          />
        </div>
        <div className="middle-panel">
          <AddWordContainer onWordAdded={handleWordAdded} />
        </div>
        <div className="right-panel">
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <WordList
              selectedVocabulary={selectedVocabulary}
              words={words} // Pass the already filtered words
              {...infoMaps} // Spread all the map props
              onDataChange={handleWordAdded}
              getToken={getToken}
              vocabularies={vocabularies}
            />
          )}
        </div>
      </div>
    </div>
  );
}
