import React, { useState, useEffect } from "react";
import '../../styles/QuizAnswerUnit.css';
import { useAuth } from "@clerk/clerk-react";

function QuizResult({word_id, word, userAnswer ,progress}) {
  const [correctIndexes, setCorrectIndexes] = useState([]);
  const [incorrectIndexes, setIncorrectIndexes] = useState([]);
  const [extraCorrectIndexes, setExtraCorrectIndexes] = useState([]);
  const [extraIncorrectIndexes, setExtraIncorrectIndexes] = useState([]);


  const { getToken } = useAuth();

  // 2. User answered correctly and is not at the last learning stage
  const cor_answer_not_last_learning_stage = async () => {
    console.log("Function called: cor_answer_not_last_learning_stage");
    increaseCorrectCount();
    increaseCorrectInRowCount();
    increaseLearningStage();
    resetCorrectInRowCount();
    increaseCorrectInRowCount();
  }

  // 3. User answered correctly , but it's the first correct answer in a row
  const cor_answer_first_in_row = async () => {
    console.log("Function called: cor_answer_first_in_row");
    increaseCorrectCount();
    increaseCorrectInRowCount();
    resetWrongInRowCount();
  }

  // 4. User answered correctly , but it's not the first correct answer in a row
  const cor_answer_not_first_in_row = async () => {
    console.log("Function called: cor_answer_not_first_in_row");
    increaseCorrectCount();
    increaseCorrectInRowCount();
  }

  // 5. User answered wrongly, it's the first wrong answer in a row
  const wrong_answer_first_in_row = async () => {
    console.log("Function called: wrong_answer_first_in_row");
    increaseWrongCount();
    increaseWrongInRowCount();
    resetCorrectInRowCount();
  }

  //6. User answered wrongly, it's not the first wrong answer in a row
  const wrong_answer_not_first_in_row = async () => {
    console.log("Function called: wrong_answer_not_first_in_row");
    increaseWrongCount();
    increaseWrongInRowCount();
  }

 //7. User answered wrongly and is not at the first learning stage
  const wrong_answer_not_first_learning_stage = async () => {
    console.log("Function called: wrong_answer_not_first_learning_stage");
    increaseWrongCount();
    decreaseLearningStage();
    resetWrongInRowCount();
    increaseWrongInRowCount();
  }
  


  const add_Minutes = (minutes) => {
    const currentDate = new Date();
    currentDate.setMinutes(currentDate.getMinutes() + minutes);
    setNewDateToRepeat(currentDate);
  }

  const add_Days = (days) => {
    const currentDate = new Date();
    currentDate.setDate(currentDate.getDate() + days);
    setNewDateToRepeat(currentDate);
  }

  const add_Weeks = (weeks) => {
    const currentDate = new Date();
    currentDate.setDate(currentDate.getDate() + weeks * 7);
    setNewDateToRepeat(currentDate);
  }

  const add_Months = (months) => {
    const currentDate = new Date();
    currentDate.setMonth(currentDate.getMonth() + months);
    setNewDateToRepeat(currentDate);
  }




  const increaseCorrectCount = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quiz/words/${word_id}/correct-answers`, {
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
      const response = await fetch(`http://localhost:8000/quiz/words/${word_id}/wrong-answers`, {
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

  const increaseLearningStage = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quiz/words/${word_id}/learning-stage/increase`, {
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
        console.error("Failed to increase learning stage:", error);
    }
  };

  const decreaseLearningStage = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quiz/words/${word_id}/learning-stage/decrease`, {
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
        console.error("Failed to decrease learning stage:", error);
    }
  };

  const increaseCorrectInRowCount = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quiz/words/${word_id}/correct-answers-row/increase`, {
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
        console.error("Failed to increase correct in row count:", error);
    }
  };
  const resetCorrectInRowCount = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quiz/words/${word_id}/correct-answers-row/reset`, {
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
        console.error("Failed to reset correct in row count:", error);
    }
  };

  const increaseWrongInRowCount = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quiz/words/${word_id}/wrong-answers-row/increase`, {
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
        console.error("Failed to increase wrong in row count:", error);
    }
  }

  const resetWrongInRowCount = async () => {
    try{
      const token = await getToken();
      const response = await fetch(`http://localhost:8000/quiz/words/${word_id}/wrong-answers-row/reset`, {
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
        console.error("Failed to reset wrong in row count:", error);
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
    const [isEmpty, setIsEmpty] = useState(false);
    if (word.word.length === 0 && safeUserAnswer.length === 0) {
      setIsEmpty(true);
    }
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
    
    return { correct, incorrect, extraCorrect, extraIncorrect , isEmpty};
  };

  useEffect(() => {
    if (word.vocabulary === 'unknown') {
      changeVocabularyToLearn();
    }
    if (!userAnswer) {
      return;
    }
    
    const { correct, incorrect, extraCorrect, extraIncorrect } = calculateIndexes(word, userAnswer);
    
    if (correct.length === word.word.length && extraCorrect.length === 0 && extraIncorrect.length === 0) {
    console.log("Handling correct answer...");
    if (progress.correct_answers_in_a_row === 0) {
      cor_answer_first_in_row();
      if (progress.learning_stage === 1) {
        add_Minutes(15);
      }else if (progress.learning_stage === 2) {
        add_Days(1);
      }else if (progress.learning_stage === 3) {
        add_Weeks(1);
      }else if (progress.learning_stage === 4) {
        add_Months(1);
      }
    } else if (progress.correct_answers_in_a_row + 1 === 5 && progress.learning_stage !== 4) {
      cor_answer_not_last_learning_stage();
      if (progress.learning_stage === 1) {
        add_Minutes(5 * (progress.correct_answers_in_a_row + 1));
      }else if (progress.learning_stage === 2) {
        add_Days(7 * (progress.correct_answers_in_a_row + 1));
      }else if (progress.learning_stage === 3) {
        add_Weeks(4 * (progress.correct_answers_in_a_row + 1));
      }
    } else {
      cor_answer_not_first_in_row();
      add_Minutes((progress.correct_answers_in_a_row + 1) * 5);
  }
}
if (incorrect.length > 0 || extraCorrect.length > 0 || extraIncorrect.length > 0 || is) {
  console.log("Handling wrong answer...");
  if (progress.wrong_answers_in_a_row === 0) {
    wrong_answer_first_in_row();
    if (progress.learning_stage === 1) {
      add_Minutes(5);
    }else if (progress.learning_stage === 2) {
      add_Days(1);
    }else if (progress.learning_stage === 3) {
      add_Weeks(1);
    }else if (progress.learning_stage === 4) {
      add_Months(1);
    }
  } else if (progress.wrong_answers_in_a_row + 1 === 5 && progress.learning_stage > 1) {
    console.log("Decreasing learning stage due to multiple wrong answers in a row.");
    wrong_answer_not_first_learning_stage();
    if (progress.learning_stage === 2) {
      add_Days(1);
    }else if (progress.learning_stage === 3) {
      add_Weeks(1);
    }else if (progress.learning_stage === 4) {
      add_Months(1);
    }
  } else {
    wrong_answer_not_first_in_row();
    add_Minutes(10);
  }
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