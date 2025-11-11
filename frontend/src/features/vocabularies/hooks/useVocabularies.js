import { useState, useEffect, useCallback, useMemo } from "react";
import { useAuth } from "@clerk/clerk-react";
import { apiClient } from "../../../api/apiClient";
import { createMapByWordId } from "../../../utils/wordProcessing";


export function useVocabularies() {
  const [words, setWords] = useState([]);
  const [vocabularies, setVocabularies] = useState([]);
  const [selectedVocabulary, setSelectedVocabulary] = useState(null);
  const [infoMaps, setInfoMaps] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const { getToken } = useAuth();

  const fetchAllData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Use apiClient for cleaner, parallel requests
      const [
        wordsData,
        translationsData,
        definitionsData,
        examplesData,
        synonymsData,
        warningsData,
        tagsData,
        vocabulariesData,
      ] = await Promise.all([
        apiClient("/user/words", getToken),
        apiClient("/user/words/translations/all", getToken),
        apiClient("/user/words/definitions/all", getToken),
        apiClient("/user/words/examples/all", getToken),
        apiClient("/user/words/synonyms/all", getToken),
        apiClient("/user/words/warnings/all", getToken),
        apiClient("/user/words/tags/all", getToken),
        apiClient("/user/vocabularies", getToken),
      ]);

      setWords(wordsData.words || []);
      setVocabularies(vocabulariesData.vocabularies || []);
      setInfoMaps({
        translationsMap: createMapByWordId(translationsData, "translations"),
        definitionsMap: createMapByWordId(definitionsData, "definitions"),
        examplesMap: createMapByWordId(examplesData, "examples"),
        synonymsMap: createMapByWordId(synonymsData, "synonyms"),
        warningsMap: createMapByWordId(warningsData, "warnings"),
        tagsMap: createMapByWordId(tagsData, "tags"),
      });
    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  }, [getToken]);

  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  // Memoize the filtered words to prevent re-calculating on every render
  const filteredWords = useMemo(() => {
    if (!selectedVocabulary) {
      return words;
    }
    return words.filter((word) => word.vocabulary === selectedVocabulary);
  }, [words, selectedVocabulary]);

  return {
    isLoading,
    error,
    words: filteredWords,
    vocabularies,
    infoMaps,
    selectedVocabulary,
    handleVocabularySelect: setSelectedVocabulary, // Directly expose the setter
    handleWordAdded: fetchAllData, // Expose the refetch function
    getToken, // Pass getToken down if child components need it directly
  };
}