// Evaluator.js

import React, { useState, useEffect, useContext } from 'react';
import FileUpload from "../../components/FileUpload/FileUpload";
import LogoutButton from "../../components/LogoutButton/LogoutButton";
import NavBar from "../../components/NavBar/NavBar";
import UserGamesDropdown from '../../components/UserGameDropdown/UserGamesDropdown';
import AllGamesDropdown from '../../components/AllGamesDropdown/AllGamesDropdown';
import ComboVisuals from '../../components/ComboVisuals/ComboVisuals';
import { AuthContext } from '../../AuthContext';
import './Evaluator.css';

export default function Evaluator() {
    const { user } = useContext(AuthContext);
    const [selectedGameId, setSelectedGameId] = useState(null);
    const [combos, setCombos] = useState(null);

    useEffect(() => {
        const fetchGameData = async () => {
            if (selectedGameId) {
                try {
                    const response = await fetch(`http://127.0.0.1:5555/api/games/${selectedGameId}`); 
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    const data = await response.json()
                    console.log(data)
                    setCombos(data);
                } catch (error) {
                    console.error('Error fetching game data:', error);
                }
            }
        };
    
        fetchGameData();
    }, [selectedGameId]);
    
    const handleGameSelection = (gameId) => {
        setSelectedGameId(gameId);
    };

    return (
        <div className="evaluator-container">
            <NavBar />
            <div className="content">
                <div className="file-upload-container">
                    <FileUpload />
                    <AllGamesDropdown onGameSelect={setSelectedGameId} />
                    <h3>Current Game Id: {selectedGameId}</h3>
                </div>
                {user && (
                <div className="user-games-dropdown-container">
                        <UserGamesDropdown userId={user.id} onGameSelect={handleGameSelection} />
                        <LogoutButton />
                    </div>
                )}
                {combos && <ComboVisuals combos={combos} />}
            </div>
        </div>
    );
}
