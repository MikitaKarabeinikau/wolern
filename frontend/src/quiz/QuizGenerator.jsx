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
return (
    <div>
      {error && <div style={{ color: "red" }}>Error: {error}</div>}
      
      {words.length > 0 ? (
        <>
          {/* This part is correct */}
          <div style={{ display: isAnswered ? 'none' : 'block' }}>
            <QuizWord 
              word={words[currentWordIndex]} 
              wordTranslation={translation[words[currentWordIndex].id]} 
              wordExample={example[words[currentWordIndex].id]} 
              wordDefinition={definition[words[currentWordIndex].id]} 
              wordSynonym={synonym[words[currentWordIndex].id]} 
            />
            <QuizAnswerField onCheckAnswer={handleCheckAnswer} />
          </div>

          {/* --- Start of Change --- */}
          <div style={{ display: isAnswered ? 'block' : 'none' }}>
            {/* The "isAnswered &&" check has been removed */}
            <>
              <QuizResult 
                word_id={words[currentWordIndex].id} 
                word={words[currentWordIndex]} 
                userAnswer={result} 
              />
              <button onClick={handleNextQuestion}>Next Question</button>
            </>
          </div>
          {/* --- End of Change --- */}
        </>
      ) : (
        <p>Loading quiz...</p>
      )}
    </div>
  )
}