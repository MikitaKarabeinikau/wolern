import { apiClient } from "../../../api/apiClient";
import { useAuth } from "@clerk/clerk-react";
import { useCallback, useState } from "react";

export function useVocabularies() {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [vocabularies, setVocabularies] = useState([]);
  const { getToken } = useAuth();

  const getVocabularies = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
            const token = await getToken(); 

      // Retrieve the token before making the API call
      const vocabulariesData = await apiClient("/user/vocabularies", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      console.log("Fetched vocabularies data from useVocabularies:", vocabulariesData);

      setVocabularies(vocabulariesData.vocabularies );
    } catch (err) {
      setError(err.message || "Failed to fetch vocabularies.");
    } finally {
      setIsLoading(false);
    }
  }, [getToken]);

  return { getVocabularies, vocabularies, error, isLoading };
}