import HintUnit from "./HintUnit";

function ExerciseInputView({
  partOfSpeech,
  question,
  hints,
  userAnswer,
  setUserAnswer,
  handleAnswer,
  handleKeyPress,
}) {
  return (
    <div className="two-column">
      <div className="left-panelexercise">
        <div className="top-section">
          <div className="exercise-header">
            <span className="part-of-speech">{partOfSpeech}</span>
          </div>
        </div>
        <div className="middle-section">
          <p className="question">{question}</p>
        </div>
        <div className="bottom-section">
          <div className="answer-input-wrapper">
            <input
              type="text"
              placeholder="Type your answer..."
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              onKeyPress={handleKeyPress}
              autoFocus
            />
            <button onClick={handleAnswer} disabled={!userAnswer?.trim()}>
              Check
            </button>
          </div>
        </div>
      </div>

      <div className="right-panel-exercise">
        <div className="exercise-hints">
          <div className="hints-list">
            {hints?.map((hint, index) => (
              <HintUnit key={`hint-${index}`} index={index} hint={hint} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
export default ExerciseInputView;
