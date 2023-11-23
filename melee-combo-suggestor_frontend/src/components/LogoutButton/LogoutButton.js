import React from 'react';
import axios from 'axios';
import './LogoutButton.css'; // Import the CSS here

const LogoutButton = () => {
    const handleLogout = async () => {
        try {
            await axios.post('http://localhost:5000/logout');
            // Handle successful logout (e.g., update state, redirect)
        } catch (error) {
            // Handle error
        }
    };

    return <button className="logout-button" onClick={handleLogout}>Logout</button>;
};

export default LogoutButton;