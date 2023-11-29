import React, { useState, useEffect, useContext } from 'react';
import LogoutButton from "../../components/LogoutButton/LogoutButton";
import NavBar from "../../components/NavBar/NavBar";
import UserGamesDropdown from '../../components/UserGameDropdown/UserGamesDropdown';
import AllGamesDropdown from '../../components/AllGamesDropdown/AllGamesDropdown';
import ComboVisuals from '../../components/ComboVisuals/ComboVisuals';
import GameSidebar from '../../components/GameSidebar/GameSidebar';
import { AuthContext } from '../../AuthContext';
import FileUpload from '../../components/FileUpload/FileUpload';
import './Evaluator.css';

const Evaluator = () => {
    const { user } = useContext(AuthContext);
    const [selectedGameId, setSelectedGameId] = useState(null);
    const [gameData, setGameData] = useState({ combos: null, settings: null, playerInfo: null });
    const [isActionInitiated, setIsActionInitiated] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        if (selectedGameId) {
            setIsLoading(true);
            const fetchGameData = async () => {
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
                } finally {
                    setIsLoading(false);
                }
            };

            fetchGameData();
        }
    }, [selectedGameId]);

    const handleGameSelection = (gameId) => {
        setSelectedGameId(gameId);
        setIsActionInitiated(true);
        setIsLoading(true);
    };

    const handleFileUploadComplete = (data) => {
        setGameData({
            combos: data.combos,
            settings: data.settings,
            playerInfo: data.players_info
        });
        setIsLoading(false);
        setIsActionInitiated(true);
    };

    const handleUploadStart = () => {
        setIsLoading(true);
        setIsActionInitiated(true);
    };

    return (
        <div className="evaluator-container">
            <NavBar />
            <div className="fixed-background"></div>
            <div className="banner-container">
                <FileUpload onUploadComplete={handleFileUploadComplete} onUploadStart={handleUploadStart} />
                <AllGamesDropdown onGameSelect={handleGameSelection} />
                {user && <UserGamesDropdown userId={user.id} onGameSelect={handleGameSelection} />}
                {user && <LogoutButton />}
            </div>
            {!isActionInitiated && (
                <div className="placeholder-container">
                    <p className="overlay-message">Upload or select a game</p>
                    <img src="/backendimages/Blank_2_Grids_Collage-removebg-preview.png" alt="Placeholder" />
                </div>
            )}
            {isLoading && (
                <div className="loading-container">
                    <img src="/backendimages/180px-MultiShine.gif" alt="Loading..." />
                </div>
            )}
            {gameData.settings && gameData.playerInfo && (
                <GameSidebar 
                    settings={gameData.settings} 
                    playerInfo={gameData.playerInfo}
                />
            )}
            <div className="content">
                {gameData.combos && <ComboVisuals combos={gameData.combos} settings={gameData.settings} />}
            </div>
        </div>
    );
};

export default Evaluator;
