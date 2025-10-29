import React, { useState } from "react";
import "../../styles/Word.css";

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
  const [vocabulariesSet, setVocabulariesSet] = useState(new Set(vocabularies || []));
  const [isOpen, setIsOpen] = useState(false);
  const [isVocabularyMenuOpen, setIsVocabularyMenuOpen] = useState(false);
  const [vocabularySelected, setVocabularySelected] = useState(currentSelectedVocabulary || "");
  const vocabulariesArray = Array.isArray(vocabularies) ? vocabularies : Array.from(vocabularies);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleDelete = () => {
    console.log(`Delete requested for item ID: ${wordId}`);
    onDelete(wordId);
  };

  const handleOpenVocabularyMenu = () => {
    setIsVocabularyMenuOpen(true);
  };

  const handleToggleVocabularyMenu = () => {
    setIsVocabularyMenuOpen(!isVocabularyMenuOpen);
  };

  const handleCloseVocabularyMenu = () => {
    setIsVocabularyMenuOpen(false);
  };

  const handleChangeVocabulary = (newVocabulary) => {
    console.log(`Change Vocabulary requested for item ID: ${wordId}`);
    setVocabularySelected(newVocabulary);
    onChangeVocabulary(wordId, newVocabulary);
    setIsVocabularyMenuOpen(false);
  };

  const handleNewVocabulary = () => {
    const newVocabulary = prompt("Enter new category:");
    if (newVocabulary && newVocabulary.trim()) {
      const trimmedVocabulary = newVocabulary.trim();
      if (!vocabulariesSet.has(trimmedVocabulary)) {
        const updatedSet = new Set([...vocabulariesSet, trimmedVocabulary]);
        setVocabulariesSet(updatedSet);
        setVocabularySelected(trimmedVocabulary);
        onChangeVocabulary(wordId, trimmedVocabulary);
        if (onAddVocabulary) {
          onAddVocabulary(trimmedVocabulary);
        }
      }
    }
    setIsVocabularyMenuOpen(false);
  };

 return (
  <div className="collapsible-container">
    <div className="collapsible-header">
      {/* Word on the left */}
      <div className="collapsible-left" onClick={handleToggle}>
        <h4 className="collapsible-title">{title}</h4>
      </div>
      {/* Buttons and triangle on the right */}
      <div className="collapsible-right">
        <span className={`collapsible-icon ${isOpen ? "open" : ""}`} onClick={handleToggle}>
          ▼
        </span>
        <button onClick={handleOpenVocabularyMenu} className="btn">
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
      <div className="category-menu-overlay">
        <div className="category-menu-container">
          <div className="category-menu-header">
            <h3>Select Vocabulary</h3>
            <button className="close-menu-btn" onClick={handleCloseVocabularyMenu}>
              X
            </button>
          </div>

          <div className="category-menu-content">
            {vocabulariesArray.length > 0 ? (
              <table className="category-table">
                <thead>
                  <tr>
                    <th>Available Vocabularies</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {vocabulariesArray.map((vocabulary) => (
                    <tr
                      key={vocabulary}
                      className={vocabularySelected === vocabulary ? "selected-row" : ""}
                    >
                      <td className="category-name">{vocabulary}</td>
                      <td>
                        <button
                          className="select-category-btn"
                          onClick={() => handleChangeVocabulary(vocabulary)}
                        >
                          {vocabularySelected === vocabulary ? "Selected" : "Select"}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="no-categories">No Vocabularies available</p>
            )}
          </div>

          <div className="add-new-category-section">
            <button className="add-new-category-btn" onClick={handleNewVocabulary}>
              + Add New Vocabulary
            </button>
          </div>

          <div className="category-menu-footer">
            <button className="cancel-btn" onClick={handleCloseVocabularyMenu}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    )}
  </div>
);
};

export default Collapsible;