import React, { useState, useEffect, useMemo } from "react";
import QuizWord from "./QuizWord";
import QuizAnswerField from "./components/QuizAnswerField";
import QuizResult from "./components/QuizResult";
import { useAuth } from "@clerk/clerk-react";
import { createMapByWordId } from "../../utils/wordProcessing";
import DebugQuizTable from "./components/DebugQuizTable";

export function QuizGenerator() {
  const [isAnswered, setIsAnswered] = useState(false);
  const [result, setResult] = useState(null);
  const [words, setWords] = useState([]);
  const [error, setError] = useState(null);
  const { getToken } = useAuth();
  const [progress, setProgress] = useState([]);
  const [actionSummary, setActionSummary] = useState([]); // State for action summary

  const [translation, setTranslation] = useState({});
  const [definition, setDefinition] = useState({});
  const [example, setExample] = useState({});
  const [synonym, setSynonym] = useState({});
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [prevTime, setPrevTime] = useState("");

  const fetchQuizWords = async () => {
    const token = await getToken();
    const headers = { Authorization: `Bearer ${token}` };
    const responses = await Promise.all([
      fetch(`http://localhost:8000/quiz/word/translations`, { headers }),
      fetch(`http://localhost:8000/quiz/word/definitions`, { headers }),
      fetch(`http://localhost:8000/quiz/word/examples`, { headers }),
      fetch(`http://localhost:8000/quiz/word/synonyms`, { headers }),
      fetch(`http://localhost:8000/quiz/generate`, { headers }),
      fetch(`http://localhost:8000/quiz/data`, { headers }),
    ]);

    const [
      translationsRes,
      definitionsRes,
      examplesRes,
      synonymsRes,
      wordsRes,
      progressRes,
    ] = await Promise.all(
      responses.map(async (res) => {
        if (!res.ok) {
          throw new Error(`Failed to fetch: ${res.url}`);
        }
        return res.json();
      })
    );
    setTranslation(createMapByWordId(translationsRes, "translations"));
    setDefinition(createMapByWordId(definitionsRes, "definitions"));
    setExample(createMapByWordId(examplesRes, "examples"));
    setSynonym(createMapByWordId(synonymsRes, "synonyms"));
    setWords(wordsRes.words || []);
    setProgress(progressRes.progress || []);
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return "No data";
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      day: "2-digit",
      month: "2-digit",
      year: "2-digit",
    });
  };

  useEffect(() => {
    fetchQuizWords();
  }, []);

  const debugData = useMemo(() => {
    if (!words.length || !progress.length) {
      return [];
    }

    // Create a map of progress data for quick lookups
    const progressMap = new Map(progress.map((p) => [p.word_id, p]));

    // Map over the words and merge with their corresponding progress
    return words.map((word) => ({
      ...word, // Includes word.id, word.word, etc.
      progress: progressMap.get(word.id) || {}, // Find the matching progress, or use an empty object
    }));
  }, [words, progress]);

  const handleNextQuestion = () => {
    setIsAnswered(false);
    setResult(null);

    if (currentWordIndex + 1 >= words.length) {
      fetchQuizWords();
      setCurrentWordIndex(0);
    } else {
      setCurrentWordIndex((prevIndex) => prevIndex + 1);
    }
  };

  const handleCheckAnswer = (answer) => {
    setResult(answer);
    setIsAnswered(true);
  };
  const pressEnter = (e) => {
    if (e.key === "Enter") {
      handleNextQuestion();
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "row" }}>
      <div style={{ flex: 2, padding: "20px" }}>
        {error && <div style={{ color: "red" }}>Error: {error}</div>}

        {words.length > 0 ? (
          <>
            <div style={{ display: isAnswered ? "none" : "block" }}>
              <QuizWord
                word={words[currentWordIndex]}
                wordTranslation={translation[words[currentWordIndex].id]}
                wordExample={example[words[currentWordIndex].id]}
                wordDefinition={definition[words[currentWordIndex].id]}
                wordSynonym={synonym[words[currentWordIndex].id]}
                wordProgress={progress.find(
                  (p) => p.word_id === words[currentWordIndex].id
                )}
              />
              <QuizAnswerField onCheckAnswer={handleCheckAnswer} />
            </div>
            <DebugQuizTable data={debugData} />

            <div style={{ display: isAnswered ? "block" : "none" }}>
              <>
                <QuizResult
                  word_id={words[currentWordIndex].id}
                  word={words[currentWordIndex]}
                  userAnswer={result}
                  progress={progress.find(
                    (p) => p.word_id === words[currentWordIndex].id
                  )}
                />
                <button onClick={handleNextQuestion} onKeyDown={pressEnter}>
                  Next Question
                </button>
              </>
            </div>
          </>
        ) : (
          <p>Loading quiz...</p>
        )}
      </div>
    </div>
  );
}
