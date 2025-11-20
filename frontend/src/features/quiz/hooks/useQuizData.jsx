import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@clerk/clerk-react";
import { apiClient } from "../../../api/apiClient";
import { createMapByWordId } from "../../../utils/wordProcessing";

const QUIZ_ENDPOINTS = {
  translations: "/quiz/word/translations",
  definitions: "/quiz/word/definitions",
  examples: "/quiz/word/examples",
  synonyms: "/quiz/word/synonyms",
  words: "/quiz/generate",
  progress: "/quiz/data",
};

export const useQuizData = () => {
  const { getToken } = useAuth();

  const [data, setData] = useState({
    words: [],
    progress: [],
    translation: {},
    definition: {},
    example: {},
    synonym: {},
  });

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchQuizData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const responses = await Promise.all([
        apiClient(QUIZ_ENDPOINTS.translations, getToken),
        apiClient(QUIZ_ENDPOINTS.definitions, getToken),
        apiClient(QUIZ_ENDPOINTS.examples, getToken),
        apiClient(QUIZ_ENDPOINTS.synonyms, getToken),
        apiClient(QUIZ_ENDPOINTS.words, getToken),
        apiClient(QUIZ_ENDPOINTS.progress, getToken),
      ]);

      const [
        translationsRes,
        definitionsRes,
        examplesRes,
        synonymsRes,
        wordsRes,
        progressRes,
      ] = responses;

      setData({
        translation: createMapByWordId(translationsRes, "translations"),
        definition: createMapByWordId(definitionsRes, "definitions"),
        example: createMapByWordId(examplesRes, "examples"),
        synonym: createMapByWordId(synonymsRes, "synonyms"),
        words: wordsRes.words || [],
        progress: progressRes.progress || [],
      });
    } catch (err) {
      setError(err.message || "Failed to load quiz data");
      console.error("Error fetching quiz data:", err);
    } finally {
      setIsLoading(false);
    }
  }, [getToken]);

  useEffect(() => {
    fetchQuizData();
  }, [fetchQuizData]);

  return { ...data, isLoading, error, refetch: fetchQuizData };
};
