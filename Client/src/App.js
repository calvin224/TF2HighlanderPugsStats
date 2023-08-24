import React, { useState } from 'react';
import './App.css';
import Stats from './Stats';
import Leaderboard from './Leaderboard';

function App() {
  // Function to scroll down to the table
  const scrollToTable = () => {
    const table = document.getElementById('stats-table');
    if (table) {
      table.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // State to manage which page is active
  const [activePage, setActivePage] = useState('stats');

  return (
    <div className="App">
      <header
        className="App-header"
        style={{
          backgroundImage: `url(./Product.jpg)`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          minHeight: '100vh',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flexDirection: 'column',
        }}
      >
        <div className="header-content">
          <h1 style={{ color: '#fff', fontSize: '2rem', marginBottom: '20px' }}>
            EU Highlander Pugs Stats
          </h1>
          <div className="centered-image" onClick={scrollToTable}></div>
        </div>
      </header>
      <main>
        {/* Fixed navigation buttons */}
        <div className="fixed-buttons">
          <button
            className={`button ${activePage === 'stats' ? 'active-button' : ''}`}
            onClick={() => setActivePage('stats')}
          >
            Go to Stats
          </button>
          <button
            className={`button ${activePage === 'leaderboard' ? 'active-button' : ''}`}
            onClick={() => setActivePage('leaderboard')}
          >
            Go to Leaderboard
          </button>
        </div>

        {/* Content based on activePage */}
        {activePage === 'stats' && <Stats id="stats-table" />}
        {activePage === 'leaderboard' && <Leaderboard id="Leaderboard" />}
      </main>

      {/* Footer with GitHub icon */}
      <footer className="App-footer">
        <p>
          <a
            href="https://github.com/Kosuketf2/HLPugsStatistics" // Replace with your GitHub profile URL
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#ffffff', textDecoration: 'none' }}
          >
            <i className="fab fa-github"></i> GitHub
          </a>
            <a
            href="404" // Replace with your GitHub profile URL
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#ffffff', textDecoration: 'none' }}
          >
            <i className="fab fa-github"></i> Api Doc
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
