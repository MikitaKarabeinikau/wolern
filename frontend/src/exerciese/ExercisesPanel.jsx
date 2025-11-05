import "react"
import Exercise from "./Exercise"
import ExerciseGenerator from "./ExerciseGenerator"

export function ExercisesPanel() {
  return (
    <div>
      <h1>Exercises Panel</h1>
      <ExerciseGenerator />
    </div>
  )
}