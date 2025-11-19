import React, { useState, useEffect } from "react";

const DEFAULT_VOCABULARIES = ["new", "learning", "known", "strange"];

function VocabularySelectionModal({
  isOpen,
  onClose,
  onConfirm,
  word,
  initialVocabulary,
  vocabularies,
}) {
  const [selectedVocabulary, setSelectedVocabulary] =
    useState(initialVocabulary);

  useEffect(() => {
    setSelectedVocabulary(initialVocabulary);
  }, [initialVocabulary, isOpen]);

  if (!isOpen) {
    return null;
  }

  const handleConfirm = () => {
    onConfirm(selectedVocabulary);
  };

  const vocabularyOptions =
    vocabularies && vocabularies.length > 0
      ? vocabularies
      : DEFAULT_VOCABULARIES;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h4>Set Vocabulary for "{word}"</h4>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>
        <div className="modal-body">
          <label htmlFor="vocabulary-select">Vocabulary Level:</label>
          <select
            id="vocabulary-select"
            value={selectedVocabulary}
            onChange={(e) => setSelectedVocabulary(e.target.value)}
          >
            {vocabularyOptions.map((vocab) => (
              <option key={vocab} value={vocab}>
                {vocab}
              </option>
            ))}
          </select>
        </div>
        <div className="modal-footer">
          <button className="btn-cancel" onClick={onClose}>
            Cancel
          </button>
          <button className="btn-confirm" onClick={handleConfirm}>
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}

export default VocabularySelectionModal;
