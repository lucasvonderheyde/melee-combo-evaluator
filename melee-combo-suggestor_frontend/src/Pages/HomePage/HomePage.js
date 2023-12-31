import React, { useContext } from 'react';
import NavBar from "../../components/NavBar/NavBar"
import "./HomePage.css"
import { AuthContext } from '../../AuthContext'; 

export default function HomePage() {
    const { user } = useContext(AuthContext);
    console.log("User in HomePage:", user)
    return (
        <div className="home-container">
            <div className='fixed-background'></div>
            <img src="/backendimages/combofox-removebg.png" alt="Background Image" className="background-image"/>
            <NavBar />
            <div className="overlay"></div>
            <div className="content">
                <h1 className="welcome-message">Welcome to the Melee Combo Evaluator</h1>
                {user && <p className="user-greeting">Hello, {user.username}!</p>}
            </div>
        </div>
    );
}
