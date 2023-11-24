import React, { useEffect, useState } from 'react';

const AllGamesDropdown = () => {
    const [allGames, setAllGames] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:5555/all-games', { credentials: 'include' })
            .then(response => response.json())
            .then(data => setAllGames(data))
            .catch(error => console.error('Error fetching all games:', error));
    }, []);

    return (
        <select>
            {allGames.map(game => (
                <option key={game.game_id} value={game.game_id}>Game at {game.start_at}</option>
            ))}
        </select>
    );
};

export default AllGamesDropdown;
