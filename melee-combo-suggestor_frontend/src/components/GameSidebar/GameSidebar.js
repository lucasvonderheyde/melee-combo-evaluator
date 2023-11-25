import React, { useEffect, useState } from 'react';
import './GameSidebar.css'; // Ensure this path is correct

const GameSidebar = ({ settings, playerInfo }) => {
    // useState for stageName and stageImage
    const [stageDetails, setStageDetails] = useState({
        name: '',
        image: ''
    });

    useEffect(() => {
        if (settings) {
            // Assuming getStageDetails is a function that returns an object with name and image
            const details = getStageDetails(settings.stage_id);
            setStageDetails(details);
        }
    }, [settings]);

    const getCharacterIcon = (characterId) => {
        switch (characterId) {
            case 20: return '/falcocssicon.png';
            case 2: return '/foxcssicon.png';
            default: return '/defaulticon.png';
        }
    };

    // Function to get stage details based on stageId
    const getStageDetails = (stageId) => {
        switch (stageId) {
            case 31: return { name: 'Battlefield', image: '/Battlefieldssbm.webp' };
            default: return { name: 'Unknown Stage', image: '/defaultstage.png' };
        }
    };

    return (
        <div className="game-sidebar">
            {stageDetails.name && (
                <div className="stage-container">
                    <h3>{stageDetails.name}</h3>
                    <img src={stageDetails.image} alt={stageDetails.name} />
                </div>
            )}
            {playerInfo.map((player, index) => (
                <div className="player-container" key={index}>
                    <h3>{player.display_name}</h3>
                    <img src={getCharacterIcon(player.character_id)} alt={`${player.display_name}'s character`} />
                </div>
            ))}
        </div>
    );
};

export default GameSidebar;
