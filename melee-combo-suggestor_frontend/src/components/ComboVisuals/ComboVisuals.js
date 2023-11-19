import React, { useEffect, useState } from 'react';
import ComboBlock from '../ComboBlock/ComboBlock';
import './ComboVisuals.css'

const ComboVisuals = ({ combos }) => {
    const [groupedCombos, setGroupedCombos] = useState({ lowerPortPlayerCombos: {}, higherPortPlayerCombos: {} });
    const [expandedComboBlock, setExpandedComboBlock] = useState(null)

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

    const handleComboBlockClick = (comboBlockId) => {
        setExpandedComboBlock(expandedComboBlock === comboBlockId ? null : comboBlockId);
    };

    return (
        <div className="combo-visuals-container">
            <div className="character-combos lower-port">
                <img src='falcoStock.png' alt='Falco'/>
                {Object.entries(groupedCombos.lowerPortPlayerCombos).map(([comboBlock, frames]) => (
                    <ComboBlock 
                        key={`lowerPort-${comboBlock}`} 
                        frames={frames}
                        comboBlockId={`lowerPort-${comboBlock}`}
                        expandedComboBlock={expandedComboBlock}
                        setExpandedComboBlock={handleComboBlockClick} 
                        playerport='lowerportplayer' 
                    />
                ))}
            </div>
            <div className="character-combos higher-port">
                <img src='foxStock.png' alt='Fox'/>
                {Object.entries(groupedCombos.higherPortPlayerCombos).map(([comboBlock, frames]) => (
                    <ComboBlock 
                        key={`higherPort-${comboBlock}`} 
                        frames={frames}
                        comboBlockId={`higherPort-${comboBlock}`}
                        expandedComboBlock={expandedComboBlock}
                        setExpandedComboBlock={handleComboBlockClick} 
                        playerport='higherportplayer' 
                    />
                ))}
            </div>
        </div>
    );
};


export default ComboVisuals;
