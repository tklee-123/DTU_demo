import React, { useState, useContext } from 'react';
import DataContext from '../context/dataContext';
import logo from '../assets/airc.png';

const Start = () => {
    const { startQuiz, showStart } = useContext(DataContext);
    const [userID, setUserID] = useState('');

    const handleInputChange = (e) => {
        setUserID(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        startQuiz(userID);
    };

    return (
        <section className='text-white text-center bg-dark' style={{ display: `${showStart ? 'block' : 'none'}` }}>
            <div className="container">
                <div className="row vh-100 align-items-center justify-content-center">
                    <div className="col-lg-8">
                        <img src={logo} alt="Logo" className="mb-4" style={{ width: '150px' }} />
                        <h1 className='fw-bold mb-4'>Quiz Recommender System</h1>
                        <form onSubmit={handleSubmit} className="mb-4">
                            <input 
                                type="text" 
                                className="form-control mb-3" 
                                placeholder="Enter playerID" 
                                value={userID}
                                onChange={handleInputChange}
                            />
                            <button type="submit" className="btn px-4 py-2 bg-light text-dark fw-bold">Login</button>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Start;
