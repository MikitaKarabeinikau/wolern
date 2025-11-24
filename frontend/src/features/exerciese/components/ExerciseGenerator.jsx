import React from "react";
import { useExerciseGenerator } from "../hooks/useExerciseGenerator";
import QuotaDisplay from "./QuotaDisplay";
import ExerciseGeneratorForm from "./ExerciseGeneratorForm";
import GeneratedExerciseView from "./GeneratedExerciseView";

function ExerciseGenerator() {
  const {
    exercises,
    difficulty,
    setDifficulty,
    quota,
    currentWord,
    isLoading,
    error,
    isGenerated,
    resetTrigger,
    handleGenerate,
    handleGenerateAnother,
  } = useExerciseGenerator();

  const isQuotaExhausted = quota?.exercises_remaining === 0;
  const canGenerate = !isLoading && !isQuotaExhausted && currentWord;

  return (
    <div className="generator-card">
      <QuotaDisplay quota={quota} />

      {isGenerated && exercises ? (
        <GeneratedExerciseView
          currentWord={currentWord}
          exercise={exercises.exercise}
          resetTrigger={resetTrigger}
          isLoading={isLoading}
          onGenerateAnother={handleGenerateAnother}
        />
      ) : (
        <ExerciseGeneratorForm
          currentWord={currentWord}
          difficulty={difficulty}
          setDifficulty={setDifficulty}
          isLoading={isLoading}
          error={error}
          canGenerate={canGenerate}
          onGenerate={handleGenerate}
        />
      )}
    </div>
  );
}

export default ExerciseGenerator;
