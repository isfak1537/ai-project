class TicTacToe5x5:
    def __init__(self):
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.current_player = 'X'
        self.winner = None

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.winner:
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                self.winner = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self, row, col):
        # Check row, column, and diagonals for 4 consecutive marks
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],   # Vertical
            [(1, 1), (-1, -1)],  # Diagonal
            [(1, -1), (-1, 1)]    # Anti-diagonal
        ]
        for dir_pair in directions:
            count = 1
            for dr, dc in dir_pair:
                r, c = row + dr, col + dc
                while 0 <= r < 5 and 0 <= c < 5 and self.board[r][c] == self.current_player:
                    count += 1
                    r += dr
                    c += dc
                    if count == 4:
                        return True
        return False

    def reset(self):
        self.__init__()