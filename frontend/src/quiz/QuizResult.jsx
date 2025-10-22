import React, { useState, useEffect } from "react";
import '../../styles/QuizAnswerUnit.css';
import { useAuth } from "@clerk/clerk-react";

function QuizResult({word_id, word, userAnswer }) {
  const [correctIndexes, setCorrectIndexes] = useState([]);
  const [incorrectIndexes, setIncorrectIndexes] = useState([]);
  const [extraCorrectIndexes, setExtraCorrectIndexes] = useState([]);
  const [extraIncorrectIndexes, setExtraIncorrectIndexes] = useState([]);
  const [nextTimeToRepeat, setNextTimeToRepeat] = useState(null);

  const { getToken } = useAuth();


  const increaseCorrectCount = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/words/${word_id}/correct-answers`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);  
      }

    } catch (error) {
        console.error("Failed to increase correct count:", error);
    }
  }

  const increaseWrongCount = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/words/${word_id}/wrong-answers`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);  
      }

    } catch (error) {
        console.error("Failed to increase wrong count:", error);
    }
  };

  const changeVocabularyToLearn = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/words/${word_id}/vocabulary/to_learn`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);  
      }

    } catch (error) {
        console.error("Failed to change vocabulary:", error);
    }
  };

  const setNewDateToRepeat =  async (new_date) => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quiz/word/${word_id}/set_next_review_date`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({new_date: new_date.toISOString()}),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);  
      }

    } catch (error) {
        console.error("Failed to set next review date:", error);
    }
  };
  const calculateIndexes = (word, userAnswer) => {
    const correct = [];
    const incorrect = [];
    const extraCorrect = [];
    const extraIncorrect = [];
    const safeUserAnswer = userAnswer || '';
    const maxLength = Math.max(word.word.length, safeUserAnswer.length);

    for (let i = 0; i < maxLength; i++) {
      const wordLetter = word.word[i] || null;
      const userAnswerLetter = safeUserAnswer[i] || null;

      if (wordLetter && userAnswerLetter) {
        if (wordLetter === userAnswerLetter) {
          correct.push(i);
        } else {
          incorrect.push(i);
        }
      } else if (wordLetter) {
        extraCorrect.push(i);
      } else if (userAnswerLetter) {
        extraIncorrect.push(i);
      }
    }
    
    return { correct, incorrect, extraCorrect, extraIncorrect };
  };

  useEffect(() => {
    if (word.vocabulary === 'unknown') {
      changeVocabularyToLearn();
    }
    if (!userAnswer) {
      return;
    }

    const { correct, incorrect, extraCorrect, extraIncorrect } = calculateIndexes(word, userAnswer);


    if (correct.length === word.word.length && extraCorrect.length === 0 && extraIncorrect.length === 0 && incorrect.length === 0) {
      const nextReviewDate = new Date();
      nextReviewDate.setMinutes(nextReviewDate.getMinutes() + 15);
     
      setNewDateToRepeat(nextReviewDate);
      increaseCorrectCount();
    } else if (correct.length === 0) {
      const nextReviewDate = new Date();
      nextReviewDate.setMinutes(nextReviewDate.getMinutes() + 5);
      setNewDateToRepeat(nextReviewDate);
      increaseWrongCount();
    } else if (correct.length > 0) {
      const nextReviewDate = new Date();
      nextReviewDate.setMinutes(nextReviewDate.getMinutes() + 10);
      setNewDateToRepeat(nextReviewDate);
      increaseWrongCount();
    }
    
    
    setCorrectIndexes(correct);
    setIncorrectIndexes(incorrect);
    setExtraCorrectIndexes(extraCorrect);
    setExtraIncorrectIndexes(extraIncorrect);


  }, [word.word, userAnswer]); // Correct placement of the closing brace

  return (
    <>
      <div className="quiz-answers-container">
        <div className="quiz-correct-answer">
          {word.word.split("").map((l, index) => (
            <span
              key={index}
              className={`quiz-letter ${correctIndexes.includes(index) ? 'correct' : incorrectIndexes.includes(index) ? 'incorrect' : extraCorrectIndexes.includes(index) ? 'extra-correct' : ''}`}
            >
              {l}
            </span>
          ))}
          {extraIncorrectIndexes.length > 0 && extraIncorrectIndexes.map((index) => (
            <span key={`extra-correct-${index}`} className="quiz-letter extra-letter">
              .
            </span>
          ))}
        </div>
        <div className="quiz-user-answer">
          {(userAnswer || '').split("").map((l, index) => (
            <span
              key={index}
              className={`quiz-letter ${correctIndexes.includes(index) ? 'correct' : incorrectIndexes.includes(index) ? 'extra-incorrect' : extraIncorrectIndexes.includes(index) ? 'extra-incorrect' : ''}`}
            >
              {l}
            </span>
          ))}
          {extraCorrectIndexes.length > 0 && extraCorrectIndexes.map((index) => (
            <span key={`extra-incorrect-${index}`} className="quiz-letter extra-letter">
              .
            </span>
          ))}
        </div>
      </div>
    </>
  );
}

export default QuizResult;