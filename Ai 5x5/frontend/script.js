document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = 'http://localhost:5001';
    const board = document.getElementById('board');
    const status = document.getElementById('status');
    const resetBtn = document.getElementById('reset');
    const themeBtn = document.getElementById('theme-toggle');
    const difficultySelect = document.getElementById('difficulty');
    const winsElement = document.getElementById('wins');
    const lossesElement = document.getElementById('losses');
    const drawsElement = document.getElementById('draws');
    const loadingIndicator = document.getElementById('loading');

    let gameActive = true;

    function init() {
        renderBoard();
        initTheme();
        initGame();
    }

    function initTheme() {
        const darkMode = localStorage.getItem('darkMode') === 'true';
        document.body.classList.toggle('dark-mode', darkMode);
        updateThemeButton();
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        updateThemeButton();
    }

    function updateThemeButton() {
        themeBtn.textContent = document.body.classList.contains('dark-mode') 
            ? '☀️ Light Mode' 
            : '🌙 Dark Mode';
    }

    function renderBoard() {
        board.innerHTML = '';
        for (let i = 0; i < 5; i++) {
            for (let j = 0; j < 5; j++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = i;
                cell.dataset.col = j;
                cell.addEventListener('click', handleCellClick);
                board.appendChild(cell);
            }
        }
    }

    async function initGame() {
        gameActive = true;
        try {
            loadingIndicator.style.display = 'block';
            const response = await fetch(`${API_BASE}/reset`, { 
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            updateBoard(data.board);
            updateStats(data.stats);
            status.textContent = `Your turn (X) - ${difficultySelect.value} mode`;
        } catch (error) {
            console.error('Init error:', error);
            status.textContent = 'Error initializing game. Please ensure: \n1. Backend is running (python server.py)\n2. You are accessing via http://localhost:8000';
        } finally {
            loadingIndicator.style.display = 'none';
        }
    }

    async function handleCellClick(e) {
        if (!gameActive) return;
        
        const cell = e.target;
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        
        try {
            cell.classList.add('loading');
            
            const response = await fetch(`${API_BASE}/move`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 
                    row, 
                    col,
                    difficulty: difficultySelect.value
                })
            });
            
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            updateBoard(data.board);
            
            if (data.gameOver) {
                gameActive = false;
                status.textContent = data.winner 
                    ? (data.winner === 'X' ? 'You win! 🎉' : 'AI wins! 🤖')
                    : "It's a draw!";
            } else {
                status.textContent = `Your turn (X) - ${difficultySelect.value} mode`;
            }
            
            if (data.stats) updateStats(data.stats);
            
        } catch (error) {
            console.error('Move error:', error);
            status.textContent = 'Error making move. Please try again.';
        } finally {
            cell.classList.remove('loading');
        }
    }

    function updateBoard(board) {
        document.querySelectorAll('.cell').forEach((cell, index) => {
            const row = Math.floor(index / 5);
            const col = index % 5;
            cell.textContent = board[row][col];
            cell.className = 'cell';
            if (board[row][col] === 'X') cell.classList.add('x');
            if (board[row][col] === 'O') cell.classList.add('o');
        });
    }

    function updateStats(stats) {
        winsElement.textContent = stats?.wins || 0;
        lossesElement.textContent = stats?.losses || 0;
        drawsElement.textContent = stats?.draws || 0;
    }

    resetBtn.addEventListener('click', initGame);
    themeBtn.addEventListener('click', toggleTheme);
    difficultySelect.addEventListener('change', initGame);

    init();
});