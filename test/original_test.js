const { SlippiGame } = require("@slippi/slippi-js");
const fs = require("fs");

const game = new SlippiGame("test/slp_files/Game_20230927T205957.slp");

const outputDir = `./jsondb/output_folder_${Date.now()}`;

if (!fs.existsSync(outputDir)){
    fs.mkdirSync(outputDir);
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
const allPreFrames = [];  // Added this line to store "pre" frames

let frameIndex = 0;

while (frameIndex < lastFrame) {
    const frame = frames[frameIndex];
    
    const lowerPortPlayerPostFrame = frame.players[lowerPortPlayer].post;
    const higherPortPlayerPostFrame = frame.players[higherPortPlayer].post;

    const lowerPortPlayerPreFrame = frame.players[lowerPortPlayer].pre;  // Added this line
    const higherPortPlayerPreFrame = frame.players[higherPortPlayer].pre;  // Added this line

    allPostFrames.push({ lowerPortPlayerPostFrame, higherPortPlayerPostFrame });
    allPreFrames.push({ lowerPortPlayerPreFrame, higherPortPlayerPreFrame });  // Added this line

    frameIndex++;
}

const postFrameDataFilePath = `${outputDir}/all_post_frames.json`;
fs.writeFileSync(postFrameDataFilePath, JSON.stringify(allPostFrames));
console.log(`All "post" frame data saved to ${postFrameDataFilePath}`);

const preFrameDataFilePath = `${outputDir}/all_pre_frames.json`;  // Added this line
fs.writeFileSync(preFrameDataFilePath, JSON.stringify(allPreFrames));  // Added this line
console.log(`All "pre" frame data saved to ${preFrameDataFilePath}`);  // Added this line
