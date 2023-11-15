const { SlippiGame } = require("@slippi/slippi-js");
const fs = require("fs");
const path = require('path');

const slippiFilesDirectory = "player_uploads/slp_games"; // Directory containing Slippi files
const outputBaseDir = "player_uploads/user_temp_slp_data"; // Base directory for outputs

// Ensure the output base directory exists
if (!fs.existsSync(outputBaseDir)) {
    fs.mkdirSync(outputBaseDir);
}

// Read the directory and filter for .slp files
const slippiFiles = fs.readdirSync(slippiFilesDirectory).filter(file => file.endsWith('.slp'));

slippiFiles.forEach(file => {
    const slippiFilePath = path.join(slippiFilesDirectory, file);
    const game = new SlippiGame(slippiFilePath);

    // Process settings
    const settings = game.getSettings();
    if (!settings || Object.keys(settings).length === 0) {
        throw new Error('Settings invalid or empty for ' + file);
    }
    const settingsFilePath = path.join(outputBaseDir, `settings_${file}.json`);
    fs.writeFileSync(settingsFilePath, JSON.stringify(settings));

    // Process metadata
    const metadata = game.getMetadata();
    if (!metadata || Object.keys(metadata).length === 0) {
        throw new Error('Metadata invalid or empty for ' + file);
    }
    const metadataFilePath = path.join(outputBaseDir, `metadata_${file}.json`);
    fs.writeFileSync(metadataFilePath, JSON.stringify(metadata));

    // Process frame data
    const lastFrame = metadata.lastFrame;
    const frames = game.getFrames();
    const allPostFrames = [];
    const allPreFrames = [];
    const lowerPortPlayer = settings.players[0].playerIndex;
    const higherPortPlayer = settings.players[1].playerIndex;

    for (let frameIndex = 0; frameIndex <= lastFrame; frameIndex++) {
        const frame = frames[frameIndex];
        if (frame) {
            const lowerPortPlayerPostFrame = frame.players[lowerPortPlayer].post;
            const higherPortPlayerPostFrame = frame.players[higherPortPlayer].post;
            allPostFrames.push({ frameIndex, lowerPortPlayerPostFrame, higherPortPlayerPostFrame });

            const lowerPortPlayerPreFrame = frame.players[lowerPortPlayer].pre;
            const higherPortPlayerPreFrame = frame.players[higherPortPlayer].pre;
            allPreFrames.push({ frameIndex, lowerPortPlayerPreFrame, higherPortPlayerPreFrame });
        }
    }

    // Write post and pre frame data
    const postFrameDataFilePath = path.join(outputBaseDir, `all_post_frames_${file}.json`);
    fs.writeFileSync(postFrameDataFilePath, JSON.stringify(allPostFrames));

    const preFrameDataFilePath = path.join(outputBaseDir, `all_pre_frames_${file}.json`);
    fs.writeFileSync(preFrameDataFilePath, JSON.stringify(allPreFrames));

    console.log(`Processed ${file}`);
});
