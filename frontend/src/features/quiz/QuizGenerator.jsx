import React, { useState, useEffect, useMemo, useCallback } from "react";
import { useAuth } from "@clerk/clerk-react";
import QuizWord from "./QuizWord";
import QuizAnswerField from "./components/QuizAnswerField";
import QuizResult from "./components/QuizResult";
import DebugQuizTable from "./components/DebugQuizTable";
import { createMapByWordId } from "../../utils/wordProcessing";
import { apiClient } from "../../api/apiClient";
import { useQuizData } from "./hooks/useQuizData";

const QUIZ_ENDPOINTS = {
  translations: "/quiz/word/translations",
  definitions: "/quiz/word/definitions",
  examples: "/quiz/word/examples",
  synonyms: "/quiz/word/synonyms",
  words: "/quiz/generate",
  progress: "/quiz/data",
};

export function QuizGenerator() {
  const { getToken } = useAuth();

  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const {
    words,
    progress,
    translation,
    definition,
    example,
    synonym,
    isLoading,
    error,
    refetch,
  } = useQuizData();
  const [isAnswered, setIsAnswered] = useState(false);
  const [userAnswer, setUserAnswer] = useState(null);

  const currentWord = useMemo(
    () => words[currentWordIndex],
    [words, currentWordIndex]
  );

  const currentProgress = useMemo(
    () => progress.find((p) => p.word_id === currentWord?.id),
    [progress, currentWord]
  );

  const debugData = useMemo(() => {
    if (!words.length || !progress.length) return [];

    const progressMap = new Map(progress.map((p) => [p.word_id, p]));
    return words.map((word) => ({
      ...word,
      progress: progressMap.get(word.id) || {},
    }));
  }, [words, progress]);

  const handleCheckAnswer = useCallback((answer) => {
    setUserAnswer(answer);
    setIsAnswered(true);
  }, []);

  const handleNextQuestion = useCallback(() => {
    setIsAnswered(false);
    setUserAnswer(null);

    if (currentWordIndex + 1 >= words.length) {
      refetch();
      setCurrentWordIndex(0);
    } else {
      setCurrentWordIndex((prevIndex) => prevIndex + 1);
    }
  }, [currentWordIndex, words.length, refetch]);

  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === "Enter" && isAnswered) {
        handleNextQuestion();
      }
    },
    [isAnswered, handleNextQuestion]
  );

  if (error) {
    return (
      <div style={{ padding: "20px", color: "red" }}>
        <h3>Error loading quiz</h3>
        <p>{error}</p>
        <button onClick={fetchQuizData}>Retry</button>
      </div>
    );
  }

  if (isLoading) {
    return <div style={{ padding: "20px" }}>Loading quiz...</div>;
  }

  if (!words.length) {
    return <div style={{ padding: "20px" }}>No quiz words available.</div>;
  }

  return (
    <div style={{ display: "flex", flexDirection: "row" }}>
      <div style={{ flex: 2, padding: "20px" }}>
        {!isAnswered ? (
          <>
            <QuizWord
              word={currentWord}
              wordTranslation={translation[currentWord.id]}
              wordExample={example[currentWord.id]}
              wordDefinition={definition[currentWord.id]}
              wordSynonym={synonym[currentWord.id]}
              wordProgress={currentProgress}
            />
            <QuizAnswerField onCheckAnswer={handleCheckAnswer} />
          </>
        ) : (
          <>
            <QuizResult
              word_id={currentWord.id}
              word={currentWord}
              userAnswer={userAnswer}
              progress={currentProgress}
            />
            <button
              onClick={handleNextQuestion}
              onKeyDown={handleKeyDown}
              autoFocus
            >
              Next Question (Press Enter)
            </button>
          </>
        )}

        <DebugQuizTable data={debugData} />
      </div>
    </div>
  );
}
