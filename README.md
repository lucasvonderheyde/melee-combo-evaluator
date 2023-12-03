# Melee Combo Evaluator

## Introduction
Melee Combo Evaluator is an innovative tool designed for players of Super Smash Brothers Melee. Utilizing a robust tech stack that includes React, PostgreSQL, PyTorch, Pandas, Jupyter Notebooks, and Flask, this application revolutionizes the way players analyze and improve their gameplay. A special acknowledgment goes to `slippi.js` for enabling the extraction of detailed game data from Slippi recordings.

![Gif Preview](/melee-combo-suggestor_frontend/public/meleewebapp.gif)


### Project Status
The application currently processes Slippi game recordings from Super Smash Brothers Melee, extracting and posting the data to a database. Key features include:
- **True Combo Analysis**: Identification and organization of true combos from each game.
- **Detailed Combo Visualization**: Display of all moves used in a combo, along with their trajectory.
- **Combo Evaluation**: A custom-developed machine learning model evaluates combos based on various parameters like x position, y position, and percent damage inflicted.

### Project Goal
The aim is to create a sophisticated combo evaluator that not only assesses but also suggests combos. This functionality is intended to enhance player decision-making and efficiency in gameplay.

## Features
- **User Accounts**: Users can create accounts to upload and manage their combos.
- **Database Access**: Users have access to all games and combos uploaded to the database, fostering a community-driven repository of gameplay data.

## Tech Stack
- React
- PostgreSQL
- PyTorch
- Pandas
- Jupyter Notebooks
- Flask

## Getting Started

### Prerequisites
- Node.js
- Python
- PostgreSQL
- Additional dependencies listed in `requirements.txt`

### Installation and Setup
1. Clone the repository:
2. Install the necessary Python and Node.js dependencies:
3. Set up your PostgreSQL database.
4. Start the Flask backend and React frontend:

## Usage
- **Account Creation**: Sign up to manage your combos.
- **Upload and Analyze Combos**: Upload your Slippi game recordings and explore the extracted combo data.
- **Combo Evaluation**: Get scores for your combos and insights on how to improve your gameplay.

## Contributing
Contributions to the Melee Combo Evaluator are welcome! Please refer to our contribution guidelines for more information on how to report issues, submit pull requests, and suggest improvements.

## Acknowledgments
- Special thanks to `slippi.js` for enabling the core functionality of this project.
