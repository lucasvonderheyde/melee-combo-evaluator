import { useState } from 'react';
import Papa from 'papaparse';

const ComboBlock = ({ frames, setExpandedComboBlock, expandedComboBlock, playerport }) => {
    const deathActionStateIds = [0, 1, 2, 4, 8];
    const comboBlockId = frames[0]?.combo_block_for_model;
    let isLowerPlayer = playerport === 'higherportplayer' ? false : true;
    const [score, setScore] = useState(null);

    const handleClick = () => {
        setExpandedComboBlock(comboBlockId);
    };

    if (expandedComboBlock !== null && expandedComboBlock !== comboBlockId) {
        return null; 
    }

    const renderActionStates = () => {
        return frames.map((frame, index) => {
            const actionState = frame.attack_state_to_hit_in_combo_for_model;
            if (actionState !== null && actionState !== undefined) {
                return <p key={index}>Action State to Hit: {actionState}</p>;
            }
            return null;
        });
    };

    const handleComboAiClick = async () => {
        const csv = Papa.unparse(frames);
        try {
            const response = await fetch('http://127.0.0.1:5000/api/score-combo', {
                method: 'POST',
                headers: { 'Content-Type': 'text/csv' },
                body: csv
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const result = await response.json();
            console.log('Score:', result);
            setScore(result);  // Update the score state
        } catch (error) {
            console.error('Error scoring combo:', error);
        }
    };

    const renderScores = () => {
        if (!score) return null;

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
            <h3>Combo Block: {frames[0].combo_block_for_model}</h3>
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
