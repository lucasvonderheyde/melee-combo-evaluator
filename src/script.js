const { SlippiGame } = require("@slippi/slippi-js");
const fs = require("fs");
const path = require('path');

const slippiFilePath = "data/slp_files/Mango_20230911T191555.slp"

const game = new SlippiGame(`../${slippiFilePath}`);

const outputDir = `../data/temp_json_data/output_folder_${Date.now()}`;

// Debugging: Print out the absolute path
console.log("Absolute path: ", path.resolve(__dirname, outputDir));

// Debugging: Check if parent directory exists
console.log("Does parent directory exist?", fs.existsSync('../data/temp_json_data'));

// Create the new folder
try {
  if (!fs.existsSync(outputDir)){
    fs.mkdirSync(outputDir);
    console.log(`Directory created at ${outputDir}`);
  }
} catch (e) {
  console.error("Could not create directory", e);
}

const settings = game.getSettings();
const settingsFilePath = `${outputDir}/settings.json`;
fs.writeFileSync(settingsFilePath, JSON.stringify(settings));
console.log(`Settings saved to ${settingsFilePath}`);

const lowerPortPlayer = settings.players[0].playerIndex;
const higherPortPlayer = settings.players[1].playerIndex;

const metadata = game.getMetadata();
const metadataFilePath = `${outputDir}/metadata.json`;
fs.writeFileSync(metadataFilePath, JSON.stringify(metadata));
console.log(`Metadata saved to ${metadataFilePath}`);

const lastFrame = metadata.lastFrame;
const frames = game.getFrames();

const allPostFrames = [];
const allPreFrames = [];  // New array for "pre" frames

let frameIndex = 0;

while (frameIndex <= lastFrame) {
    const frame = frames[frameIndex];
    
    const lowerPortPlayerPostFrame = frame.players[lowerPortPlayer].post;
    const higherPortPlayerPostFrame = frame.players[higherPortPlayer].post;

    allPostFrames.push({ lowerPortPlayerPostFrame, higherPortPlayerPostFrame });

    // New code for "pre" frames
    const lowerPortPlayerPreFrame = frame.players[lowerPortPlayer].pre;
    const higherPortPlayerPreFrame = frame.players[higherPortPlayer].pre;

    allPreFrames.push({ lowerPortPlayerPreFrame, higherPortPlayerPreFrame });

    frameIndex++;
}

const postFrameDataFilePath = `${outputDir}/all_post_frames.json`;
fs.writeFileSync(postFrameDataFilePath, JSON.stringify(allPostFrames));
console.log(`All "post" frame data saved to ${postFrameDataFilePath}`);

// New code to save "pre" frames
const preFrameDataFilePath = `${outputDir}/all_pre_frames.json`;
fs.writeFileSync(preFrameDataFilePath, JSON.stringify(allPreFrames));
console.log(`All "pre" frame data saved to ${preFrameDataFilePath}`);
