// filepath: /home/scb/wolern/frontend/src/vocabularies/Vocabularies.jsx
import React from "react";
import CollapsibleVocabulary from "./CollapsibleVocabulary";

function Vocabularies({ vocabularies, onVocabularySelect }) {
  return (
    <div>
      {vocabularies.length === 0 ? (
        <p>No vocabularies available.</p>
      ) : (
        <ul>
          {vocabularies.map((vocab, index) => (
            <li key={index}>
              <CollapsibleVocabulary
                title={vocab}
                onClick={() => {
                  console.log("Vocabulary clicked:", vocab); // Add this line
                  onVocabularySelect(vocab);
                }} // Call onVocabularySelect
              />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Vocabularies;