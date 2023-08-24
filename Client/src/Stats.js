import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Stats.css';

function Stats() {
    const [stats, setStats] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [sortOrder, setSortOrder] = useState({
        column: null,
        ascending: true,
    });
    const [searchQuery, setSearchQuery] = useState('');
    const dataCategories = [
        'Overall Stats',
        'Demo Stats',
        'Scout Stats',
        'Heavy Weapons Stats',
        'Soldier Stats',
        'Spy Stats',
        'Sniper Stats',
        'Medic Stats',
        'Engineer Stats',
    ];
    const [selectedCategory, setSelectedCategory] = useState('Overall Stats');
    const [currentPage, setCurrentPage] = useState(1);
    const [isLast30Days, setIsLast30Days] = useState(false); // Added state for 30 days
    const itemsPerPage = 10;

    const toggleTimeframe = (timeframe) => {
        setIsLast30Days(timeframe === 'last30days');
    };

    const getTimeframeStyle = (timeframe) => {
        return isLast30Days === (timeframe === 'last30days') ? 'selected' : '';
    };

    useEffect(() => {
        let apiEndpoint;
        switch (selectedCategory) {
            case 'Pyro Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/pyro-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Spy Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/spy-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Engineer Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/engineer-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Medic Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/medic-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Heavy Weapons Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/heavyweapons-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Scout Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/scout-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Demo Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/demoman-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Sniper Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/sniper-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Soldier Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/soldier-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            case 'Overall Stats':
                apiEndpoint = `http://127.0.0.1:5000/api/overall-stats${isLast30Days ? '_30days' : ''}?page=${currentPage}&search=${searchQuery}`;
                break;
            default:
                apiEndpoint = '';
                break;
        }

        axios.get(apiEndpoint)
            .then((response) => {
                setStats(response.data);
                setIsLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
                setIsLoading(false);
            });
    }, [selectedCategory, currentPage, searchQuery, isLast30Days]);

    const handleSort = (column) => {
        setSortOrder((prevSortOrder) => ({
            column,
            ascending:
                column === prevSortOrder.column
                    ? !prevSortOrder.ascending
                    : true,
        }));
    };

 const sortData = (data) => {
  if (!sortOrder.column) {
    return data;
  }

  const sortedData = [...data].sort((a, b) => {
    let aValue = a[sortOrder.column];
    let bValue = b[sortOrder.column];

    // Convert DAPM values to numbers for proper numeric sorting
    if (sortOrder.column === 'dapm') {
      aValue = parseFloat(aValue);
      bValue = parseFloat(bValue);
    }

    if (aValue < bValue) {
      return sortOrder.ascending ? -1 : 1;
    } else if (aValue > bValue) {
      return sortOrder.ascending ? 1 : -1;
    } else {
      return 0;
    }
  });

  return sortedData;
};

    const renderSortButtons = (column) => (
        <div>
            <button onClick={() => handleSort(column)}>↑</button>
            <button onClick={() => handleSort(column)}>↓</button>
        </div>
    );

    const renderTableRows = () => {
        const sortedStats = sortData(stats);

        if (isLoading) {
            return <tr><td colSpan="12">Loading...</td></tr>;
        } else if (sortedStats.length === 0) {
            return <tr><td colSpan="12">No data available</td></tr>;
        } else {
            return sortedStats.map((stat, index) => (
                <tr key={index}>
                    <td>{stat.steamid}</td>
                    <td>{stat.etf2l_name}</td>
                    <td>{stat.overall_kills}</td>
                    <td>{stat.overall_assists}</td>
                    <td>{stat.overall_deaths}</td>
                    <td>{stat.overall_dmg}</td>
                    <td>{stat.overall_wins}</td>
                    <td>{stat.dapm}</td>
                    <td>{stat.matches_played}</td>
                    <td>{stat.win_rate}%</td>
                </tr>
            ));
        }
    };

    const handlePageChange = (newPage) => {
        setCurrentPage(newPage);
    };

    const handleSearch = () => {
        setCurrentPage(1);
    };

    const totalPages = Math.ceil(stats.length / itemsPerPage);

    return (
        <div>
            <h2>TF2 Stats</h2>
            <label htmlFor="category">Select Category:</label>
            <select
                id="category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
            >
                {dataCategories.map((category) => (
                    <option key={category} value={category}>
                        {category}
                    </option>
                ))}
            </select>
            <input
                type="text"
                placeholder="Search by name"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button onClick={handleSearch}>Search</button>
            <div className="timeframe-toggle">
                <button
                    className={getTimeframeStyle('overall')}
                    onClick={() => toggleTimeframe('overall')}
                >
                    Overall
                </button>
                <button
                    className={getTimeframeStyle('last30days')}
                    onClick={() => toggleTimeframe('last30days')}
                >
                    Last 30 Days
                </button>
            </div>
            <table>
                <thead>
        <tr>
          <th>Steam ID {renderSortButtons('steamid')}</th>
          <th>ETF2L Name {renderSortButtons('etf2l_name')}</th>
          <th>Overall Kills {renderSortButtons('overall_kills')}</th>
          <th>Overall Assists {renderSortButtons('overall_assists')}</th>
          <th>Overall Deaths {renderSortButtons('overall_deaths')}</th>
          <th>Overall Damage {renderSortButtons('overall_dmg')}</th>
            <th>&nbsp;DPM {renderSortButtons('dapm')}</th>
          <th>Overall Wins {renderSortButtons('overall_wins')}</th>
          <th>Matches Played {renderSortButtons('matches_played')}</th>
          <th>Win Rate {renderSortButtons('win_rate')}</th>
        </tr>
      </thead>
                <tbody>
                    {renderTableRows()}
                </tbody>
            </table>
            <div className="pagination">
                {currentPage > 1 && (
                    <button onClick={() => handlePageChange(currentPage - 1)}>← Prev</button>
                )}
                <span>Page {currentPage} of {totalPages}</span>
                {currentPage < totalPages && (
                    <button onClick={() => handlePageChange(currentPage + 1)}>Next →</button>
                )}
            </div>
        </div>
    );
}

export default Stats;