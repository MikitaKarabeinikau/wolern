import React, { useEffect, useState } from "react";
import Word from "./Word.jsx";
import { useAuth } from "@clerk/clerk-react";
import "../../../../styles/Exercise.css";
import { prepareWords } from "../../../utils/wordProcessing.js";
import { useScanner } from "../hooks/useScanner.js";
// TODO: 1. Symbols should be shown without changes.

function ScannerResult({ text }) {
  const { getToken } = useAuth();
  const { fetchWordData, words, isLoading, error } = useScanner();
  console.log("ScannerResult words:", words);
  useEffect(() => {
    fetchWordData();
    console.log("Fetched words:", words);
  }, [fetchWordData]);
  const mapByWord = new Map(words.map((item) => [item.word, item.vocabulary]));
  console.log("Map by word:", mapByWord.get("example") === undefined); // Example usage
  return (
    <>
      <div className="scanner-results-container">
        <div className="scanner-output">
          {isLoading && <p>Loading scanned words...</p>}
          {prepareWords(text).map((word, index) => (
            <Word
              key={index}
              word={word}
              vocabulary={
                mapByWord.get(word) === undefined ? "new" : mapByWord.get(word)
              }
            />
          ))}
        </div>
        <div className="modes-panel">
          <div className="menu-container">
            <div className="menu-type-selector">
              <button class className>
                <strong>Read Mode</strong>
              </button>
              <button>
                <strong>Edit Mode</strong>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ScannerResult;
