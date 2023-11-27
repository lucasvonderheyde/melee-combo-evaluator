import React from 'react';
import './StageComboDisplay.css';
import stageData from '../../stageComboDisplay';

const StageComboDisplay = ({ frames, settings, playerport }) => {
  const stage = stageData.find(s => s.id === settings.stage_id);

  // Recalculated scale factors and reference points
  const scaleX = stage.dimensions.imagewidthpx / stage.dimensions.gameunitswidth;
  const scaleY = stage.dimensions.imageheightpx / stage.dimensions.gameunitsheight;
  const refX = stage.dimensions.imagewidthpx / 2;
  const refY = stage.dimensions.imageheightpx / 2;

  const convertToSvgPosition = (gameCoord, scale, refPoint) => {
    return (gameCoord * scale) + refPoint;
  };

  const isLowerPlayer = playerport === 'lowerportplayer';

  const svgPositions = frames.map(frame => {
    const gameX = isLowerPlayer ? frame.higher_post_position_x : frame.lower_post_position_x;
    const gameY = isLowerPlayer ? frame.higher_post_position_y : frame.lower_post_position_y;

    return {
      x: convertToSvgPosition(gameX, scaleX, refX),
      y: convertToSvgPosition(-gameY, scaleY, refY) // Invert the Y axis for SVG
    };
  });

  const renderSvgMarkers = () => {
    return svgPositions.map((position, index) => (
      <circle key={index} cx={position.x} cy={position.y} r="20" fill="red" />
    ));
  };

  return (
    <div className="stage-combo-display">
        <img
            className="stage-image"
            src={stage.imagePath}
            alt={stage.name}
        />
        <svg
            className="stage-svg"
            viewBox={`0 0 ${stage.dimensions.imagewidthpx} ${stage.dimensions.imageheightpx}`}
        >
            {renderSvgMarkers()}
        </svg>
    </div>
  );
};

export default StageComboDisplay
