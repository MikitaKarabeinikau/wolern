import React, { useState, useMemo } from "react";
import "../../../../styles/Vocabulary.css";
import VocabularyMenu from "./VocabularyMenu";

const Collapsible = ({
  title,
  wordId,
  children,
  onDelete,
  onChangeVocabulary,
  vocabularies,
  currentSelectedVocabulary,
  onAddVocabulary,
}) => {
  const [vocabulariesArray, setVocabulariesArray] = useState(
    useMemo(() => {
      if (!vocabularies || !Array.isArray(vocabularies)) {
        console.warn("Invalid vocabularies prop:", vocabularies);
        return [];
      }
      return vocabularies;
    }, [vocabularies])
  );

  const [isOpen, setIsOpen] = useState(false);
  const [isVocabularyMenuOpen, setIsVocabularyMenuOpen] = useState(false);
  const [vocabularySelected, setVocabularySelected] = useState(
    currentSelectedVocabulary || ""
  );

  const handleToggle = () => setIsOpen((prev) => !prev);

  const handleDelete = () => {
    console.log(`Delete requested for item ID: ${wordId}`);
    onDelete(wordId);
  };

  const handleChangeVocabulary = (newVocabulary) => {
    console.log(`Change Vocabulary requested for item ID: ${wordId}`);
    console.log("New Vocabulary:", newVocabulary);
    setVocabularySelected(newVocabulary);
    onChangeVocabulary(wordId, newVocabulary);
    setIsVocabularyMenuOpen(false);
  };

  const handleAddVocabulary = (newVocabulary) => {
    if (onAddVocabulary) {
      onAddVocabulary(newVocabulary);
      setVocabulariesArray((prev) => [...prev, newVocabulary]);
      setVocabularySelected(newVocabulary);
      setIsVocabularyMenuOpen(false);
    }
  };

  return (
    <div className="collapsible-container">
      <div className="collapsible-header">
        <div className="collapsible-left" onClick={handleToggle}>
          <h4 className="collapsible-title">{title}</h4>
        </div>
        <div className="collapsible-right">
          <span
            className={`collapsible-icon ${isOpen ? "open" : ""}`}
            onClick={handleToggle}
          >
            ▼
          </span>
          <button onClick={() => setIsVocabularyMenuOpen(true)} className="btn">
            Change Vocabulary
          </button>
          <button onClick={handleDelete} className="btn-delete">
            x
          </button>
        </div>
      </div>

      <div className={`collapsible-content ${isOpen ? "open" : ""}`}>
        <div className="collapsible-content-inner">{children}</div>
      </div>

      {isVocabularyMenuOpen && (
        <VocabularyMenu
          vocabularies={Array.from(vocabularies)}
          vocabularySelected={vocabularySelected}
          onChangeVocabulary={handleChangeVocabulary}
          onAddVocabulary={handleAddVocabulary}
          onCloseMenu={() => setIsVocabularyMenuOpen(false)}
        />
      )}
    </div>
  );
};

export default Collapsible;
