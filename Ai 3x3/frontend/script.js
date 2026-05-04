document.addEventListener('DOMContentLoaded', () => {
    // Configuration
    const API_BASE = 'http://localhost:5001'; // Directly use development URL
    
    // DOM Elements
    const board = document.getElementById('board');
    const status = document.getElementById('status');
    const resetBtn = document.getElementById('reset');
    const undoBtn = document.getElementById('undo');
    const themeBtn = document.getElementById('theme-toggle');
    const difficultySelect = document.getElementById('difficulty');

    // Helper Functions
    const updateBoard = (boardState) => {
        document.querySelectorAll('.cell').forEach((cell, i) => {
            cell.textContent = boardState[i];
            cell.className = 'cell';
            if (boardState[i] === 'X') cell.classList.add('x');
            if (boardState[i] === 'O') cell.classList.add('o');
        });
    };

    const updateStats = (stats) => {
        document.getElementById('wins').textContent = stats.wins;
        document.getElementById('losses').textContent = stats.losses;
        document.getElementById('draws').textContent = stats.draws;
    };

    const toggleTheme = () => {
        document.body.classList.toggle('dark-mode');
        themeBtn.textContent = document.body.classList.contains('dark-mode') 
            ? '☀️ Light Mode' 
            : '🌙 Dark Mode';
    };

    // Core Game Functions
    const safeFetch = async (endpoint, options = {}) => {
        const url = `${API_BASE}${endpoint}`;
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...(options.headers || {})
                },
                mode: 'cors'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Fetch error:', {
                error,
                url,
                config: options
            });
            status.textContent = 'Connection error. Please:';
            status.innerHTML += '<br>1. Ensure backend is running (port 5001)';
            status.innerHTML += '<br>2. Open via http://localhost:8000';
            throw error;
        }
    };

    const handleCellClick = async (e) => {
        const cell = e.target;
        if (!cell.classList.contains('cell')) return;
        
        try {
            const index = parseInt(cell.dataset.index);
            const data = await safeFetch('/move', {
                method: 'POST',
                body: JSON.stringify({ position: index })
            });
            
            updateBoard(data.board);
            
            if (data.gameOver) {
                status.textContent = data.winner 
                    ? `Player ${data.winner} wins!` 
                    : "Game ended in a draw!";
                if (data.stats) updateStats(data.stats);
            } else {
                status.textContent = 'Your turn (X)';
            }
        } catch (error) {
            console.error('Move error:', error);
        }
    };

    const undoMove = async () => {
        try {
            const data = await safeFetch('/undo', { method: 'POST' });
            updateBoard(data.board);
            status.textContent = `Your turn (${data.currentPlayer})`;
        } catch (error) {
            console.error('Undo error:', error);
        }
    };

    const initGame = async () => {
        try {
            status.textContent = 'Starting game...';
            const difficulty = difficultySelect.value;
            const data = await safeFetch('/reset', {
                method: 'POST',
                body: JSON.stringify({ difficulty })
            });
            updateBoard(data.board);
            updateStats(data.stats || {wins: 0, losses: 0, draws: 0});
            status.textContent = 'Your turn (X)';
        } catch (error) {
            console.error('Init error:', error);
        }
    };

    // Initialize Game
    (() => {
        // Create board cells
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.index = i;
            board.appendChild(cell);
        }

        // Set up event listeners
        board.addEventListener('click', handleCellClick);
        resetBtn.addEventListener('click', initGame);
        undoBtn.addEventListener('click', undoMove);
        themeBtn.addEventListener('click', toggleTheme);

        // Start the game
        initGame();
    })();
});