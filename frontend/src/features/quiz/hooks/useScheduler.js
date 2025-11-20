import { useAuth } from "@clerk/clerk-react";
import { createQuizApi } from '../api/quizApi';
import { 
  LEARNING_STAGES, 
  WRONG_ANSWER_MINUTES, 
  FIRST_STAGE_RETRY_MINUTES 
} from '../constants/learningStages';

export const useScheduler = (word_id) => {
  const { getToken } = useAuth();
  const quizApi = createQuizApi(getToken);

  const addTime = async (type, value) => {
    const date = new Date();
    
    switch (type) {
      case 'minutes':
        date.setMinutes(date.getMinutes() + value);
        break;
      case 'days':
        date.setDate(date.getDate() + value);
        break;
      case 'weeks':
        date.setDate(date.getDate() + value * 7);
        break;
      case 'months':
        date.setMonth(date.getMonth() + value);
        break;
    }
    
    return await quizApi.setNextReviewDate(word_id, date);
  };

  const scheduleNextReview = async (progress, isCorrect) => {
    const stage = progress.learning_stage;
    const count = isCorrect 
      ? progress.correct_answers_in_a_row 
      : progress.wrong_answers_in_a_row;

    if (isCorrect) {
      const config = LEARNING_STAGES[stage];
      if (!config) return;
      
      const [timeType] = Object.keys(config);
      const timeValue = config[timeType][count - 1] || config[timeType][config[timeType].length - 1];
      
      await addTime(timeType, timeValue);
    } else {
      if (stage === 1) {
        await addTime('minutes', FIRST_STAGE_RETRY_MINUTES);
      } else {
        const minutes = WRONG_ANSWER_MINUTES[count - 1] || WRONG_ANSWER_MINUTES[WRONG_ANSWER_MINUTES.length - 1];
        await addTime('minutes', minutes);
      }
    }
  };

  return { scheduleNextReview };
};