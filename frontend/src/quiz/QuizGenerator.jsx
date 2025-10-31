import React, { useState, useEffect } from "react";
import QuizWord from "./QuizWord";
import QuizAnswerField from "./QuizAnswerField";
import QuizResult from "./QuizResult";
import { useAuth } from "@clerk/clerk-react";

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
{/* 
      <div style={{ flex: 1, padding: "20px", borderLeft: "1px solid #ccc" }}>
        <h3>Progress Data</h3>
        {progress.length > 0 ? (
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              tableLayout: "auto",
            }}
          >
            <thead>
              <tr>
                <th>Word</th>
                <th>Correct Answers</th>
                <th>Wrong Answers</th>
                <th>Learning Stage</th>
                <th>Correct Answers in a Row</th>
                <th>Wrong Answers in a Row</th>
                <th>Time to Repeat</th>
              </tr>
            </thead>
            <tbody>
              {progress.map((p) => {
                const word =
                  words.find((w) => w.id === p.word_id)?.word || "Unknown Word";
                return (
                  <tr key={p.word_id}>
                    <td>{word}</td>
                    <td>{p.correct_answers || 0}</td>
                    <td>{p.wrong_answers || 0}</td>
                    <td>{p.learning_stage || 0}</td>
                    <td>{p.correct_answers_in_a_row || 0}</td>
                    <td>{p.wrong_answers_in_a_row || 0}</td>
                    <td>{formatDateTime(p.time_to_repeat)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <p>No progress data available.</p>
        )}
      
      </div> */}
    </div>
  );
}
