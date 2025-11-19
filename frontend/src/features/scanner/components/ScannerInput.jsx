import React, { useState } from "react";
import "../../../../styles/Scanner.css";

import ScannerResults from "./ScannerResult.jsx";

function ScannerInput() {
  const [text, setText] = useState("");
  const [isInputed, setIsInputed] = useState(false);
  return (
    <>
      {!isInputed && (
        <div className="scanner-container">
          <p className="scanner-title">Writte a text to check new words</p>
          <textarea
            className="scanner-textarea"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste or type your text here..."
          ></textarea>
          <button
            className="btn"
            onClick={() => {
              setText(text);
              setIsInputed(true);
            }}
          >
            Scan
          </button>
        </div>
      )}
      {isInputed && (
        <>
          <div>
            <ScannerResults text={text} />
            <button
              className="scan-btn"
              onClick={() => {
                setIsInputed(false);
                setText("");
              }}
            >
              New Scan
            </button>
          </div>
        </>
      )}
    </>
  );
}

export default ScannerInput;
