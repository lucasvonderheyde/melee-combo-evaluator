import React, { useEffect, useState } from 'react';
import './AllGamesDropdown.css'

const AllGamesDropdown = ({ onGameSelect }) => {
    const [allGames, setAllGames] = useState([]);

    useEffect(() => {
        const fetchAllGames = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5555/all-games');
                if(response.ok) {
                    const games = await response.json();
                    setAllGames(games);
                } else {
                    console.error('Failed to fetch all games');
                }
            } catch (error) {
                console.error('Error fetching all games:', error);
            }
        };

        fetchAllGames();
    }, []);

    const handleGameSelection = (event) => {
        onGameSelect(event.target.value);
    };

    return (
        <select className='dropdown' onChange={handleGameSelection} defaultValue="">
            <option value="" disabled>All games</option>
            {allGames.map((game) => (
                <option key={game.game_id} value={game.game_id}>{game.start_at}</option> 
            ))}
        </select>
    );
};

export default AllGamesDropdown;
