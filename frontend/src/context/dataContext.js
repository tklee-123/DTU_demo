import { createContext, useState, useEffect } from "react";
import axios from "axios";

const DataContext = createContext({});

export const DataProvider = ({children}) => {
      // All Quizs, Current Question, Index of Current Question, Answer, Selected Answer, Total Marks
  const baseURL = 'http://localhost:8000/';
  const [user, setUser] = useState(null);
  const [quizs, setQuizs] = useState([]);
  const [question, setQuesion] = useState({});
  const [questionIndex, setQuestionIndex] = useState(0);
  const [correctAnswer, setCorrectAnswer] = useState('');
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [marks, setMarks] = useState(0);
  const [interaction, setInteraction] = useState([]);

  // Display Controlling States
  const [showStart, setShowStart] = useState(true);
  const [showQuiz, setShowQuiz] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [timer, setTimer] = useState(60);

  // Set a Single Question
  useEffect(() => {
    if (quizs.length > questionIndex) {
      setQuesion(quizs[questionIndex]);
    }
  }, [quizs, questionIndex])

  const updateInteraction = (time, outcome) => {
    setInteraction([...interaction, {player_id: user._id, 
      question_id: question.id, 
      time: time, 
      outcome: outcome,
      category: question.category,
      difficulty: question.difficulty,
      major: user.major,
      rank: user.rank,}]);
    console.log(interaction);
  };

  // Start Quiz
  const startQuiz = async (userID) => {
    await axios.get(`${baseURL}get_infor/${userID}`).then(res => setUser(res.data));
    await axios.post(`${baseURL}recommend`, {player_id: userID}).then(res => {
      axios.post(`${baseURL}get_question`, {question_id: res.data}).then(res => {
        setQuizs(res.data);
    }).then(() => {
      setShowStart(false);
      setShowQuiz(true);
      setQuestionIndex(0);
      setTimer(60);
    })});
  }

  // Check Answer
  const checkAnswer = (event, selected, time) => {
    if (!selectedAnswer) {
      setCorrectAnswer(question.answer);
      setSelectedAnswer(selected);

      if (selected === question.answer) {
        event.target.classList.add('bg-success');
        setMarks(marks + 1);
        updateInteraction(time, 1);
      } else {
        event.target.classList.add('bg-danger');
        updateInteraction(time, 0);
      }
    }
  }

  // Next Quesion
  const nextQuestion = () => {
    setTimer(60);
    setCorrectAnswer('');
    setSelectedAnswer('');
    const wrongBtn = document.querySelector('button.bg-danger');
    wrongBtn?.classList.remove('bg-danger');
    const rightBtn = document.querySelector('button.bg-success');
    rightBtn?.classList.remove('bg-success');
    setQuestionIndex(questionIndex + 1);
  }

  // Show Result
  const showTheResult = () => {
    try {
      axios.post(`${baseURL}recommend_with_data`, interaction).then(res => {
        axios.post(`${baseURL}get_question`, {question_id: res.data[user._id]}).then(res => {
          setQuizs(res.data);
      })
      });
    } catch (error) {
      console.log(error);
    }
    setShowResult(true);
    setShowStart(false);
    setShowQuiz(false);
  }

  // Start Over
  const startOver = () => {
    setInteraction([]);
    setShowStart(false);
    setShowResult(false);
    setShowQuiz(true);
    setCorrectAnswer('');
    setSelectedAnswer('');
    setQuestionIndex(0);
    setMarks(0);
    const wrongBtn = document.querySelector('button.bg-danger');
    wrongBtn?.classList.remove('bg-danger');
    const rightBtn = document.querySelector('button.bg-success');
    rightBtn?.classList.remove('bg-success');
  }
    return (
        <DataContext.Provider value={{
            startQuiz,showStart,showQuiz,question,quizs,checkAnswer,correctAnswer,
            selectedAnswer,questionIndex,nextQuestion,showTheResult,showResult,marks,
            startOver, user, timer, setTimer
        }} >
            {children}
        </DataContext.Provider>
    );
}

export default DataContext;

