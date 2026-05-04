
import random

class MinimaxAgent:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.set_difficulty()

    def set_difficulty(self):
        if self.difficulty == 'easy':
            self.random_prob = 0.5
        elif self.difficulty == 'hard':
            self.random_prob = 0.0
        else:
            self.random_prob = 0.2

    def get_action(self, state, valid_moves):
        if random.random() < self.random_prob:
            return random.choice(valid_moves)
        else:
            board = list(state)
            best_score = float('-inf')
            best_move = None
            for move in valid_moves:
                board[move] = 'O'
                score = self.minimax(board, False)
                board[move] = ' '
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move

    def minimax(self, board, is_maximizing):
        winner = self.check_winner(board)
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, board):
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for a, b, c in win_combos:
            if board[a] != ' ' and board[a] == board[b] == board[c]:
                return board[a]
        return None
