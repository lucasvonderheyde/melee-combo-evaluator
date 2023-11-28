import React, { useContext } from 'react'
import NavBar from '../../components/NavBar/NavBar';
import { AuthContext } from '../../AuthContext';
import LogoutButton from '../../components/LogoutButton/LogoutButton';
import './ProfilePage.css'

const ProfilePage = () => {
    const { user } = useContext(AuthContext);

    return (
        <div>
            <NavBar />
            <div className="profile-container">
                <h1>User Profile</h1>
                {user && (
                    <div>
                        <p><strong>Username:</strong> {user.username}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                    </div>
                )}
                <LogoutButton />
            </div>
            
        </div>
    );
};

export default ProfilePage;