import React, { useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AuthContext } from '../../AuthContext';
import './NavBar.css'; 

const NavBar = () => {
    const { user } = useContext(AuthContext);
    const location = useLocation();

    const isActive = (path) => location.pathname === path;

    return (
        <nav>
            <ul>
                <li>
                    <Link to="/homepage" className={isActive('/homepage') ? 'active' : ''}>Home</Link>
                </li>
                <li>
                    <Link to="/evaluator" className={isActive('/evaluator') ? 'active' : ''}>Evaluator</Link>
                </li>
                {user 
                    ? <li><Link to="/login" className={isActive('/login') ? 'active' : ''}>Profile</Link></li> 
                    : <li><Link to="/login" className={isActive('/login') ? 'active' : ''}>Login</Link></li>}
            </ul>
        </nav>
    );
};

export default NavBar;
