import React from "react";
import "../../../../styles/Vocabulary.css";

function Vocabularies({ vocabularies, onVocabularySelect }) {
  if (!vocabularies || vocabularies.length === 0) {
    return (
      <p className="no-vocabularies-message">No vocabularies available.</p>
    );
  }

  return (
    <ul className="vocabularies-list">
      {vocabularies.map((vocab, index) => (
        <li key={vocab}>
          <div
            className="collapsible-vocabulary"
            onClick={() => onVocabularySelect(vocab)}
          >
            <div className="collapsible-vocabulary-header">{vocab}</div>
          </div>
        </li>
      ))}
    </ul>
  );
}

export default Vocabularies;
