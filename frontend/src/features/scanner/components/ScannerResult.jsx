import React, { useEffect, useState, useCallback, useMemo } from "react";
import "../../../../styles/Exercise.css";
import { prepareWords } from "../../../utils/wordProcessing.js";
import { useVocabularies } from "../../vocabularies/hooks/useVocabularies";
import AnnotationMode from "../modes/annotation/AnnotationMode.jsx";
import ReadMode from "../modes/reading/ReadMode.jsx";
import { useScannerVocabularies } from "../hooks/useScannerVocabularies.js";
import { transformToWordData } from "../../../utils/wordProcessing.js";

function ScannerResult({ text }) {
  const { vocabularyData, mappedVocabulary } = useVocabularyContext();
  const {
    isLoading,
    error,
    words,
    infoMaps,
    selectedVocabulary,
    handleVocabularySelect,
    handleWordAdded,
    fetchAllData,
  } = vocabularyData;
  const {
    getVocabularies,
    vocabularies,
    error: vocabError,
    isLoading: vocabLoading,
  } = useScannerVocabularies();

  const [mod, setMod] = useState("read");

  // Prepare words with their vocabulary status
  const preparedWords = useMemo(
    () =>
      prepareWords(text).map((item) => [
        item,
        mappedVocabulary[item.toLowerCase()] === undefined
          ? "unknown"
          : mappedVocabulary[item.toLowerCase()].vocabulary,
      ]),
    [text, mappedVocabulary]
  );

  const handleModeChange = useCallback(
    (newMode) => {
      setMod(newMode);
      if (newMode === "read") {
        fetchAllData();
      }
    },
    [fetchAllData]
  );

  // Fetch word data on mount
  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  // Fetch vocabularies on mount
  useEffect(() => {
    getVocabularies();
  }, [getVocabularies]);

  const isAnyLoading = isLoading || vocabLoading;

  return (
    <div className="scanner-results-container">
      <div className="scanner-output">
        {isAnyLoading ? (
          <p>Loading scanned words...</p>
        ) : mod === "edit" ? (
          <AnnotationMode
            userWords={mappedVocabulary}
            words={preparedWords}
            vocabularies={vocabularies}
          />
        ) : (
          <ReadMode
            userWords={mappedVocabulary}
            words={preparedWords}
            text={text}
          />
        )}

        {error && <p className="error-message">{error}</p>}
        {vocabError && <p className="error-message">{vocabError}</p>}
      </div>

      <div className="modes-panel">
        <div className="menu-container">
          <div className="menu-type-selector">
            <button
              className={mod === "read" ? "active" : ""}
              onClick={() => handleModeChange("read")}
            >
              <strong>Read Mode</strong>
            </button>
            <button
              className={mod === "edit" ? "active" : ""}
              onClick={() => handleModeChange("edit")}
            >
              <strong>Annotation Mode</strong>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ScannerResult;
