import React, { useContext, useState, useEffect } from 'react';
import DataContext from '../context/dataContext';
import ReactPlayer from 'react-player';

const Quiz = () => {
    const { showQuiz, question, quizs, checkAnswer: originalCheckAnswer, correctAnswer,
            selectedAnswer, questionIndex, nextQuestion, showTheResult, user, timer, setTimer } = useContext(DataContext);
    
    const [isTimerRunning, setIsTimerRunning] = useState(true);
    const [videoUrl, setVideoUrl] = useState('');

    useEffect(() => {
        if (timer === 0) {
            // Automatically move to the next question if time runs out
            if (questionIndex + 1 !== quizs.length) {
                nextQuestion();
            } else {
                showTheResult();
            }
        }

        if (isTimerRunning) {
            const countdown = setInterval(() => {
                setTimer((prevTimer) => (prevTimer > 0 ? prevTimer - 1 : 0));
            }, 1000);

            return () => clearInterval(countdown);
        }
    }, [timer, isTimerRunning, questionIndex, quizs.length, nextQuestion, showTheResult]);

    useEffect(() => {
        // Reset the timer and start it when moving to the next question
        setTimer(60);
        setIsTimerRunning(true);
    }, [questionIndex]);

    useEffect(() => {
        console.log(question?.multimedia);
        setVideoUrl(`http://localhost:8000/openVideo/${question?.multimedia}`);
    }, [question]);

    const checkAnswer = (event, item, time) => {
        setIsTimerRunning(false); // Stop the timer when an answer is selected
        originalCheckAnswer(event, item, time);
    };

    return (
        <section className="bg-dark text-white" style={{ display: `${showQuiz ? 'block' : 'none'}` }}>
            <div className="container">
                <div className="row vh-100 align-items-center justify-content-center">
                    <div className="col-lg-4 col-md-6 mb-4 mb-lg-0">
                        <div className="card p-4" style={{ background: '#3d3d3d', borderColor: '#646464' }}>
                            <h5 className='mb-2 fs-normal lh-base'>Thông tin người chơi</h5>
                            <p>Họ tên: {user?.full_name}</p>
                            <p>Năm sinh: {user?.birth_year}</p>
                            <p>Sở thích: {user?.major.join(' ')}</p>
                            <p>Rank: {user?.rank}</p>
                        </div>
                    </div>
                    <div className="col-lg-8 col-md-6">
                        <div className="card p-4" style={{ background: '#3d3d3d', borderColor: '#646464' }}>
                            <div className="d-flex justify-content-between gap-md-3">
                                <h5 className='mb-2 fs-normal lh-base'>{question?.question}</h5>
                                <h5 style={{ color: '#60d600', width: '100px', textAlign: 'right' }}>{quizs.indexOf(question) + 1} / {quizs?.length}</h5>
                            </div>
                            <h5 className='mb-2 fs-normal lh-base'>Chủ đề: {question?.category}</h5>
                            <h5 className='mb-2 fs-normal lh-base'>Độ khó: {question?.difficulty}</h5>
                            <h5 className='mb-2 fs-normal lh-base'>Thời gian còn lại: {timer} giây</h5>
                            <div>
                                <div>
                                    <ReactPlayer url={videoUrl} controls width="100%" playing={true} />
                                </div>
                                {
                                    question?.options?.map((item, index) => <button
                                        key={index}
                                        className={`option w-100 text-start btn text-white py-2 px-3 mt-3 rounded btn-dark ${correctAnswer === item && 'bg-success'}`}
                                        onClick={(event) => {
                                            checkAnswer(event, item, 60 - timer);
                                        }}
                                        disabled={selectedAnswer}
                                    >
                                        {item}
                                    </button>)
                                }
                            </div>

                            {
                                (questionIndex + 1) !== quizs.length ?
                                    <button className='btn py-2 w-100 mt-3 bg-primary text-light fw-bold' onClick={nextQuestion} disabled={!selectedAnswer}>Next Question</button>
                                    :
                                    <button className='btn py-2 w-100 mt-3 bg-primary text-light fw-bold' onClick={showTheResult} disabled={!selectedAnswer}>Show Result</button>
                            }
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Quiz;
