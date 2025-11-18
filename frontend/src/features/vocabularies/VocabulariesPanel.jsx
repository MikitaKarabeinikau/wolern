import React, { useState, useEffect, useTransition } from "react";
import { useVocabularies } from "./hooks/useVocabularies";
import AddWordContainer from "./components/AddWordForm";
import WordList from "./components/WordList";
import Vocabularies from "./components/Vocabularies";
import "../../../styles/Vocabulary.css";

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
  const [isPending, startTransition] = useTransition(); // Add useTransition hook

  useEffect(() => {
    if (error) {
      setPanelError(error);
      setTimeout(() => setPanelError(null), 5000);
    }
  }, [error]);

  const handleAddWord = (newWord) => {
    startTransition(() => {
      handleWordAdded(newWord); // Defer rendering updates
    });
  };

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
          <AddWordContainer onWordAdded={handleAddWord} />
        </div>
        <div className="right-panel">
          {isLoading || isPending ? ( // Show loading state during transition
            <p>Loading...</p>
          ) : (
            <WordList
              selectedVocabulary={selectedVocabulary}
              words={words}
              {...infoMaps}
              onDataChange={handleAddWord}
              getToken={getToken}
              vocabularies={vocabularies}
            />
          )}
        </div>
      </div>
    </div>
  );
}
