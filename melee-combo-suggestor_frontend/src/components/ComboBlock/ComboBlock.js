import React from 'react';

const ComboBlock = ({ frames, playerport }) => {

    const deathActionStateIds = [0, 1, 2, 4, 8]

    const handleClick = () => {
        console.log('ComboBlock clicked:', frames);
    };

    let isLowerPlayer = true

    if (playerport === 'higherportplayer') {
        isLowerPlayer = false
    }

    return (
        <div onClick={handleClick} className="combo-block">
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
        </div>
    );
};

export default ComboBlock;