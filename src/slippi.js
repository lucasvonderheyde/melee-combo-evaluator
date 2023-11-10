const { SlippiGame } = require("@slippi/slippi-js");
const fs = require("fs");
const path = require('path');

const slippiFilesDirectory = "../data/slp_files"; // Directory containing Slippi files
const outputBaseDir = "../data/temp_json_data"; // Base directory for outputs

// Ensure the output base directory exists
if (!fs.existsSync(outputBaseDir)) {
    fs.mkdirSync(outputBaseDir);
}

// Read the directory and filter for .slp files
const slippiFiles = fs.readdirSync(slippiFilesDirectory).filter(file => file.endsWith('.slp'));

slippiFiles.forEach(file => {
    const slippiFilePath = path.join(slippiFilesDirectory, file);
    const game = new SlippiGame(slippiFilePath);

    const outputDir = path.join(outputBaseDir, `output_folder_${file}_${Date.now()}`);
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    const settings = game.getSettings();
    if (!settings || Object.keys(settings).length === 0) {
        throw new Error('Settings invalid or empty for ' + file);
    }

    const settingsFilePath = `${outputDir}/settings.json`;
    fs.writeFileSync(settingsFilePath, JSON.stringify(settings));

    const lowerPortPlayer = settings.players[0].playerIndex;
    const higherPortPlayer = settings.players[1].playerIndex;

    const metadata = game.getMetadata();
    if (!metadata || Object.keys(metadata).length === 0) {
        throw new Error('Metadata invalid or empty for ' + file);
    }
    const metadataFilePath = `${outputDir}/metadata.json`;
    fs.writeFileSync(metadataFilePath, JSON.stringify(metadata));

    const lastFrame = metadata.lastFrame;
    const frames = game.getFrames();

    const allPostFrames = [];
    const allPreFrames = [];

    let frameIndex = 0;

    while (frameIndex <= lastFrame) {
        const frame = frames[frameIndex];
        if (frame) {
            const lowerPortPlayerPostFrame = frame.players[lowerPortPlayer].post;
            const higherPortPlayerPostFrame = frame.players[higherPortPlayer].post;

            allPostFrames.push({ frameIndex, lowerPortPlayerPostFrame, higherPortPlayerPostFrame });

            const lowerPortPlayerPreFrame = frame.players[lowerPortPlayer].pre;
            const higherPortPlayerPreFrame = frame.players[higherPortPlayer].pre;

            allPreFrames.push({ frameIndex, lowerPortPlayerPreFrame, higherPortPlayerPreFrame });
        }
        frameIndex++;
    }

    if (allPostFrames.length === 0) {
        throw new Error('allPostFrames is empty for ' + file);
    }

    if (allPreFrames.length === 0) {
        throw new Error('allPreFrames is empty for ' + file);
    }

    const postFrameDataFilePath = `${outputDir}/all_post_frames.json`;
    fs.writeFileSync(postFrameDataFilePath, JSON.stringify(allPostFrames));

    const preFrameDataFilePath = `${outputDir}/all_pre_frames.json`;
    fs.writeFileSync(preFrameDataFilePath, JSON.stringify(allPreFrames));

    console.log(`Processed ${file}`);
});
