import { useAuth } from "@clerk/clerk-react";
import { createQuizApi } from "../api/quizApi";

export const useAnswerHandler = (word_id) => {
  const { getToken } = useAuth();
  const quizApi = createQuizApi(getToken);

  const handleCorrectAnswer = async (progress) => {
    const isFirstCorrect = progress.wrong_answers_in_a_row === 0;
    const isFourthCorrect = progress.correct_answers_in_a_row === 4;
    const isMaxStage = progress.learning_stage === 4;

    if (isFirstCorrect) {
      if (isFourthCorrect && !isMaxStage) {
        await Promise.all([
          quizApi.learningStage.increase(word_id),
          quizApi.correctInRow.reset(word_id),
          quizApi.correctInRow.increase(word_id),
          quizApi.correctAnswers(word_id),
        ]);
        progress.correct_answers += 1;
        progress.correct_answers_in_a_row = 1;
        progress.learning_stage += 1;
      } else {
        await Promise.all([
          quizApi.correctInRow.increase(word_id),
          quizApi.correctAnswers(word_id),
        ]);
        progress.correct_answers += 1;
        progress.correct_answers_in_a_row += 1;
      }
    } else {
      await Promise.all([
        quizApi.wrongInRow.reset(word_id),
        quizApi.correctInRow.increase(word_id),
        quizApi.correctAnswers(word_id),
      ]);
      progress.correct_answers += 1;
      progress.wrong_answers_in_a_row = 0;
      progress.correct_answers_in_a_row += 1;
    }
  };

  const handleWrongAnswer = async (progress) => {
    const isFirstWrong = progress.correct_answers_in_a_row === 0;
    const isFourthWrong = progress.wrong_answers_in_a_row === 4;
    const isMinStage = progress.learning_stage === 1;

    if (isFirstWrong) {
      if (isFourthWrong && !isMinStage) {
        await Promise.all([
          quizApi.learningStage.decrease(word_id),
          quizApi.wrongInRow.reset(word_id),
          quizApi.wrongInRow.increase(word_id),
          quizApi.wrongAnswers(word_id),
        ]);
        progress.wrong_answers += 1;
        progress.wrong_answers_in_a_row = 1;
        progress.learning_stage -= 1;
      } else {
        await Promise.all([
          quizApi.wrongInRow.increase(word_id),
          quizApi.wrongAnswers(word_id),
        ]);
        progress.wrong_answers += 1;
        progress.wrong_answers_in_a_row += 1;
      }
    } else {
      await Promise.all([
        quizApi.correctInRow.reset(word_id),
        quizApi.wrongInRow.increase(word_id),
        quizApi.wrongAnswers(word_id),
      ]);
      progress.wrong_answers += 1;
      progress.correct_answers_in_a_row = 0;
      progress.wrong_answers_in_a_row += 1;
    }
  };

  return { handleCorrectAnswer, handleWrongAnswer };
};
