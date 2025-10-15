import React, { useState, useEffect } from "react";
import AddWordContainer from "./AddWordContainer";
import WordList from "./WordList";
import { useAuth } from "@clerk/clerk-react";
import '../../styles/VocabularyPanel.css';


const createMapByWordId = (items, key) => {
  const map = {};
  if (!items || !items[key]) return map;

  for (const item of items[key]) {
    const wordId = item.word_id;
    if (!map[wordId]) {
      map[wordId] = [];
    }
    map[wordId].push(item);
  }
  return map;
};

export function VocabulariesPanel() {
  const [words, setWords] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [translationMap, setTranslationMap] = useState({});
  const [definitionMap, setDefinitionMap] = useState({});
  const [exampleMap, setExampleMap] = useState({});
  const [synonymMap, setSynonymMap] = useState({});
  const [warningMap, setWarningMap] = useState({});
  const [tagMap, setTagMap] = useState({});
  const { getToken } = useAuth();

  const fetchWords = async () => {
    // This function now ONLY fetches words.
    const token = await getToken();
    const response = await fetch("http://localhost:8000/user/words", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to fetch words");
    const data = await response.json();
    setWords(data.words || []);
  };

  const fetchWordInfo = async () => {
    // This function now ONLY fetches word details.
    const token = await getToken();
    const headers = { Authorization: `Bearer ${token}` };
    const responses = await Promise.all([
      fetch(`http://localhost:8000/user/words/translations/all`, { headers }),
      fetch(`http://localhost:8000/user/words/definitions/all`, { headers }),
      fetch(`http://localhost:8000/user/words/examples/all`, { headers }),
      fetch(`http://localhost:8000/user/words/synonyms/all`, { headers }),
      fetch(`http://localhost:8000/user/words/warnings/all`, { headers }),
      fetch(`http://localhost:8000/user/words/tags/all`, { headers })
    ]);

    for (const res of responses) {
      if (!res.ok) throw new Error(`Failed to fetch word info: ${res.statusText}`);
    }

    const [translationsData, definitionsData, examplesData, synonymsData, warningsData, tagsData] = await Promise.all(responses.map(res => res.json()));

    setTranslationMap(createMapByWordId(translationsData, 'translations'));
    setDefinitionMap(createMapByWordId(definitionsData, 'definitions'));
    setExampleMap(createMapByWordId(examplesData, 'examples'));
    setSynonymMap(createMapByWordId(synonymsData, 'synonyms'));
    setWarningMap(createMapByWordId(warningsData, 'warnings'));
    setTagMap(createMapByWordId(tagsData, 'tags'));
  };

  // FIX 1: Create a single function for the initial data load.
  const fetchInitialData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Fetch both sets of data concurrently for speed.
      await Promise.all([fetchWords(), fetchWordInfo()]);
    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  // FIX 2: Create a handler that refreshes ALL data after a word is added.
  const handleWordAdded = async () => {
    // We can just call the initial fetch function again.
    // This ensures the new word AND its details are loaded.
    await fetchInitialData();
  };

  useEffect(() => {
    // On component mount, fetch all initial data.
    fetchInitialData();
  }, []);

  return (
    <div>
      {error && <div style={{ color: "red", padding: "1rem" }}>Error: {error}</div>}
      <div className="add-word-container">
        <div className="left-panel">
          <AddWordContainer onWordAdded={handleWordAdded} />
        </div>
        <div className="right-panel">
          {isLoading ? <p>Loading...</p> : <WordList words={words} translationsMap = {translationMap} definitionsMap={definitionMap} examplesMap={exampleMap} synonymsMap={synonymMap} warningsMap={warningMap} tagsMap={tagMap} />}
        </div>
      </div>
    </div>
  );
}