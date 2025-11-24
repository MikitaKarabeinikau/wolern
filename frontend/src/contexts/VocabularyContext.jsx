import React, { createContext, useContext } from "react";
import { useVocabularies } from "../features/vocabularies/hooks/useVocabularies";
import { processWords, transformToWordData } from "../utils/wordProcessing";

const VocabularyContext = createContext(null);

export const VocabularyProvider = ({ children }) => {
  const vocabularyData = useVocabularies();
  const words = Object.values(vocabularyData.words || {});
  const maps = vocabularyData.infoMaps || {};
  const processedWords = processWords(words, maps);
  const mappedVocabulary = transformToWordData(processedWords);

  return (
    <VocabularyContext.Provider value={{ vocabularyData, mappedVocabulary }}>
      {children}
    </VocabularyContext.Provider>
  );
};

export const useVocabularyContext = () => {
  const context = useContext(VocabularyContext);
  if (!context) {
    throw new Error(
      "useVocabularyContext must be used within VocabularyProvider"
    );
  }
  return context;
};
