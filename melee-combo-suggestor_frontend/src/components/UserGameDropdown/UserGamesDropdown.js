import React, { useState, useEffect } from 'react';

const UserGamesDropdown = ({ userId, onGameSelect }) => {
    const [userGames, setUserGames] = useState([]);

    useEffect(() => {
        const fetchUserGames = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5555/api/user-games/${userId}`);
                if(response.ok) {
                    const games = await response.json();
                    setUserGames(games);
                } else {
                    console.error('Failed to fetch user games');
                }
            } catch (error) {
                console.error('Error fetching user games:', error);
            }
        };

        if (userId) {
            fetchUserGames();
        }
    }, [userId]);

    const handleGameSelection = (event) => {
        onGameSelect(event.target.value);
    };

    return (
        <select onChange={handleGameSelection} defaultValue="">
            <option value="" disabled>Select a game</option>
            {userGames.map((game) => (
                <option key={game.id} value={game.id}>{game.name}</option>
            ))}
        </select>
    );
};

export default UserGamesDropdown;
