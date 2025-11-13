import React, { useState, useEffect, useMemo } from "react";
import "../../../../styles/QuizAnswerUnit.css";
import { useQuizApi } from "../hooks/useQuizApi";

// --- Configuration for Spaced Repetition ---
const repeatIntervals = {
  // [learning_stage]: { [correct_answers_in_a_row]: { unit: 'minutes'/'days'/'weeks'/'months', value: X } }
  1: {
    1: { unit: "minutes", value: 10 },
    2: { unit: "minutes", value: 15 },
    3: { unit: "minutes", value: 30 },
    4: { unit: "minutes", value: 60 },
  },
  2: {
    1: { unit: "days", value: 2 },
    2: { unit: "days", value: 3 },
    3: { unit: "days", value: 4 },
    4: { unit: "days", value: 5 },
  },
  3: {
    1: { unit: "weeks", value: 1 },
    2: { unit: "weeks", value: 2 },
    3: { unit: "weeks", value: 3 },
    4: { unit: "weeks", value: 4 },
  },
  4: {
    1: { unit: "months", value: 1 },
    2: { unit: "months", value: 2 },
    3: { unit: "months", value: 3 },
    4: { unit: "months", value: 4 },
  },
};

// --- Helper Functions ---
const calculateIndexes = (word, userAnswer) => {
  const correct = [],
    incorrect = [],
    extraCorrect = [],
    extraIncorrect = [];
  const safeUserAnswer = userAnswer || "";
  const maxLength = Math.max(word.length, safeUserAnswer.length);

  for (let i = 0; i < maxLength; i++) {
    const wordChar = word[i] || null;
    const userChar = safeUserAnswer[i] || null;

    if (wordChar && userChar) {
      wordChar === userChar ? correct.push(i) : incorrect.push(i);
    } else if (wordChar) {
      extraCorrect.push(i);
    } else if (userChar) {
      extraIncorrect.push(i);
    }
  }
  return { correct, incorrect, extraCorrect, extraIncorrect };
};

const addTime = (date, unit, value) => {
  const newDate = new Date(date);
  if (unit === "minutes") newDate.setMinutes(newDate.getMinutes() + value);
  if (unit === "days") newDate.setDate(newDate.getDate() + value);
  if (unit === "weeks") newDate.setDate(newDate.getDate() + value * 7);
  if (unit === "months") newDate.setMonth(newDate.getMonth() + value);
  return newDate;
};

// --- Main Component ---
function QuizResult({ word_id, word, userAnswer, progress }) {
  const { updateWordStat, resetWordStat, setNextReviewDate, changeVocabulary } =
    useQuizApi(word_id);

  const [indexes, setIndexes] = useState({
    correct: [],
    incorrect: [],
    extraCorrect: [],
    extraIncorrect: [],
  });

  const isCorrect = useMemo(() => {
    if (!word || !userAnswer) return false;
    return word.word === userAnswer;
  }, [word.word, userAnswer]);

  // --- Logic for Correct Answer ---
  const handleCorrectAnswer = () => {
    console.log("Answer is correct, processing...");
    updateWordStat("correct-answers", "increase");
    updateWordStat("correct-answers-row", "increase");
    resetWordStat("wrong-answers-row");

    if (
      progress.correct_answers_in_a_row + 1 >= 4 &&
      progress.learning_stage < 4
    ) {
      console.log("Promoting to next learning stage.");
      updateWordStat("learning-stage", "increase");
      resetWordStat("correct-answers-row");
    }

    // Set next review date
    const stage = progress.learning_stage;
    const rowCount = Math.min(progress.correct_answers_in_a_row + 1, 4);
    const interval = repeatIntervals[stage]?.[rowCount];
    if (interval) {
      const nextReviewDate = addTime(new Date(), interval.unit, interval.value);
      setNextReviewDate(nextReviewDate);
    }
  };

  // --- Logic for Incorrect Answer ---
  const handleIncorrectAnswer = () => {
    console.log("Answer is incorrect, processing...");
    updateWordStat("wrong-answers", "increase");
    updateWordStat("wrong-answers-row", "increase");
    resetWordStat("correct-answers-row");

    if (
      progress.wrong_answers_in_a_row + 1 >= 4 &&
      progress.learning_stage > 1
    ) {
      console.log("Demoting to previous learning stage.");
      updateWordStat("learning-stage", "decrease");
      resetWordStat("wrong-answers-row");
    }

    // Set next review date (penalty)
    const penaltyDate = addTime(new Date(), "minutes", 5);
    setNextReviewDate(penaltyDate);
  };

  useEffect(() => {
    if (word.vocabulary === "new") {
      changeVocabulary("to_learn");
    }
    if (!userAnswer) return;

    setIndexes(calculateIndexes(word.word, userAnswer));

    if (isCorrect) {
      handleCorrectAnswer();
    } else {
      handleIncorrectAnswer();
    }
  }, [word.word, userAnswer]); // Dependencies are simplified

  // --- Rendering ---
  const renderLetters = (text, type) => {
    return text.split("").map((char, index) => {
      let className = "quiz-letter";
      if (indexes.correct.includes(index)) className += " correct";
      else if (indexes.incorrect.includes(index))
        className += type === "user" ? " extra-incorrect" : " incorrect";
      else if (indexes.extraCorrect.includes(index))
        className += " extra-correct";

      return (
        <span key={index} className={className}>
          {char}
        </span>
      );
    });
  };

  return (
    <div className="quiz-answers-container">
      <div className="quiz-correct-answer">
        {renderLetters(word.word, "correct")}
      </div>
      <div className="quiz-user-answer">
        {renderLetters(userAnswer || "", "user")}
      </div>
    </div>
  );
}

export default QuizResult;
