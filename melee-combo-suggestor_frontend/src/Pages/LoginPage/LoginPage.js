import Navbar from '../../components/NavBar/NavBar'
import './LoginPage.css'
import { useState } from 'react';
import axios from 'axios';
import LogoutButton from '../../components/LogoutButton/LogoutButton';

function LoginPage() {
    const [isLogin, setIsLogin] = useState(true); 
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5555/login', { username, password });
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
        <div>
            <Navbar />
            <button onClick={() => setIsLogin(true)}>Log In</button>
            <button onClick={() => setIsLogin(false)}>Register</button>

            <form onSubmit={isLogin ? handleLogin : handleRegister}>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    required
                />
                {!isLogin && (
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                    />
                )}
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                />
                <button type="submit">{isLogin ? 'Log In' : 'Register'}</button>
            </form>

            {message && <p>{message}</p>}
            <LogoutButton />
        </div>
    );
}

export default LoginPage;
