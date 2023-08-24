import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Leaderboard.css'; // Import the CSS file for styling

function Leaderboard() {
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
  // Fetch leaderboard data for the past 30 days from your API
  axios.get('http://127.0.0.1:5000/api/overall-stats_30days')
    .then((response) => {
      // Filter and sort the data for players with over 10 matches played and win rate in descending order
      const filteredData = response.data
        .filter((player) => player.matches_played > 10)
        .sort((a, b) => b.win_rate - a.win_rate);

      // Take the top 3 results (highest win rates)
      const topResults = filteredData.slice(0, 3);

      // Set the top results in the state
      setLeaderboardData(topResults);
      setIsLoading(false);
    })
    .catch((error) => {
      console.error('Error fetching leaderboard data:', error);
      setIsLoading(false);
    });
}, []);

  return (
    <div>
      <h2>Leaderboard Page</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Win Rate (%)</th>
          </tr>
        </thead>
        <tbody>
          {isLoading ? (
            <tr>
              <td colSpan="3">Loading...</td>
            </tr>
          ) : leaderboardData.length === 0 ? (
            <tr>
              <td colSpan="3">No data available</td>
            </tr>
          ) : (
            leaderboardData.map((item, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{item.etf2l_name}</td>
                <td>{item.win_rate}%</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;
