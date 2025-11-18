import React, { useEffect, useState } from "react";
import Word from "./Word.jsx";
import { useAuth } from "@clerk/clerk-react";
import "../../../../styles/Exercise.css";
import { prepareWords } from "../../../utils/wordProcessing.js";
import { useScanner } from "../hooks/useScanner.js";
import EditWordVocabulary from "../modes/annotation/AnnotationMode.jsx";
import ReadMode from "../modes/reading/ReadMode.jsx";
import AnnotationMode from "../modes/annotation/AnnotationMode.jsx";

function ScannerResult({ text }) {
  const { getToken } = useAuth();
  const { fetchWordData, words, isLoading, error } = useScanner();
  const mapByWord = new Map(words.map((item) => [item.word, item.vocabulary]));
  const [mod, setMod] = useState("read");
  const preparedWords = prepareWords(text).map((item) => [
    item,
    mapByWord.get(item) || "unknown",
  ]);

  useEffect(() => {
    fetchWordData();
    console.log("Fetched words:", words);
  }, [fetchWordData]);

  return (
    <>
      <div className="scanner-results-container">
        <div className="scanner-output">
          {mod === "edit" && (
            <AnnotationMode userWords={words} words={preparedWords} />
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
