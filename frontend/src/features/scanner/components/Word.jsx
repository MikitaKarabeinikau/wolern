import React, { useState } from "react";
import { useVocabularies } from "../hooks/useVocabularies.js";

function Word({ word, vocabulary, mod, vocabularies }) {
  const [isHovering, setIsHovering] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [selectedVocabulary, setSelectedVocabulary] = useState(vocabulary);
  const defaultVocabularies = ["new", "learning", "known", "strange"];

  const handleMouseEnter = () => {
    setIsHovering(true);
  };

  const handleMouseLeave = () => {
    setIsHovering(false);
  };

  const handleEdit = () => {
    setShowModal(true);
  };

  const handleVocabularyChange = (e) => {
    const newVocabulary = e.target.value;
    setSelectedVocabulary(newVocabulary);
  };

  const handleConfirm = () => {
    if (onWordSelect) {
      onWordSelect(word, selectedVocabulary);
    }
    setShowModal(false);
  };

  const handleCancel = () => {
    setSelectedVocabulary(vocabulary);
    setShowModal(false);
  };

  return (
    <>
      {mod === "read" && (
        <div className="word-container">
          <div
            className={`word word-${vocabulary}`}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          >
            {word}
          </div>
          <div className={`word-info ${isHovering ? "visible" : "hidden"}`}>
            INFO BLOCK
          </div>
        </div>
      )}

      {mod === "edit" && (
        <div
          className={`word word-${vocabulary}`}
          onClick={handleEdit}
          style={{ cursor: "pointer" }}
        >
          {word}
        </div>
      )}

      {/* Modal for vocabulary selection */}
      {showModal && (
        <div className="modal-overlay" onClick={handleCancel}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h4>Set Vocabulary for "{word}"</h4>
              <button className="modal-close" onClick={handleCancel}>
                ✕
              </button>
            </div>

            <div className="modal-body">
              <label htmlFor="vocabulary-select">Vocabulary Level:</label>
              <select
                id="vocabulary-select"
                value={selectedVocabulary}
                onChange={handleVocabularyChange}
              >
                {vocabularies.length == 0
                  ? defaultVocabularies.map((vocab) => (
                      <option key={vocab} value={vocab}>
                        {vocab}
                      </option>
                    ))
                  : vocabularies.map((vocab) => (
                      <option key={vocab} value={vocab}>
                        {vocab}
                      </option>
                    ))}
              </select>
            </div>

            <div className="modal-footer">
              <button className="btn-cancel" onClick={handleCancel}>
                Cancel
              </button>
              <button className="btn-confirm" onClick={handleConfirm}>
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Word;
