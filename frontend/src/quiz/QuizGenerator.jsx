import React, {useState, useEffect} from "react";
import QuizWord from "./QuizWord";
import QuizAnswerField from "./QuizAnswerField";
import QuizResult from "./QuizResult";
import { useAuth } from "@clerk/clerk-react";


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


export function QuizGenerator() {
  const [isAnswered, setIsAnswered] = useState(false);
  const [result, setResult] = useState(null);
  const [words, setWords] = useState([]);
  const [error, setError] = useState(null); // Add error state
  const { getToken } = useAuth();
  const [progress, setProgress] = useState([]);

  const [translation, setTranslation] = useState({});
  const [definition, setDefinition] = useState({});
  const [example, setExample] = useState({});
  const [synonym, setSynonym] = useState({});
  const [currentWordIndex, setCurrentWordIndex] = useState(0);

  const fetchQuizWords = async () => {
    // This function now ONLY fetches word details.
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

    const [translationsRes, definitionsRes, examplesRes, synonymsRes, wordsRes, progressRes] = await Promise.all(
      responses.map(async (res) => {
        if (!res.ok) {
          throw new Error(`Failed to fetch: ${res.url}`);
        }
        return res.json();
      })
    );
  setTranslation(createMapByWordId(translationsRes, 'translations'));
  setDefinition(createMapByWordId(definitionsRes, 'definitions'));
  setExample(createMapByWordId(examplesRes, 'examples'));
  setSynonym(createMapByWordId(synonymsRes, 'synonyms'));
  setWords(wordsRes.words || []);
  setProgress(progressRes.progress || []);
  };

  

  useEffect(() => {
    fetchQuizWords();
  }, []);

  const handleNextQuestion = () => {
    // Logic to load the next question
    setIsAnswered(false);
    setResult(null);
    if (currentWordIndex + 1 >= words.length){
        // Restart the quiz or handle end of quiz
        fetchQuizWords();
        setCurrentWordIndex(0);
    } else {
    setCurrentWordIndex((prevIndex) => prevIndex + 1);
    }
  }

  const handleCheckAnswer = (answer) => {
    setResult(answer);
    setIsAnswered(true);
  }
  

  const pressEnter = (e) => {
    if (e.key === 'Enter') {
      handleNextQuestion();
    }
  }
return (
   <div style={{ display: "flex", flexDirection: "row" }}>
      {/* Main Quiz Section */}
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
                wordProgress={progress.find((p) => p.word_id === words[currentWordIndex].id)}
              />
              <QuizAnswerField onCheckAnswer={handleCheckAnswer} />
            </div>

            <div style={{ display: isAnswered ? "block" : "none" }}>
              <>
                <QuizResult
                  word_id={words[currentWordIndex].id}
                  word={words[currentWordIndex]}
                  userAnswer={result}
                  progress={progress.find((p) => p.word_id === words[currentWordIndex].id)}
                />
                <button onClick={handleNextQuestion}
                onKeyDown={pressEnter}
                >Next Question</button>
              </>
            </div>
          </>
        ) : (
          <p>Loading quiz...</p>
        )}
      </div>

      {/* Sidebar for Progress Data */}
<div style={{ flex: 1, padding: "20px", borderLeft: "1px solid #ccc" }}>
  <h3>Progress Data</h3>
  {progress.length > 0 ? (
    <table style={{ width: "100%", borderCollapse: "collapse", tableLayout: "auto" }}>
      <thead>
        <tr>
          <th style={{ border: "1px solid #ccc", padding: "8px", textAlign: "left", wordWrap: "break-word" }}>Word</th>
          <th style={{ border: "1px solid #ccc", padding: "8px", textAlign: "left", wordWrap: "break-word" }}>Correct Answers</th>
          <th style={{ border: "1px solid #ccc", padding: "8px", textAlign: "left", wordWrap: "break-word" }}>Wrong Answers</th>
          <th style={{ border: "1px solid #ccc", padding: "8px", textAlign: "left", wordWrap: "break-word" }}>Learning Stage</th>
          <th style={{ border: "1px solid #ccc", padding: "8px", textAlign: "left", wordWrap: "break-word" }}>Correct Answers in a Row</th>
          <th style={{ border: "1px solid #ccc", padding: "8px", textAlign: "left", wordWrap: "break-word" }}>Wrong Answers in a Row</th>
          <th style={{ border: "1px solid #ccc", padding: "8px", textAlign: "left", wordWrap: "break-word" }}>Time to Repeat</th>
        </tr>
      </thead>
      <tbody>
        {progress.map((p) => {
          const word = words.find((w) => w.id === p.word_id)?.word || "Unknown Word";
          return (
            <tr key={p.word_id}>
              <td style={{ border: "1px solid #ccc", padding: "8px", wordWrap: "break-word", maxWidth: "150px" }}>{word}</td>
              <td style={{ border: "1px solid #ccc", padding: "8px", wordWrap: "break-word", maxWidth: "150px" }}>{p.correct_answers || 0}</td>
              <td style={{ border: "1px solid #ccc", padding: "8px", wordWrap: "break-word", maxWidth: "150px" }}>{p.wrong_answers || 0}</td>
              <td style={{ border: "1px solid #ccc", padding: "8px", wordWrap: "break-word", maxWidth: "150px" }}>{p.learning_stage || 0}</td>
              <td style={{ border: "1px solid #ccc", padding: "8px", wordWrap: "break-word", maxWidth: "150px" }}>{p.correct_answers_in_a_row || 0}</td>
              <td style={{ border: "1px solid #ccc", padding: "8px", wordWrap: "break-word", maxWidth: "150px" }}>{p.wrong_answers_in_a_row || 0}</td>
              <td style={{ border: "1px solid #ccc", padding: "8px", wordWrap: "break-word", maxWidth: "150px" }}>{p.time_to_repeat || "No data"}</td>

            </tr>
          );
        })}
      </tbody>
    </table>
  ) : (
    <p>No progress data available.</p>
  )}
</div>
    </div>
  )
}