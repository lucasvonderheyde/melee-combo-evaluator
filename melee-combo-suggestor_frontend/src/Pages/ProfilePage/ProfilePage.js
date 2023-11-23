import React, { useContext } from 'react'
import NavBar from '../../components/NavBar/NavBar';
import { AuthContext } from '../../AuthContext';

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
            </div>
        </div>
    );
};

export default ProfilePage;