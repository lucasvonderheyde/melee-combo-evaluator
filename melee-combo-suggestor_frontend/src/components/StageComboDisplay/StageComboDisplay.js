import React from 'react';
import './StageComboDisplay.css'
import stageData from '../../stageComboDisplay';

const StageComboDisplay = ({ frames, settings, playerport }) => {
  return (
    <div className="stage-combo-display">
        <h3>{settings.stage_id}</h3>
    </div>
  );
};


export default StageComboDisplay;