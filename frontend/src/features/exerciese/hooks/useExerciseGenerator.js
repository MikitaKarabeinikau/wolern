import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@clerk/clerk-react";
import { apiClient } from "../../../api/apiClient";

const API_ENDPOINTS = {
  WORDS: "/exercise/words",
  QUOTA: "/quota",
  GENERATE: (wordId) => `/exercise/generate-exercise/${wordId}`,
};

export const useExerciseGenerator = () => {
  const { getToken } = useAuth();

  const [exercises, setExercises] = useState(null);
  const [difficulty, setDifficulty] = useState("Beginner");
  const [quota, setQuota] = useState(null);
  const [wordList, setWordList] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isGenerated, setIsGenerated] = useState(false);
  const [resetTrigger, setResetTrigger] = useState(0);

  const currentWord = wordList[currentIndex] || null;

  const fetchQuota = useCallback(async () => {
    try {
      const data = await apiClient(API_ENDPOINTS.QUOTA, getToken);
      setQuota(data);
    } catch (err) {
      console.error("Error fetching quota:", err);
      setError(err.message);
    }
  }, [getToken]);

  const fetchWords = useCallback(async () => {
    try {
      const data = await apiClient(API_ENDPOINTS.WORDS, getToken);

      if (data.words && data.words.length > 0) {
        setWordList(data.words);
        setCurrentIndex(0);
      } else {
        setError("No words available for exercises");
      }
    } catch (err) {
      console.error("Error fetching words:", err);
      setError(err.message);
    }
  }, [getToken]);


  useEffect(() => {
    fetchQuota();
    fetchWords();
  }, [fetchQuota, fetchWords]);

  const handleNextWord = useCallback(() => {
    if (currentIndex + 1 >= wordList.length) {
      fetchWords();
    } else {
      setCurrentIndex((prev) => prev + 1);
    }
  }, [currentIndex, wordList.length, fetchWords]);

  const handleGenerate = useCallback(async () => {
    if (!currentWord) return;

    setIsLoading(true);
    setError(null);

    try {
      const data = await apiClient(
        API_ENDPOINTS.GENERATE(currentWord.id),
        getToken,
        {
          method: "POST",
          body: JSON.stringify({
            word: currentWord.word,
            difficulty,
          }),
        }
      );

      setExercises(data);
      setIsGenerated(true);
      await fetchQuota();
    } catch (err) {
      console.error("Error generating exercise:", err);
      setError(err.message || "Failed to generate exercise");
    } finally {
      setIsLoading(false);
    }
  }, [currentWord, difficulty, getToken, fetchQuota]);

  const handleGenerateAnother = useCallback(() => {
    setIsGenerated(false);
    setExercises(null);
    setResetTrigger((prev) => prev + 1);
    handleNextWord();
  }, [handleNextWord]);

  return {
    exercises,
    difficulty,
    setDifficulty,
    quota,
    currentWord,
    isLoading,
    error,
    isGenerated,
    resetTrigger,
    handleGenerate,
    handleGenerateAnother,
  };
};
