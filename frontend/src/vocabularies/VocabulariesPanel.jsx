import React, { useState, useEffect } from "react";
import AddWordContainer from "./AddWordContainer";
import WordList from "./WordList";
import { useAuth } from "@clerk/clerk-react";
import '../../styles/VocabularyPanel.css';

export function VocabulariesPanel() {
  const [words, setWords] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { getToken } = useAuth();

  const fetchWords = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const token = await getToken();
      const response = await fetch("http://localhost:8000/user/words", {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch words");
      }
  

      const data = await response.json();
      console.log("Fetched words data:", data.words); 
      
      setWords(data.words || []);
    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchWords();
  }, []);

  return (
    <div>
      {error && <div style={{ color: "red", padding: "1rem" }}>Error: {error}</div>}
      <div className="add-word-container">
        <div className="left-panel">
          {/* FIX: Pass the 'fetchWords' function as the 'onWordAdded' prop */}
          <AddWordContainer onWordAdded={fetchWords} />
        </div>
        <div className="right-panel">
          {isLoading ? <p>Loading...</p> : <WordList words={words} />}
        </div>
      </div>
    </div>
  );
}