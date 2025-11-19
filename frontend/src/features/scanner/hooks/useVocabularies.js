import { apiClient } from "../../../api/apiClient";
import { useAuth } from "@clerk/clerk-react";
import { useCallback, useState } from "react";

export function useVocabularies() {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { getToken } = useAuth();

  const getVocabularies = useCallback(async (onSuccess) => {
    setIsLoading(true);
    setError(null);

    try {
      // Ensure the token is retrieved before making the API call
      const token = await getToken();
      const vocabulariesData = await apiClient("/user/vocabularies", token);
      console.log("Fetched vocabularies data from useVocabularies:", vocabulariesData);
      if (onSuccess) {
        onSuccess(vocabulariesData.vocabularies || []);
      }
      return vocabulariesData.vocabularies || [];
    } catch (err) {
      setError(err.message || "Failed to fetch vocabularies.");
      return [];
    } finally {
      setIsLoading(false);
    }
  }, [getToken]);

  return { getVocabularies, error, isLoading };
}