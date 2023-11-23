import React from 'react';
import './LandingPage.css';
import { useNavigate, useLocation } from 'react-router-dom';

function LandingPage() {
    const navigate = useNavigate();
    const location = useLocation();

    return (
        <div className={`landing-container ${location.pathname === '/' ? 'no-overlay' : ''}`}>
            <div className="centered-content">
                <button onClick={() => navigate('/homepage')}>
                    Enter
                </button>
            </div>
        </div>
    );
}

export default LandingPage;

