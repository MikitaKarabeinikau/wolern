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
  const [words, setWords] = useState([]);
  const [error, setError] = useState(null); // Add error state
  const { getToken } = useAuth();

  const [translation, setTranslation] = useState({});
  const [definition, setDefinition] = useState({});
  const [example, setExample] = useState({});
  const [synonym, setSynonym] = useState({});

  const fetchQuizWords = async () => {
    // This function now ONLY fetches word details.
    const token = await getToken();
    const headers = { Authorization: `Bearer ${token}` };
    const responses = await Promise.all([
      fetch(`http://localhost:8000/quiz/word/translations`, { headers }),
      fetch(`http://localhost:8000/quiz/word/definitions`, { headers }),
      fetch(`http://localhost:8000/quiz/word/examples`, { headers }),
      fetch(`http://localhost:8000/quiz/word/synonyms`, { headers }),
      fetch(`http://localhost:8000/quiz/generate`, { headers })
    ]);

  const [translationsRes, definitionsRes, examplesRes, synonymsRes, wordsRes] = await Promise.all(responses.map(res => res.json()));

  setTranslation(createMapByWordId(translationsRes, 'translations'));
  setDefinition(createMapByWordId(definitionsRes, 'definitions'));
  setExample(createMapByWordId(examplesRes, 'examples'));
  setSynonym(createMapByWordId(synonymsRes, 'synonyms'));
  setWords(wordsRes.words || []);
  };

  

  useEffect(() => {
    fetchQuizWords();
  }, []);

  const handleNextQuestion = () => {
    // Logic to load the next question
    setIsAnswered(false);
  }

  if (isAnswered) {
    return (
      <div>
        <QuizResult />
        <button onClick={handleNextQuestion}>Next Question</button>
      </div>
    )
  }

  
  return (
    <div>
      {error && <div style={{ color: "red" }}>Error: {error}</div>} {/* Display error message */}
      {words.length > 0 ? (
        <QuizWord word={words[0]} wordTranslation={translation[words[0].id]} wordExample={example[words[0].id]} wordDefinition={definition[words[0].id]} wordSynonym={synonym[words[0].id]} />
      ) : (
        <p>Loading quiz...</p>
      )}
      <QuizAnswerField />
    </div>
  )
}