import React, { useEffect, useState, useCallback, useMemo } from "react";
import { useAuth } from "@clerk/clerk-react";
import "../../../../styles/Exercise.css";
import { prepareWords } from "../../../utils/wordProcessing.js";
import { useScanner } from "../hooks/useScanner.js";
import AnnotationMode from "../modes/annotation/AnnotationMode.jsx";
import ReadMode from "../modes/reading/ReadMode.jsx";
import { useVocabularies } from "../hooks/useVocabularies.js";

function ScannerResult({ text }) {
  const { fetchWordData, words, isLoading, error } = useScanner();
  const {
    getVocabularies,
    vocabularies,
    error: vocabError,
    isLoading: vocabLoading,
  } = useVocabularies();
  const [mod, setMod] = useState("read");

  const mapByWord = useMemo(
    () =>
      new Map(words.map((item) => [item.word.toLowerCase(), item.vocabulary])),
    [words]
  );

  const preparedWords = useMemo(
    () =>
      prepareWords(text).map((item) => [
        item,
        mapByWord.get(item.toLowerCase()) || "unknown",
      ]),
    [text, mapByWord]
  );

  const handleModeChange = useCallback(
    (newMode) => {
      setMod(newMode);
      if (newMode === "read") {
        fetchWordData();
      }
    },
    [fetchWordData]
  );

  useEffect(() => {
    fetchWordData();
  }, [fetchWordData]);

  useEffect(() => {
    getVocabularies();
  }, [getVocabularies]);

  return (
    <>
      <div className="scanner-results-container">
        <div className="scanner-output">
          {mod === "edit" && (
            <AnnotationMode
              userWords={mapByWord}
              words={preparedWords}
              text={text}
              vocabularies={vocabularies}
            />
          )}
          {mod === "read" && <ReadMode userWords={mapByWord} text={text} />}
          {isLoading && <p>Loading scanned words...</p>}
        </div>
        <div className="modes-panel">
          <div className="menu-container">
            <div className="menu-type-selector">
              <button onClick={() => handleModeChange("read")}>
                <strong>Read Mode</strong>
              </button>
              <button onClick={() => handleModeChange("edit")}>
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
