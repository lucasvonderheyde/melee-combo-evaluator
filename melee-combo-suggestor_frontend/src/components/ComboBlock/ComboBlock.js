import { useState } from 'react';
import Papa from 'papaparse';
import moveImages from '../../moveImages';
import { characterIdsFromCombosTable } from '../../gameIds'; // Import the character ID mappings
import './ComboBlock.css';

const ComboBlock = ({ frames, setExpandedComboBlock, expandedComboBlock, playerport, characterId }) => {
    const deathActionStateIds = [0, 1, 2, 4, 8];
    const comboBlockId = frames[0]?.combo_block_for_model;
    let isLowerPlayer = playerport === 'higherportplayer' ? false : true;
    const [score, setScore] = useState(null);

    // Function to get character name from ID
    const getCharacterName = (id) => {
        return characterIdsFromCombosTable[id]?.toLowerCase().replace(/\s/g, '');
    };

    const handleClick = () => {
        setExpandedComboBlock(comboBlockId);
    };

    if (expandedComboBlock !== null && expandedComboBlock !== comboBlockId) {
        return null; 
    }

    const renderActionStates = () => {
        const characterName = getCharacterName(characterId);
        return frames.map((frame, index) => {
            const actionState = frame.attack_state_to_hit_in_combo_for_model;
            
            // Check if actionState is not null and actionState image exists
            if (actionState !== null && actionState !== undefined) {
                const imagePath = moveImages[characterName]?.[actionState.toString()] || `Action State ${actionState} image not available`;
    
                if (typeof imagePath === 'string') {
                    return (
                        <div key={index}>
                            <p>Action State to Hit: {actionState}</p>
                            <img src={imagePath} alt={`Move ${actionState}`} />
                        </div>
                    );
                } else {
                    return <p key={index}>Action State to Hit: {actionState} (image not available)</p>;
                }
            }
            return null;
        });
    };

    const handleComboAiClick = async () => {
        const csv = Papa.unparse(frames);
        try {
            const response = await fetch('http://127.0.0.1:5555/api/score-combo', {
                method: 'POST',
                headers: { 'Content-Type': 'text/csv' },
                body: csv
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const result = await response.json();
            setScore(result);  // Update the score state
        } catch (error) {
            console.error('Error scoring combo:', error);
        }
    };
    
    const renderScores = () => {
        if (!score || expandedComboBlock !== comboBlockId) return null;

        return (
            <div>
                <p>Damage Done Score: {isLowerPlayer ? score.lower_port_damage_done_with_combo_model_score : score.higher_port_damage_done_with_combo_model_score}</p>
                <p>X Position Score: {isLowerPlayer ? score.higher_port_x_position_model_score : score.lower_port_x_position_model_score}</p>
                <p>Y Position Score: {isLowerPlayer ? score.higher_port_y_position_model_score : score.lower_port_y_position_model_score}</p>
            </div>
        );
    };

    return (
        <div className="combo-block">
            <h3>Combo: {comboBlockId}</h3>
            <p>Number of Frames: {frames.length}</p>
            {isLowerPlayer 
                ? <p>Damage Done: {frames[frames.length - 1].lower_port_damage_done_with_combo}</p>
                : <p>Damage Done: {frames[frames.length - 1].higher_port_damage_done_with_combo}</p>}
            {isLowerPlayer && frames[frames.length - 1].higher_post_action_state_id in deathActionStateIds
                ? <p>Stock Taken</p>
                : null}
            {!isLowerPlayer && frames[frames.length - 1].lower_post_action_state_id in deathActionStateIds
                ? <p>Stock Taken</p>
                : null}
            {expandedComboBlock === comboBlockId && (
                <div className="action-states">
                    {renderActionStates()}
                    <button onClick={handleComboAiClick}>Score Combo</button>
                </div>
            )}
            {renderScores()}
            <button onClick={handleClick}>Details</button>
        </div>
    );
};

export default ComboBlock;
