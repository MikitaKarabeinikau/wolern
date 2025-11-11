import React, { useState } from "react";
import { useAddWord } from "../hooks/useAddWord";
import "../../../../styles/Vocabulary.css";

function AddWordForm({ onWordAdded }) {
  const [inputValue, setInputValue] = useState("");
  const [success, setSuccess] = useState(null);
  const { addWord, error, isLoading } = useAddWord(onWordAdded);

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      handleAddWord();
    }
  };

  const handleAddWord = () => {
    addWord(inputValue, () => {
      setInputValue("");
      setSuccess("Word added successfully!");
      setTimeout(() => setSuccess(null), 3000);
    });
  };

  return (
    <div className="add-container">
      {/* Notifications */}
      <div className="notification-container">
        {error && (
          <div className="error-notification">
            <span>⚠️ {error}</span>
          </div>
        )}
        {success && (
          <div className="success-notification">
            <span>✓ {success}</span>
          </div>
        )}
      </div>

      <div className="input-section">
        <h3>Add New Word</h3>
        <div>
          <label htmlFor="add-word-input" className="visually-hidden">
            Enter a word
          </label>
          <input
            id="add-word-input"
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Enter a word"
            onKeyDown={handleKeyPress}
            className="field"
            disabled={isLoading}
            aria-invalid={!!error}
          />
          <button
            onClick={handleAddWord}
            className="btn"
            disabled={isLoading || !inputValue.trim()}
          >
            {isLoading ? "Adding..." : "Add Word"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default AddWordForm;
