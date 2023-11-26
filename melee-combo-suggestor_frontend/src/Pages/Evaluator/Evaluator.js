import React, { useState, useEffect, useContext } from 'react';
import FileUpload from "../../components/FileUpload/FileUpload";
import LogoutButton from "../../components/LogoutButton/LogoutButton";
import NavBar from "../../components/NavBar/NavBar";
import UserGamesDropdown from '../../components/UserGameDropdown/UserGamesDropdown';
import AllGamesDropdown from '../../components/AllGamesDropdown/AllGamesDropdown';
import ComboVisuals from '../../components/ComboVisuals/ComboVisuals';
import GameSidebar from '../../components/GameSidebar/GameSidebar';
import { AuthContext } from '../../AuthContext';
import './Evaluator.css';

const Evaluator = () => {
    const { user } = useContext(AuthContext);
    const [selectedGameId, setSelectedGameId] = useState(null);
    const [gameData, setGameData] = useState({ combos: null, settings: null, playerInfo: null });

    useEffect(() => {
        const fetchGameData = async () => {
            if (selectedGameId) {
                try {
                    const response = await fetch(`http://127.0.0.1:5555/api/games/${selectedGameId}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    const data = await response.json();
                    setGameData({
                        combos: data.combos,
                        settings: data.settings,
                        playerInfo: data.players_info
                    });
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

    const handleFileUploadComplete = (data) => {
        setGameData({
            combos: data.combos,
            settings: data.settings,
            playerInfo: data.players_info
        });
    };

    return (
        <div className="evaluator-container">
            <NavBar />
            <div className="banner-container">
                <FileUpload onUploadComplete={handleFileUploadComplete} />
                <AllGamesDropdown onGameSelect={setSelectedGameId} />
                {user && <UserGamesDropdown userId={user.id} onGameSelect={handleGameSelection} />}
                {user && <LogoutButton />} 
            </div>
            {gameData.settings && gameData.playerInfo && (
                <GameSidebar 
                    settings={gameData.settings} 
                    playerInfo={gameData.playerInfo}
                />
            )}
            <div className="content">
                {gameData.combos && <ComboVisuals combos={gameData.combos} />}
            </div>
        </div>
    );
};

export default Evaluator;
