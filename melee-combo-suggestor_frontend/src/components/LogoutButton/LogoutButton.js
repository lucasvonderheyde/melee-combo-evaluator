import React, { useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../../AuthContext';
import './LogoutButton.css';
import { useNavigate } from 'react-router-dom';  

const LogoutButton = ({ className }) => {
    const { logout } = useContext(AuthContext);
    const navigate = useNavigate(); 

    const handleLogout = async () => {
        try {
            await axios.post('http://localhost:5555/logout');
            logout();  
            navigate('/'); 
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return <button className={`logout-button ${className}`} onClick={handleLogout}>Logout</button>;
};

export default LogoutButton;
