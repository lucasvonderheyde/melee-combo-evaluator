import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../../AuthContext';
import Navbar from '../../components/NavBar/NavBar';
import './LoginPage.css';

function LoginPage() {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const { login } = useContext(AuthContext);

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5555/login', { username, password });
            console.log("Full Login response:", response); 
            login(response.data.user); // Pass the entire user object
            setMessage(response.data.message);
        } catch (error) {
            setMessage(error.response.data.message || 'Login failed');
        }
    };
    

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5555/register', { username, email, password });
            setMessage(response.data.message);
        } catch (error) {
            setMessage(error.response.data.message || 'Registration failed');
        }
    };

    return (
        <div className="login-page-container">
            <Navbar />
            <div className="login-register-buttons">
                <button 
                    onClick={() => setIsLogin(true)}
                    className={isLogin ? 'active' : ''}>
                    Log In
                </button>
                <button 
                    onClick={() => setIsLogin(false)}
                    className={!isLogin ? 'active' : ''}>
                    Register
                </button>
            </div>

            <form className="login-form" onSubmit={isLogin ? handleLogin : handleRegister}>
                <div className="form-group">
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        required
                    />
                </div>
                {!isLogin && (
                    <div className="form-group">
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Email"
                            required
                        />
                    </div>
                )}
                <div className="form-group">
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                    />
                </div>
                <button type="submit" className="submit-button">
                    {isLogin ? 'Enter' : 'Start Evaluating'}
                </button>
            </form>

            {message && <p className="login-message">{message}</p>}
        </div>
    );
}

export default LoginPage;