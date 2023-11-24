import React, { useState, useContext } from 'react';
import FileUpload from "../../components/FileUpload/FileUpload";
import LogoutButton from "../../components/LogoutButton/LogoutButton";
import NavBar from "../../components/NavBar/NavBar";
import { AuthContext } from '../../AuthContext';
import './Evaluator.css';
import UserGamesDropdown from '../../components/UserGameDropdown/UserGamesDropdown';
import AllGamesDropdown from '../../components/AllGamesDropdown/AllGamesDropdown';

export default function Evaluator() {
    const { user } = useContext(AuthContext);
    const [selectedGameId, setSelectedGameId] = useState(null);
    const [combos, setCombos] = useState([]);

    const handleGameSelection = async (gameId) => {
        setSelectedGameId(gameId);
    };

    return (
        <div className="evaluator-container">
            <NavBar />
            <div className="content">
                <div className="file-upload-container">
                    <FileUpload />
                    <AllGamesDropdown onSelect={handleGameSelection} />
                </div>
                {user && ( 
                    <div className="logout-button-container">
                        <UserGamesDropdown onSelect={handleGameSelection} />
                        <LogoutButton />
                    </div>
                )}
            </div>
        </div>
    );
}

