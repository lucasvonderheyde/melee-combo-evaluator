import React, { useEffect, useState } from 'react';
import { charactersIdsFromPlayersInfoTable } from '../../gameIds'; // Import the character ID mappings
import stageImages from '../../stageImages'; // Import the stage images
import './GameSidebar.css'; // Ensure this path is correct

const GameSidebar = ({ settings, playerInfo }) => {
    const [stageDetails, setStageDetails] = useState({
        name: '',
        image: ''
    });

    useEffect(() => {
        if (settings && settings.stage_id !== undefined) {
            const details = getStageDetails(settings.stage_id);
            setStageDetails(details);
        }
    }, [settings]);

    const getCharacterIcon = (characterId) => {
        const characterName = charactersIdsFromPlayersInfoTable[characterId];
        return `/character_data/${characterName}/${characterName}cssicon.png`; // Path assumes a consistent naming convention
    };

    // Function to get stage details based on stageId
    const getStageDetails = (stageId) => {
        const stageImage = stageImages.Stages[stageId];
        const stageName = stageId in stageImages.Stages ? 'Battlefield' : 'Unknown Stage'; // Temporary logic, needs proper mapping
        return { name: stageName, image: stageImage || '/defaultstage.png' };
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
