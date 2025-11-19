import React, { useState } from "react";
import "../../../../styles/Scanner.css";
import ScannerResults from "./ScannerResult.jsx";

const TITLE = "Write a text to check new words";
const PLACEHOLDER = "Paste or type your text here...";

function ScannerInput() {
  const [text, setText] = useState("");
  const [isInputed, setIsInputed] = useState(false);

  const handleScan = () => setIsInputed(true);
  const handleNewScan = () => {
    setIsInputed(false);
    setText("");
  };

  return (
    <>
      {!isInputed ? (
        <div className="scanner-container">
          <p className="scanner-title">{TITLE}</p>
          <textarea
            className="scanner-textarea"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={PLACEHOLDER}
          ></textarea>
          <button className="btn" onClick={handleScan}>
            Scan
          </button>
        </div>
      ) : (
        <div>
          <ScannerResults text={text} />
          <button className="scan-btn" onClick={handleNewScan}>
            New Scan
          </button>
        </div>
      )}
    </>
  );
}

export default ScannerInput;
