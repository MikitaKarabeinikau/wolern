import axios from "axios";
import { useAuth } from "@clerk/clerk-react";
import { useCallback, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function useVocabularies() {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [vocabularies, setVocabularies] = useState([]);
  const { getToken } = useAuth();

  const getVocabularies = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Get the authentication token
      const token = await getToken();
      
      // Make the API request using axios
      const response = await axios.get(`${API_BASE_URL}/user/vocabularies`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        timeout: 10000, // 10 second timeout
      });

      console.log("Fetched vocabularies data from useVocabularies:", response.data);

      // Extract vocabularies from response
      const fetchedVocabularies = response.data.vocabularies || [];
      setVocabularies(fetchedVocabularies);
      
      return fetchedVocabularies;
    } catch (err) {
      let errorMessage = "Failed to fetch vocabularies.";
      
      if (axios.isAxiosError(err)) {
        if (err.response) {
          // Server responded with error status
          errorMessage = `Server error: ${err.response.status} - ${err.response.data?.message || err.response.statusText}`;
          console.error("API Error Response:", err.response.data);
        } else if (err.request) {
          // Request was made but no response received
          errorMessage = "Network error: Unable to reach server.";
          console.error("Network Error:", err.request);
        } else {
          // Something else happened
          errorMessage = `Request error: ${err.message}`;
          console.error("Request Error:", err.message);
        }
      } else {
        // Non-axios error (e.g., getToken failure)
        errorMessage = err.message || errorMessage;
        console.error("General Error:", err);
      }

      setError(errorMessage);
      setVocabularies([]);
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
    refetch
  };
}