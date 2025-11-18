import React, { useEffect, useState } from "react";
import { useAuth } from "@clerk/clerk-react";
import ExerciseField from "./ExerciseField";

const GeneratedBase = () => {
  const { getToken } = useAuth();
  const [generatedExercisesList, setGeneratedExercisesList] = useState([]);
  const [exercise, setExercise] = useState(null);
  const [multipleChoice, setMultipleChoice] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [resetTrigger, setResetTrigger] = useState(false); // Add reset trigger state

  // Fetch exercises when the component mounts
  useEffect(() => {
    fetchGeneratedExercises();
  }, []);

  // Fetch exercises from the backend
  const fetchGeneratedExercises = async () => {
    try {
      const token = await getToken();
      const response = await fetch(
        "http://localhost:8000/exercise/generated/",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response from server:", errorText);
        throw new Error("Failed to fetch generated exercises");
      }

      const data = await response.json();
      setGeneratedExercisesList(data.exercises);
      setIsLoaded(true);
      console.log("Fetched generated exercises:", data.exercises);

      // Automatically load the first exercise
      if (data.exercises.length > 0) {
        getNextExercise(data.exercises);
      }
    } catch (err) {
      console.error("Error fetching generated exercises:", err);
    }
  };

  // Load the next exercise
  const getNextExercise = (exercisesList = generatedExercisesList) => {
    if (!exercisesList || exercisesList.length === 0) {
      console.warn("No exercises available. Refetching...");
      setIsLoaded(false);
      fetchGeneratedExercises();
      return;
    }

    const randomIndex = getRandomIndex(exercisesList.length);
    const selectedExercise = exercisesList[randomIndex];

    setExercise(selectedExercise);
    setMultipleChoice(selectedExercise?.multiple_choice);

    // Remove the selected exercise from the list
    const updatedExercisesList = [...exercisesList];
    updatedExercisesList.splice(randomIndex, 1);
    setGeneratedExercisesList(updatedExercisesList);

    console.log("Remaining exercises:", updatedExercisesList.length);

    // Trigger reset for ExerciseField
    setResetTrigger((prev) => !prev); // Toggle reset trigger
  };

  // Generate a random index
  const getRandomIndex = (arrayLength) => {
    return Math.floor(Math.random() * arrayLength);
  };

  return (
    <>
      <div>
        {isLoaded && exercise ? (
          <ExerciseField
            word={exercise?.word}
            exercise={exercise}
            resetTrigger={resetTrigger} // Pass reset trigger to ExerciseField
          />
        ) : (
          <p>Loading exercise...</p>
        )}
      </div>
      <button
        className="btn"
        onClick={() => getNextExercise()}
        disabled={!isLoaded}
      >
        Next Exercise
      </button>
    </>
  );
};

export default GeneratedBase;
