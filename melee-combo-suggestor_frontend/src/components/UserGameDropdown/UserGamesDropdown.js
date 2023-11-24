import React, { useEffect, useState, useContext } from 'react';
import { AuthContext } from '../../AuthContext';

// UserGamesDropdown.js
const UserGamesDropdown = ({ onSelect }) => {
    const [games, setGames] = useState([]);

    useEffect(() => {
        // Fetch user games from the API
        const fetchGames = async () => {
            try {
                const response = await fetch('/api/user-games');
                if (response.ok) {
                    const data = await response.json();
                    setGames(data);
                } else {
                    console.error("Failed to fetch user games");
                }
            } catch (error) {
                console.error("Error fetching user games:", error);
            }
        };
        fetchGames();
    }, []);

    return (
        <select onChange={e => onSelect(e.target.value)}>
            {games.map(game => (
                <option key={game.id} value={game.id}>{game.description}</option>
            ))}
        </select>
    );
};

// Similar structure for AllGamesDropdown.js


export default UserGamesDropdown;
