import React, { useState, useContext, useEffect } from 'react';
import axios from 'axios';
import NavBar from '../../components/NavBar/NavBar';
import { AuthContext } from '../../AuthContext';
import LogoutButton from '../../components/LogoutButton/LogoutButton';
import './ProfilePage.css';

const ProfilePage = () => {
    const { user, refreshUserData } = useContext(AuthContext);

    // State for editing fields
    const [editing, setEditing] = useState(false);
    const [newUsername, setNewUsername] = useState('');
    const [newEmail, setNewEmail] = useState('');
    const [favoriteCombo, setFavoriteCombo] = useState('');
    const [mainCharacter, setMainCharacter] = useState('');
    const [secondaryCharacter, setSecondaryCharacter] = useState('');
    const [message, setMessage] = useState('');

    // Update state when user context changes
    useEffect(() => {
        if (user) {
            setNewUsername(user.username);
            setNewEmail(user.email);
            setFavoriteCombo(user.favorite_combo);
            setMainCharacter(user.main_character);
            setSecondaryCharacter(user.secondary_character);
        }
    }, [user]);

    const handleProfileUpdate = async (e) => {
        e.preventDefault();
        let profileUpdated = false;

        // Preparing JSON data for the account update
        const accountData = {
            user_id: user.id,
            new_username: newUsername,
            new_email: newEmail,
            favorite_combo: favoriteCombo,
            main_character: mainCharacter,
            secondary_character: secondaryCharacter
        };

        // Updating account details
        try {
            const accountResponse = await axios.post('http://127.0.0.1:5555/update-account', accountData);
            console.log("Response from update-account:", accountResponse.data);

            profileUpdated = accountResponse.data.message;
        } catch (error) {
            setMessage(error.response?.data?.message || 'Profile update failed');
            return;
        }

        if (profileUpdated) {
            setMessage('Profile updated successfully!');
            setEditing(false);
            await refreshUserData(); // Refresh user data
        }
    };

    return (
        <div>
            <NavBar />
            <div className='fixed-background'></div>
            <div className="profile-container">
                <h1 className='user-heading' >User Profile</h1>
                {user && (
                    <div>
                        <p><strong>Username:</strong> {user.username}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                        <p><strong>Favorite Combo:</strong> {user.favorite_combo || 'Not specified'}</p>
                        <p><strong>Main Character:</strong> {user.main_character || 'Not specified'}</p>
                        <p><strong>Secondary Character:</strong> {user.secondary_character || 'Not specified'}</p>
                    </div>
                )}
                <button onClick={() => setEditing(!editing)}>{editing ? 'Cancel Editing' : 'Edit Profile'}</button>
                {editing && (
                    <form onSubmit={handleProfileUpdate}>
                        <input
                            type="text"
                            placeholder="Username"
                            value={newUsername}
                            onChange={(e) => setNewUsername(e.target.value)}
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            value={newEmail}
                            onChange={(e) => setNewEmail(e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Favorite Combo"
                            value={favoriteCombo}
                            onChange={(e) => setFavoriteCombo(e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Main Character"
                            value={mainCharacter}
                            onChange={(e) => setMainCharacter(e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Secondary Character"
                            value={secondaryCharacter}
                            onChange={(e) => setSecondaryCharacter(e.target.value)}
                        />
                        <button type="submit">Update Profile</button>
                    </form>
                )}
                {message && <p className="profile-message">{message}</p>}
                <LogoutButton />
            </div>
        </div>
    );
};

export default ProfilePage;
