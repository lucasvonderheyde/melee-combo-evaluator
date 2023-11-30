import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            try {
                const parsedUser = JSON.parse(storedUser);
                setUser(parsedUser);
            } catch (error) {
                console.error('Error parsing user from localStorage:', error);
                localStorage.removeItem('user');
            }
        }
    }, []);

    const login = (userData) => {
        console.log("Logged in user data:", userData); 
        localStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem('user'); 
        setUser(null); 
    };

    const refreshUserData = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5555/get-user', { params: { user_id: user.id } });
            const updatedUserData = response.data.user;
            localStorage.setItem('user', JSON.stringify(updatedUserData));
            setUser(updatedUserData);
        } catch (error) {
            console.error('Error refreshing user data:', error);
        }
    };


    return (
        <AuthContext.Provider value={{ user, login, logout, refreshUserData }}>
            {children}
        </AuthContext.Provider>
    );
};
