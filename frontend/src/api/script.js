

import axiosClient from "./axiosClient";

const scriptAPI = {
  get_recommended_questions: (playerId) => {
    const url = `/get_recommended_questions/${playerId}`;
    return axiosClient.get(url);
  },
  open_video: (playerId, recommendedQuestionId) => {
    const url = `/openVideo/${playerId}/${recommendedQuestionId}`;
    return axiosClient.get(url)
  },
  recommend: (playerId) => {
    const url = `/recommend`;
    return axiosClient.post(url, {player_id: playerId})
  },
  get_infor: (playerId) => {
    const url = `/get_infor/${playerId}`;
    return axiosClient.get(url)
  },
  get_id: (number) => {
    const url = `/get_id`;
    return axiosClient.post(url, {number: number})
  },
  get_question: (playerId, recommendedQuestionId) => {
    const url = `/get_question/${playerId}`;
    return axiosClient.post(url, {question_id : recommendedQuestionId})
  }
};

export default scriptAPI;
