import React from 'react';

const ComboBlock = ({ frames, playerport }) => {

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
        </div>
    );
};

export default ComboBlock;