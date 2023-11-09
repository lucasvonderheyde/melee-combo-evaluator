const { exec } = require('child_process')
const { error } = require('console')
const { stdout, stderr } = require('process')

function runSlippi() {
    console.log("Starting slippi.js...");
    
    const process = exec('node slippi.js', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return;
        }
        console.log(`slippi.js output: ${stdout}`);
    });

    process.on('exit', (code) => {
        console.log(`slippi.js process exited with code ${code}`);
    });
}

runSlippi();
