import { apiCall } from '../../../api/apiClient';

const API_BASE_URL = "http://localhost:8000";

export const createQuizApi = (getToken) => ({
  correctAnswers: (word_id) => 
    apiCall(`${API_BASE_URL}/quiz/words/${word_id}/correct-answers`, getToken, "PUT"),
  
  wrongAnswers: (word_id) => 
    apiCall(`${API_BASE_URL}/quiz/words/${word_id}/wrong-answers`, getToken, "PUT"),
  
  learningStage: {
    increase: (word_id) => 
      apiCall(`${API_BASE_URL}/quiz/words/${word_id}/learning-stage/increase`, getToken, "PUT"),
    decrease: (word_id) => 
      apiCall(`${API_BASE_URL}/quiz/words/${word_id}/learning-stage/decrease`, getToken, "PUT"),
  },
  
  correctInRow: {
    increase: (word_id) => 
      apiCall(`${API_BASE_URL}/quiz/words/${word_id}/correct-answers-row/increase`, getToken, "PUT"),
    reset: (word_id) => 
      apiCall(`${API_BASE_URL}/quiz/words/${word_id}/correct-answers-row/reset`, getToken, "PUT"),
  },
  
  wrongInRow: {
    increase: (word_id) => 
      apiCall(`${API_BASE_URL}/quiz/words/${word_id}/wrong-answers-row/increase`, getToken, "PUT"),
    reset: (word_id) => 
      apiCall(`${API_BASE_URL}/quiz/words/${word_id}/wrong-answers-row/reset`, getToken, "PUT"),
  },
  
  setNextReviewDate: (word_id, date) =>
    apiCall(`${API_BASE_URL}/quiz/words/${word_id}/set-next-review-date`, getToken, "PUT", {
      new_date: date.toISOString(),
    }),
});

export const createWordApi = (getToken) => ({
  changeVocabulary: (word_id) =>
    apiCall(`${API_BASE_URL}/words/${word_id}/vocabulary/to_learn`, getToken, "PUT"),
});