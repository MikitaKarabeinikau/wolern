import { useAuth } from "@clerk/clerk-react";
import { useCallback } from "react";

export const useQuizApi = (word_id) => {
  const { getToken } = useAuth();

  const makeApiCall = useCallback(
    async (endpoint, method = "PUT", body = null) => {
      try {
        const token = await getToken();
        const response = await fetch(`http://localhost:8000/quiz/${endpoint}`, {
          method,
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: body ? JSON.stringify(body) : null,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log(`Successfully called ${method} on ${endpoint}`);
      } catch (error) {
        console.error(`Failed to call ${method} on ${endpoint}:`, error);
      }
    },
    [getToken]
  );

  const updateWordStat = (stat, action) =>
    makeApiCall(`words/${word_id}/${stat}/${action}`);
  const resetWordStat = (stat) => makeApiCall(`words/${word_id}/${stat}/reset`);
  const setNextReviewDate = (new_date) =>
    makeApiCall(`word/${word_id}/set_next_review_date`, "PUT", {
      new_date: new_date.toISOString(),
    });
  const changeVocabulary = (newVocabulary) =>
    fetch(
      `http://localhost:8000/words/${word_id}/vocabulary/${newVocabulary}`,
      {
        /* ...headers... */
      }
    );

  return { updateWordStat, resetWordStat, setNextReviewDate, changeVocabulary };
};
