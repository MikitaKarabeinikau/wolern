import {useAuth} from "@clerk/clerk-react";
import {useCallback, useState} from "react";
import {apiClient} from "../../../api/apiClient";

export function useScannerVocabularies() {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [vocabularies, setVocabularies] = useState([]);
  const {getToken} = useAuth();

  const getVocabularies = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await apiClient("/user/vocabularies", getToken, {
        method: "GET",
      });

      const fetchedVocabularies = data.vocabularies || [];
      setVocabularies(fetchedVocabularies);

      return fetchedVocabularies;
    } catch (err) {
      setError(err.message || "Failed to fetch vocabularies.");
      setVocabularies([]); // Ensure vocabularies are cleared on error
      return [];
    } finally {
      setIsLoading(false);
    }
  }, [getToken]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const refetch = useCallback(() => {
    return getVocabularies();
  }, [getVocabularies]);

  return {
    getVocabularies,
    vocabularies,
    error,
    isLoading,
    clearError,
    refetch,
  };
}
