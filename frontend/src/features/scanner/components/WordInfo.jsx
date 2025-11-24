import React from "react";
import { groupDataByCategory } from "../../../utils/wordProcessing";
import "../../../../styles/Scanner.css";

function WordInfo({ translations, definitions }) {
  const groupedTranslations = groupDataByCategory(translations, "language");
  const groupedDefinitions = groupDataByCategory(definitions, "part_of_speech");

  return (
    <div>
      <div className="word-info-section">
        <h4>Translations</h4>
        {Object.entries(groupedTranslations).map(([language, items]) => (
          <div key={language}>
            <strong>{language}:</strong>{" "}
            {items.map((item) => item.translation).join(", ")}
          </div>
        ))}
      </div>
      <div className="word-info-section">
        <h4>Definitions</h4>
        {Object.entries(groupedDefinitions).map(([partOfSpeech, items]) => (
          <div key={partOfSpeech}>
            <strong>{partOfSpeech}:</strong>{" "}
            {items.map((item) => item.definition).join("; ")}
          </div>
        ))}
      </div>
    </div>
  );
}

export default WordInfo;
