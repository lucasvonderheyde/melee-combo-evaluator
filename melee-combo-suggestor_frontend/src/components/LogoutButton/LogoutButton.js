import React, { useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../../AuthContext'; 
import './LogoutButton.css'; 

const LogoutButton = () => {
    const { logout } = useContext(AuthContext); 

    const handleLogout = async () => {
        try {
            await axios.post('http://localhost:5000/logout');
            logout(); 
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return <button className="logout-button" onClick={handleLogout}>Logout</button>;
};

export default LogoutButton;
