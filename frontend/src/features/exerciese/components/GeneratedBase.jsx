import React from "react";
import { useAuth } from "@clerk/clerk-react";

const GeneratedBase = () => {
  const { getToken } = useAuth();

  const fetchGeneratedExercises = async () => {
    // Placeholder for fetching logic\
    try {
      const token = await getToken();
      const response = await fetch("/exercise/generated/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error("Failed to fetch generated exercises");
      }
      const data = await response.json();
      console.log("Fetched generated exercises:", data);
      // Handle the fetched data as needed
    } catch (err) {
      console.log("Error fetching generated exercises:", err);
    }
  };
  return (
    <div>
      <h2>Base of Exercises</h2>
    </div>
  );
};

export default GeneratedBase;
