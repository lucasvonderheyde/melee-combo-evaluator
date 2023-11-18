import React, { useEffect, useState } from 'react';
import ComboBlock from '../ComboBlock/ComboBlock';
import './ComboVisuals.css'

const ComboVisuals = ({ combos }) => {
    const [groupedCombos, setGroupedCombos] = useState({ lowerPortPlayerCombos: {}, higherPortPlayerCombos: {} });

    useEffect(() => {
        if (combos) {
            const lowerPortPlayerCombos = {};
            const higherPortPlayerCombos = {};

            combos.forEach(combo => {
                const characterKey = combo.character_creating_combo_for_model === 0 ? 'lowerPortPlayerCombos' : 'higherPortPlayerCombos';
                const comboBlock = combo.combo_block_for_model;

                if (!lowerPortPlayerCombos[comboBlock] && characterKey === 'lowerPortPlayerCombos') {
                    lowerPortPlayerCombos[comboBlock] = [];
                }
                if (!higherPortPlayerCombos[comboBlock] && characterKey === 'higherPortPlayerCombos') {
                    higherPortPlayerCombos[comboBlock] = [];
                }

                if (characterKey === 'lowerPortPlayerCombos') {
                    lowerPortPlayerCombos[comboBlock].push(combo);
                } else {
                    higherPortPlayerCombos[comboBlock].push(combo);
                }
            });

            setGroupedCombos({ lowerPortPlayerCombos, higherPortPlayerCombos });
        }
    }, [combos]);

    return (
        <div className="combo-visuals-container">
            <div className="character-combos lower-port">
                <img src='falcoStock.png'/>
                {Object.entries(groupedCombos.lowerPortPlayerCombos).map(([comboBlock, frames]) => (
                    <ComboBlock key={`lowerPort-${comboBlock}`} frames={frames} playerport='lowerportplayer' />
                ))}
            </div>
            <div className="character-combos higher-port">
                <img src='foxStock.png'/>
                {Object.entries(groupedCombos.higherPortPlayerCombos).map(([comboBlock, frames]) => (
                    <ComboBlock key={`higherPort-${comboBlock}`} frames={frames} playerport='higherportplayer' />
                ))}
            </div>
        </div>
    );
};

export default ComboVisuals;
