import React from 'react';
import axios from 'axios';

const LogoutButton = () => {
    const handleLogout = async () => {
        try {
            await axios.post('http://localhost:5000/logout');
            // Handle successful logout (e.g., update state, redirect)
        } catch (error) {
            // Handle error
        }
    };

    return <button onClick={handleLogout}>Logout</button>;
};

export default LogoutButton;