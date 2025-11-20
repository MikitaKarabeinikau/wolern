import React, { useState, useEffect, useMemo, useRef } from "react";
import { useAuth } from "@clerk/clerk-react";
import "../../../../styles/QuizAnswerUnit.css";
import { calculateIndexes } from "../../../utils/wordProcessing";
import { createWordApi } from "../api/quizApi";
import { useAnswerHandler } from "../hooks/useAnswerHandler";
import { useScheduler } from "../hooks/useScheduler";

function QuizResult({ word_id, word, userAnswer, progress }) {
  const { getToken } = useAuth();
  const wordApi = createWordApi(getToken);
  const { handleCorrectAnswer, handleWrongAnswer } = useAnswerHandler(word_id);
  const { scheduleNextReview } = useScheduler(word_id);

  // Use ref to track if this answer has been processed
  const processedRef = useRef(null);

  // Calculate indexes immediately
  const {
    correct: correctIndexes,
    incorrect: incorrectIndexes,
    extraCorrect: extraCorrectIndexes,
    extraIncorrect: extraIncorrectIndexes,
    isEmpty,
  } = useMemo(() => {
    if (!userAnswer) {
      return {
        correct: [],
        incorrect: [],
        extraCorrect: [],
        extraIncorrect: [],
        isEmpty: true,
      };
    }
    return calculateIndexes(word.word, userAnswer);
  }, [word.word, userAnswer]);

  useEffect(() => {
    // Create unique key for this answer
    const answerKey = `${word_id}-${userAnswer}`;

    // Skip if already processed
    if (!userAnswer || processedRef.current === answerKey) {
      return;
    }

    const processAnswer = async () => {
      // Mark as processing immediately
      processedRef.current = answerKey;

      try {
        if (word.vocabulary === "new") {
          await wordApi.changeVocabulary(word_id);
        }

        const isCorrectAnswer =
          correctIndexes.length === word.word.length &&
          extraCorrectIndexes.length === 0 &&
          extraIncorrectIndexes.length === 0;

        const updatedProgress = { ...progress };

        if (isCorrectAnswer) {
          await handleCorrectAnswer(updatedProgress);
        } else {
          await handleWrongAnswer(updatedProgress);
        }

        await scheduleNextReview(updatedProgress, isCorrectAnswer);
      } catch (error) {
        console.error("Error processing answer:", error);
        // Reset on error so user can retry
        processedRef.current = null;
      }
    };

    processAnswer();
  }, [
    word_id,
    userAnswer,
    correctIndexes.length,
    extraCorrectIndexes.length,
    extraIncorrectIndexes.length,
    word.word.length,
  ]);

  return (
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
  );
}

export default QuizResult;
