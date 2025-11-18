import {apiClient} from "../../../api/apiClient";
import {useAuth} from "@clerk/clerk-react";
import {useCallback, useState} from "react";

export function useAddWord(onWordAdded) {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const {getToken} = useAuth();

  const addWord = useCallback(
    async (word, vocabulary, onSuccess) => {
      if (!word.trim()) return; // Prevent empty submissions
      setIsLoading(true);
      setError(null);

      try {
        await apiClient(`/user/${word}/vocabulary/${vocabulary}`, getToken, {
          method: "POST",
          body: JSON.stringify({word}),
        });

        if (onWordAdded) {
          onWordAdded(); // Refresh parent data
        }

        if (onSuccess) {
          onSuccess(); // Callback for success (e.g., clearing input)
        }
      } catch (err) {
        setError(err.message || "Failed to add word.");
      } finally {
        setIsLoading(false);
      }
    },
    [getToken, onWordAdded]
  );

  return {addWord, error, isLoading};
}