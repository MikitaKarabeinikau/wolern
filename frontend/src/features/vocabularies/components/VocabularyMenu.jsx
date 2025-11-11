import React from "react";

const VocabularyMenu = ({
  vocabularies,
  vocabularySelected,
  onChangeVocabulary,
  onAddVocabulary,
  onCloseMenu,
}) => {
  console.log("VocabularyMenu rendered with vocabularies:", vocabularies);

  const handleNewVocabulary = () => {
    const newVocabulary = prompt("Enter new category:");
    if (newVocabulary && newVocabulary.trim()) {
      const trimmedVocabulary = newVocabulary.trim();
      console.log(trimmedVocabulary);
      if (!vocabularies.includes(trimmedVocabulary)) {
        onAddVocabulary(trimmedVocabulary);
        onChangeVocabulary(trimmedVocabulary);
      } else {
        alert("This vocabulary already exists!");
      }
    }
    onCloseMenu();
  };
  return (
    <div className="category-menu-overlay">
      <div className="category-menu-container">
        <div className="category-menu-header">
          <h3>Select Vocabulary</h3>
          <button className="close-menu-btn" onClick={onCloseMenu}>
            X
          </button>
        </div>

        <div className="category-menu-content">
          {vocabularies.length > 0 ? (
            <table className="category-table">
              <thead>
                <tr>
                  <th>Available Vocabularies</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {vocabularies.map((vocabulary) => (
                  <tr
                    key={vocabulary}
                    className={
                      vocabularySelected === vocabulary ? "selected-row" : ""
                    }
                  >
                    <td className="category-name">{vocabulary}</td>
                    <td>
                      <button
                        className="select-category-btn"
                        onClick={() => onChangeVocabulary(vocabulary)}
                      >
                        {vocabularySelected === vocabulary
                          ? "Selected"
                          : "Select"}
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
          <button
            className="add-new-category-btn"
            onClick={handleNewVocabulary}
          >
            + Add New Vocabulary
          </button>
        </div>

        <div className="category-menu-footer">
          <button className="cancel-btn" onClick={onCloseMenu}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default VocabularyMenu;
