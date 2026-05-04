from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
# Configure CORS to allow requests from frontend server
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8000", "http://127.0.0.1:8000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

class TicTacToe5x5:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.current_player = 'X'
        self.winner = None
        self.difficulty = 'medium'

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.winner:
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                self.winner = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self, row, col):
        directions = [
            [(0,1),(0,-1)],  # Horizontal
            [(1,0),(-1,0)],  # Vertical
            [(1,1),(-1,-1)],  # Diagonal \
            [(1,-1),(-1,1)]   # Diagonal /
        ]
        for dir_pair in directions:
            count = 1
            for dr, dc in dir_pair:
                r, c = row+dr, col+dc
                while 0<=r<5 and 0<=c<5 and self.board[r][c]==self.current_player:
                    count += 1
                    r += dr
                    c += dc
                    if count >= 4:
                        return True
        return False

game = TicTacToe5x5()
stats = {'wins': 0, 'losses': 0, 'draws': 0}

def find_winning_move(player):
    for i in range(5):
        for j in range(5):
            if game.board[i][j] == ' ':
                game.board[i][j] = player
                if game.check_winner(i, j):
                    game.board[i][j] = ' '
                    return (i, j)
                game.board[i][j] = ' '
    return None

def evaluate_board():
    score = 0
    # [Previous evaluation logic]
    return score

def get_best_move():
    best_score = -float('inf')
    best_move = None
    for i in range(5):
        for j in range(5):
            if game.board[i][j] == ' ':
                game.board[i][j] = 'O'
                current_score = evaluate_board()
                game.board[i][j] = ' '
                if current_score > best_score:
                    best_score = current_score
                    best_move = (i, j)
    return best_move

def random_ai_move():
    empty = [(i,j) for i in range(5) for j in range(5) if game.board[i][j]==' ']
    return random.choice(empty) if empty else (0,0)

def get_ai_move():
    if game.difficulty == 'easy':
        return random_ai_move()
    elif game.difficulty == 'hard':
        if win_move := find_winning_move('O'):
            return win_move
        if block_move := find_winning_move('X'):
            return block_move
        return get_best_move()
    else:  # medium
        if random.random() < 0.7:
            if win_move := find_winning_move('O'):
                return win_move
            if block_move := find_winning_move('X'):
                return block_move
            return get_best_move()
        return random_ai_move()

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    game.difficulty = data.get('difficulty', 'medium')
    
    if game.make_move(data['row'], data['col']):
        response = {
            'board': game.board,
            'gameOver': game.winner is not None,
            'winner': game.winner
        }
        
        if not game.winner:
            ai_move = get_ai_move()
            game.make_move(ai_move[0], ai_move[1])
            response.update({
                'board': game.board,
                'gameOver': game.winner is not None,
                'winner': game.winner,
                'aiMove': ai_move
            })
        
        if game.winner:
            stats['wins' if game.winner == 'X' else 'losses'] += 1
            response['stats'] = stats
            
        return jsonify(response)
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/reset', methods=['POST'])
def reset():
    game.reset()
    return jsonify({
        'board': game.board,
        'stats': stats
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(stats)

if __name__ == '__main__':
    app.run(port=5001, debug=True)