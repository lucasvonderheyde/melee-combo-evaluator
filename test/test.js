const { SlippiGame } = require("@slippi/slippi-js");
const fs = require("fs");

const game = new SlippiGame("test.slp");

// Get game settings – stage, characters, etc
const settings = game.getSettings();
const settingsFilePath = "settings.json";
fs.writeFileSync(settingsFilePath, JSON.stringify(settings));
console.log(`Settings saved to ${settingsFilePath}`);

lowerPortPlayer = settings.players[0].playerIndex
higherPortPlayer =settings.players[1].playerIndex

// Get metadata - start time, platform played on, etc
const metadata = game.getMetadata();
const metadataFilePath = "metadata.json";
fs.writeFileSync(metadataFilePath, JSON.stringify(metadata));
console.log(`Metadata saved to ${metadataFilePath}`);

// Extract the last frame from the metadata
const lastFrame = metadata.lastFrame;

// Get frames – animation state, inputs, etc
const frames = game.getFrames();

const allPostFrames = [];

let frameIndex = 0;

while (frameIndex < lastFrame) {
    const frame = frames[frameIndex];
    
    // Extract "post" frames for player 2 and player 3
    const lowerPortPlayerPostFrame = frame.players[lowerPortPlayer].post;
    const higherPortPlayerPostFrame = frame.players[higherPortPlayer].post;

    // Push the "post" frames to the array
    allPostFrames.push({ lowerPortPlayerPostFrame: lowerPortPlayerPostFrame, higherPortPlayerPostFrame: higherPortPlayerPostFrame });

    frameIndex++;
}

// Specify the output file where all "post" frame data will be saved
const postFrameDataFilePath = "all_post_frames.json";
fs.writeFileSync(postFrameDataFilePath, JSON.stringify(allPostFrames));
console.log(`All "post" frame data saved to ${postFrameDataFilePath}`);
