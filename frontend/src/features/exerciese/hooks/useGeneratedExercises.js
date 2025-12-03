import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@clerk/clerk-react";
import { apiClient } from "../../../api/apiClient";

const API_ENDPOINTS = {
  GENERATED_EXERCISES: "/exercise/generated/",
};

export const useGeneratedExercises = () => {
  const { getToken } = useAuth();

  const [generatedExercisesList, setGeneratedExercisesList] = useState([]);
  const [currentExercise, setCurrentExercise] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [resetTrigger, setResetTrigger] = useState(0);

  const fetchGeneratedExercises = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await apiClient(
        API_ENDPOINTS.GENERATED_EXERCISES,
        getToken
      );

      if (data.exercises && data.exercises.length > 0) {
        setGeneratedExercisesList(data.exercises);
        // Automatically load the first exercise
        loadRandomExercise(data.exercises);
      } else {
        setError("No exercises available");
      }
    } catch (err) {
      console.error("Error fetching generated exercises:", err);
      setError(err.message || "Failed to fetch exercises");
    } finally {
      setIsLoading(false);
    }
  }, [getToken]);

  const loadRandomExercise = useCallback((exercisesList = generatedExercisesList) => {
    if (!exercisesList || exercisesList.length === 0) {
      fetchGeneratedExercises();
      return;
    }

    const randomIndex = Math.floor(Math.random() * exercisesList.length);
    const selectedExercise = exercisesList[randomIndex];

    setCurrentExercise(selectedExercise);

    // Remove the selected exercise from the list
    const updatedExercisesList = exercisesList.filter((_, index) => index !== randomIndex);
    setGeneratedExercisesList(updatedExercisesList);

    // Trigger reset for ExerciseField
    setResetTrigger((prev) => prev + 1);

    console.log("Remaining exercises:", updatedExercisesList.length);
  }, [generatedExercisesList, fetchGeneratedExercises]);

  useEffect(() => {
    fetchGeneratedExercises();
  }, [fetchGeneratedExercises]);

  const handleNextExercise = useCallback(() => {
    loadRandomExercise();
  }, [loadRandomExercise]);

  return {
    currentExercise,
    isLoading,
    error,
    resetTrigger,
    handleNextExercise,
    hasExercises: generatedExercisesList.length > 0,
  };
};
