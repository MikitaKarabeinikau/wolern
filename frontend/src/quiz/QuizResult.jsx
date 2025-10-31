import React, { useState, useEffect } from "react";
import "../../styles/QuizAnswerUnit.css";
import { useAuth } from "@clerk/clerk-react";

function QuizResult({ word_id, word, userAnswer, progress }) {
  const [correctIndexes, setCorrectIndexes] = useState([]);
  const [incorrectIndexes, setIncorrectIndexes] = useState([]);
  const [extraCorrectIndexes, setExtraCorrectIndexes] = useState([]);
  const [extraIncorrectIndexes, setExtraIncorrectIndexes] = useState([]);

  const { getToken } = useAuth();

  const add_Minutes = (minutes) => {
    const currentDate = new Date();
    currentDate.setMinutes(currentDate.getMinutes() + minutes);
    setNewDateToRepeat(currentDate);
  };

  const add_Days = (days) => {
    const currentDate = new Date();
    currentDate.setDate(currentDate.getDate() + days);
    setNewDateToRepeat(currentDate);
  };

  const add_Weeks = (weeks) => {
    const currentDate = new Date();
    currentDate.setDate(currentDate.getDate() + weeks * 7);
    setNewDateToRepeat(currentDate);
  };

  const add_Months = (months) => {
    const currentDate = new Date();
    currentDate.setMonth(currentDate.getMonth() + months);
    setNewDateToRepeat(currentDate);
  };

  const increaseCorrectCount = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/words/${word_id}/correct-answers`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to increase correct count:", error);
    }
  };

  const increaseWrongCount = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/words/${word_id}/wrong-answers`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to increase wrong count:", error);
    }
  };

  const increaseLearningStage = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/words/${word_id}/learning-stage/increase`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to increase learning stage:", error);
    }
  };

  const decreaseLearningStage = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/words/${word_id}/learning-stage/decrease`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to decrease learning stage:", error);
    }
  };

  const increaseCorrectInRowCount = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/words/${word_id}/correct-answers-row/increase`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to increase correct in row count:", error);
    }
  };
  const resetCorrectInRowCount = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/words/${word_id}/correct-answers-row/reset`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to reset correct in row count:", error);
    }
  };

  const increaseWrongInRowCount = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/words/${word_id}/wrong-answers-row/increase`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to increase wrong in row count:", error);
    }
  };

  const resetWrongInRowCount = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/words/${word_id}/wrong-answers-row/reset`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to reset wrong in row count:", error);
    }
  };

  const changeVocabularyToLearn = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/words/${word_id}/vocabulary/to_learn`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to change vocabulary:", error);
    }
  };

  const setNewDateToRepeat = async (new_date) => {
    try {
      const token = await getToken();
      const response = await fetch(
        `http://localhost:8000/quiz/word/${word_id}/set_next_review_date`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ new_date: new_date.toISOString() }),
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    } catch (error) {
      console.error("Failed to set next review date:", error);
    }
  };
  const [isEmpty, setIsEmpty] = useState(false);
  const calculateIndexes = (word, userAnswer) => {
    const correct = [];
    const incorrect = [];
    const extraCorrect = [];
    const extraIncorrect = [];
    const safeUserAnswer = userAnswer || "";
    const maxLength = Math.max(word.word.length, safeUserAnswer.length);

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

    return { correct, incorrect, extraCorrect, extraIncorrect, isEmpty };
  };

  useEffect(() => {
    if (word.vocabulary === "unknown") {
      changeVocabularyToLearn();
    }
    if (!userAnswer) {
      return;
    }

    const answerLogic = async (progress, answer) => {
      if (answer) {
        console.log("Answer is correct, processing...");
        if (progress.wrong_answers_in_a_row === 0) {
          console.log("Correct answer is not first in a row.");
          if (progress.correct_answers_in_a_row === 4) {
            console.log("Correct answer is a 4th in a row.");
            if (progress.learning_stage === 4) {
              console.log("User is at the last learning stage.");
              increaseCorrectCount();
              increaseCorrectInRowCount();
              progress.correct_answers += 1;
              progress.correct_answers_in_a_row += 1;
            } else {
              console.log("User is not at the last learning stage.");
              increaseLearningStage();
              resetCorrectInRowCount();
              increaseCorrectInRowCount();
              increaseCorrectCount();

              progress.correct_answers += 1;
              progress.correct_answers_in_a_row = 1;
              progress.learning_stage += 1;
            }
          } else {
            console.log("Correct answer is less than 4th in a row.");
            increaseCorrectInRowCount();
            increaseCorrectCount();
            progress.correct_answers += 1;
            progress.correct_answers_in_a_row += 1;
          }
        } else {
          console.log("Correct answer is first in a row.");
          resetWrongInRowCount();
          increaseCorrectInRowCount();
          increaseCorrectCount();

          progress.correct_answers += 1;
          progress.wrong_answers_in_a_row = 0;
          progress.correct_answers_in_a_row += 1;
        }
      } else {
        console.log("Answer is incorrect, processing...");
        if (progress.correct_answers_in_a_row === 0) {
          console.log("Wrong answer is not first in a row.");
          if (progress.wrong_answers_in_a_row === 4) {
            console.log("Wrong answer is a 4th in a row.");
            if (progress.learning_stage === 1) {
              console.log("User is at the first learning stage.");
              increaseWrongCount();
              increaseWrongInRowCount();

              progress.wrong_answers += 1;
              progress.wrong_answers_in_a_row += 1;
            } else {
              console.log("User is not at the first learning stage.");
              decreaseLearningStage();
              resetWrongInRowCount();
              increaseWrongInRowCount();
              increaseWrongCount();

              progress.wrong_answers += 1;
              progress.wrong_answers_in_a_row = 1;
              progress.learning_stage -= 1;
            }
          } else {
            console.log("Wrong answer is less than 4th in a row.");
            increaseWrongInRowCount();
            increaseWrongCount();

            progress.wrong_answers += 1;
            progress.wrong_answers_in_a_row += 1;
          }
        } else {
          console.log("Wrong answer is first in a row.");
          resetCorrectInRowCount();
          increaseWrongInRowCount();
          increaseWrongCount();

          progress.wrong_answers += 1;
          progress.correct_answers_in_a_row = 0;
          progress.wrong_answers_in_a_row += 1;
        }
      }
    };

    const addingTimeToRepeat = async (progress, answer) => {
      if (answer) {
        switch (progress.learning_stage) {
          case 1:
            switch (progress.correct_answers_in_a_row) {
              case 1:
                console.log(
                  "learning stage 1 | Correct in a row 1: Adding 10 minutes to repeat time."
                );
                add_Minutes(10);
                break;
              case 2:
                console.log(
                  "learning stage 1 | Correct in a row 2: Adding 15 minutes to repeat time."
                );
                add_Minutes(15);
                break;
              case 3:
                console.log(
                  "learning stage 1 | Correct in a row 3: Adding 30 minutes to repeat time."
                );
                add_Minutes(30);
                break;
              case 4:
                console.log(
                  "learning stage 1 | Correct in a row 4: Adding 60 minutes to repeat time."
                );
                add_Minutes(60);
                break;
            }
            break;
          case 2:
            switch (progress.correct_answers_in_a_row) {
              case 1:
                console.log(
                  "learning stage 2 | Correct in a row 1: Adding 2 day to repeat time."
                );
                add_Days(2);
                break;
              case 2:
                console.log(
                  "learning stage 2 | Correct in a row 2: Adding 3 day to repeat time."
                );
                add_Days(3);
                break;
              case 3:
                console.log(
                  "learning stage 2 | Correct in a row 3: Adding 4 day to repeat time."
                );
                add_Days(4);
                break;
              case 4:
                console.log(
                  "learning stage 2 | Correct in a row 4: Adding 5 day to repeat time."
                );
                add_Days(5);
                break;
            }
            break;
          case 3:
            switch (progress.correct_answers_in_a_row) {
              case 1:
                console.log(
                  "learning stage 3 | Correct in a row 1: Adding 1 week to repeat time."
                );
                add_Weeks(1);
                break;
              case 2:
                console.log(
                  "learning stage 3 | Correct in a row 2: Adding 2 week to repeat time."
                );
                add_Weeks(2);
                break;
              case 3:
                console.log(
                  "learning stage 3 | Correct in a row 3: Adding 3 week to repeat time."
                );
                add_Weeks(3);
                break;
              case 4:
                console.log(
                  "learning stage 3 | Correct in a row 4: Adding 4 week to repeat time."
                );
                add_Weeks(4);
                break;
            }
            break;
          case 4:
            switch (progress.correct_answers_in_a_row) {
              case 1:
                console.log(
                  "learning stage 4 | Correct in a row 1: Adding 1 month to repeat time."
                );
                add_Months(1);
                break;
              case 2:
                console.log(
                  "learning stage 4 | Correct in a row 2: Adding 2 month to repeat time."
                );
                add_Months(2);
                break;
              case 3:
                console.log(
                  "learning stage 4 | Correct in a row 3: Adding 3 month to repeat time."
                );
                add_Months(3);
                break;
              case 4:
                console.log(
                  "learning stage 4 | Correct in a row 4: Adding 4 month to repeat time."
                );
                add_Months(4);
                break;

              default:
                console.log(
                  `Adding ${
                    progress.correct_answers_in_a_row
                  } month to repeat time.`
                );
                add_Months(progress.correct_answers_in_a_row);
                break;
            }
        }
      } else {
        if (progress.learning_stage === 1) {
          console.log("Adding 5 minutes to repeat time.");
          add_Minutes(5);
        } else {
          switch (progress.wrong_answers_in_a_row) {
            case 1:
              console.log("Adding 60 minutes to repeat time.");
              add_Minutes(60);
              break;
            case 2:
              console.log("Adding 30 minutes to repeat time.");
              add_Minutes(30);
              break;
            case 3:
              console.log("Adding 15 minutes to repeat time.");
              add_Minutes(15);
              break;
            case 4:
              console.log("Adding 10 minutes to repeat time.");
              add_Minutes(10);
              break;
          }
        }
      }
    };

    const { correct, incorrect, extraCorrect, extraIncorrect } =
      calculateIndexes(word, userAnswer);

    if (
      correct.length === word.word.length &&
      extraCorrect.length === 0 &&
      extraIncorrect.length === 0
    ) {
      answerLogic(progress, true);
      addingTimeToRepeat(progress, true);
    } else {
      answerLogic(progress, false);
      addingTimeToRepeat(progress, false);
    }

    setCorrectIndexes(correct);
    setIncorrectIndexes(incorrect);
    setExtraCorrectIndexes(extraCorrect);
    setExtraIncorrectIndexes(extraIncorrect);
  }, [word.word, userAnswer]);

  return (
    <>
      <div className="quiz-answers-container">
        <div className="quiz-correct-answer">
          {word.word.split("").map((l, index) => (
            <span
              key={index}
              className={`quiz-letter ${
                correctIndexes.includes(index)
                  ? "correct"
                  : incorrectIndexes.includes(index)
                  ? "incorrect"
                  : extraCorrectIndexes.includes(index)
                  ? "extra-correct"
                  : ""
              }`}
            >
              {l}
            </span>
          ))}
          {extraIncorrectIndexes.length > 0 &&
            extraIncorrectIndexes.map((index) => (
              <span
                key={`extra-correct-${index}`}
                className="quiz-letter extra-letter"
              >
                .
              </span>
            ))}
        </div>
        <div className="quiz-user-answer">
          {(userAnswer || "").split("").map((l, index) => (
            <span
              key={index}
              className={`quiz-letter ${
                correctIndexes.includes(index)
                  ? "correct"
                  : incorrectIndexes.includes(index)
                  ? "extra-incorrect"
                  : extraIncorrectIndexes.includes(index)
                  ? "extra-incorrect"
                  : ""
              }`}
            >
              {l}
            </span>
          ))}
          {extraCorrectIndexes.length > 0 &&
            extraCorrectIndexes.map((index) => (
              <span
                key={`extra-incorrect-${index}`}
                className="quiz-letter extra-letter"
              >
                .
              </span>
            ))}
        </div>
      </div>
    </>
  );
}

export default QuizResult;
