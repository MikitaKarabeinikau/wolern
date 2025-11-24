import React, { useState, useEffect, useTransition } from "react";
import { useVocabularyContext } from "../../contexts/VocabularyContext";
import AddWordContainer from "./components/AddWordForm";
import WordList from "./components/WordList";
import Vocabularies from "./components/Vocabularies";
import "../../../styles/Vocabulary.css";

export function VocabulariesPanel() {
  const { vocabularyData } = useVocabularyContext();
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
    fetchAllData,
  } = vocabularyData;

  const [panelError, setPanelError] = useState(null);
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    if (error) {
      setPanelError(error);
      setTimeout(() => setPanelError(null), 5000);
    }
  }, [error]);

  const handleAddWord = async (newWord) => {
    startTransition(async () => {
      await handleWordAdded(newWord);
      await fetchAllData(); // Refresh data after adding
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
          {isLoading || isPending ? (
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
