import React, { useEffect, useState } from 'react';
import ComboBlock from '../ComboBlock/ComboBlock';
import characterImages from '../../characterImages';  // Import the character images
import  {characterIdsFromCombosTable} from '../../gameIds'; // Import the character ID mappings
import './ComboVisuals.css';

const getCharacterImageFromId = (characterId) => {
    // Check if characterId is in the table, else return a default image
    if (characterId in characterIdsFromCombosTable) {
        const characterName = characterIdsFromCombosTable[characterId].toLowerCase();
        return characterImages[characterName]?.stockIcon || '/defaultCharacterIcon.png';
    }
    return '/defaultCharacterIcon.png'; // Default image if ID not found
};

const ComboVisuals = ({ combos, settings }) => {
    const [groupedCombos, setGroupedCombos] = useState({ lowerPortPlayerCombos: {}, higherPortPlayerCombos: {} });
    const [expandedComboBlock, setExpandedComboBlock] = useState(null);

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
                <img src={getCharacterImageFromId(combos[0]?.lower_post_internal_character_id)} alt='Lower Port Character' />
                {Object.entries(groupedCombos.lowerPortPlayerCombos).map(([comboBlock, frames]) => (
                    <ComboBlock 
                        key={`lowerPort-${comboBlock}`}
                        frames={frames}
                        comboBlockId={comboBlock}
                        expandedComboBlock={expandedComboBlock}
                        setExpandedComboBlock={handleComboBlockClick}
                        playerport='lowerportplayer'
                        characterId={combos[0]?.lower_post_internal_character_id}
                        settings={settings}
                    />
                ))}
            </div>
            <div className="character-combos higher-port">
                <img src={getCharacterImageFromId(combos[0]?.higher_post_internal_character_id)} alt='Higher Port Character' />
                {Object.entries(groupedCombos.higherPortPlayerCombos).map(([comboBlock, frames]) => (
                    <ComboBlock 
                        key={`higherPort-${comboBlock}`}
                        frames={frames}
                        comboBlockId={`higherPort-${comboBlock}`}
                        expandedComboBlock={expandedComboBlock}
                        setExpandedComboBlock={handleComboBlockClick}
                        playerport='higherportplayer'
                        characterId={combos[0]?.higher_post_internal_character_id}
                        settings={settings}
                    />
                ))}
            </div>
        </div>
    );
};

export default ComboVisuals;
