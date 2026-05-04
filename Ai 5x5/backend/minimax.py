def minimax(board, depth, is_maximizing, check_winner, is_full, alpha=-float('inf'), beta=float('inf')):
    # Terminal checks
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if depth == 0 or is_full(board):
        return 0  # Could replace with a heuristic if desired

    if is_maximizing:  # AI's turn ('O')
        max_eval = -float('inf')
        for i in range(5):
            for j in range(5):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth - 1, False, check_winner, is_full, alpha, beta)
                    board[i][j] = ' '
                    if eval > max_eval:
                        max_eval = eval
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # breaks inner loop
            if beta <= alpha:
                break  # break outer loop as well
        return max_eval
    else:  # Human's turn ('X')
        min_eval = float('inf')
        for i in range(5):
            for j in range(5):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth - 1, True, check_winner, is_full, alpha, beta)
                    board[i][j] = ' '
                    if eval < min_eval:
                        min_eval = eval
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, check_winner, is_full, depth=3):
    best_score = -float('inf')
    best_move = (-1, -1)
    for i in range(5):
        for j in range(5):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, depth, False, check_winner, is_full)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move
