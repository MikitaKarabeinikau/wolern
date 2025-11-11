import React, { useMemo } from "react";
import Word from "./Word";
import { processWords } from "../../../utils/wordProcessing";

function WordList({
  selectedVocabulary,
  words,
  translationsMap,
  definitionsMap,
  examplesMap,
  synonymsMap,
  warningsMap,
  tagsMap,
  onDataChange,
  getToken,
  vocabularies,
}) {
  // Memoize the processed word data to avoid recalculating on every render
  const processedWords = useMemo(
    () =>
      processWords(words, {
        translationsMap,
        definitionsMap,
        examplesMap,
        synonymsMap,
        warningsMap,
        tagsMap,
      }),
    [
      words,
      translationsMap,
      definitionsMap,
      examplesMap,
      synonymsMap,
      warningsMap,
      tagsMap,
    ]
  );

  if (!processedWords || processedWords.length === 0) {
    return (
      <div>
        <h2>Word List</h2>
        <p>No words to display.</p>
      </div>
    );
  }

  return (
    <div>
      <h2>{selectedVocabulary || "Vocabulary"}</h2>
      {processedWords.map((wordObj) => (
        <Word
          key={wordObj.id}
          wordData={wordObj}
          translations={wordObj.translations}
          definitions={wordObj.definitions}
          examples={wordObj.examples}
          synonyms={wordObj.synonyms}
          warnings={wordObj.warnings}
          tags={wordObj.tags}
          onDataChange={onDataChange}
          getToken={getToken}
          vocabularies={vocabularies}
        />
      ))}
    </div>
  );
}

export default WordList;
