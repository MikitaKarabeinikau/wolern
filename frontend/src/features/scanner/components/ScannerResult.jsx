import React, { useEffect, useState, useCallback } from "react";
import Word from "./Word.jsx";
import { useAuth } from "@clerk/clerk-react";
import "../../../../styles/Exercise.css";
import { prepareWords } from "../../../utils/wordProcessing.js";
import { useScanner } from "../hooks/useScanner.js";
import EditWordVocabulary from "../modes/annotation/AnnotationMode.jsx";
import ReadMode from "../modes/reading/ReadMode.jsx";
import AnnotationMode from "../modes/annotation/AnnotationMode.jsx";
import { useVocabularies } from "../hooks/useVocabularies.js";
function ScannerResult({ text }) {
  const { fetchWordData, words, isLoading, error } = useScanner();
  const {
    getVocabularies,
    error: vocabError,
    isLoading: vocabLoading,
  } = useVocabularies();
  const [vocabularies, setVocabularies] = useState([]);

  useEffect(() => {
    setVocabularies(getVocabularies());
  }, [getVocabularies]);

  const mapByWord = new Map(
    words.map((item) => [item.word.toLowerCase(), item.vocabulary])
  );
  const [mod, setMod] = useState("read");

  const preparedWords = prepareWords(text).map((item) => [
    item,
    mapByWord.get(item.toLowerCase()) || "unknown",
  ]);

  const handleModeChange = useCallback(
    (newMode) => {
      setMod(newMode);
      // Refresh word data when switching to read mode
      if (newMode === "read") {
        fetchWordData();
      }
    },
    [fetchWordData]
  );

  useEffect(() => {
    fetchWordData();
  }, [mod, fetchWordData]);

  return (
    <>
      <div className="scanner-results-container">
        <div className="scanner-output">
          {mod === "edit" && (
            <AnnotationMode
              userWords={mapByWord}
              words={preparedWords}
              text={text}
            />
          )}
          {mod === "read" && <ReadMode userWords={mapByWord} text={text} />}
          {isLoading && <p>Loading scanned words...</p>}
        </div>
        <div className="modes-panel">
          <div className="menu-container">
            <div className="menu-type-selector">
              <button onClick={() => setMod("read")}>
                <strong>Read Mode</strong>
              </button>
              <button onClick={() => setMod("edit")}>
                <strong>Annotation Mode</strong>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ScannerResult;
