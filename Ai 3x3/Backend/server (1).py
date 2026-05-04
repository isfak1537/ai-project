
from flask import Flask, request, jsonify
from flask_cors import CORS
from game import TicTacToe
from minimax_agent import MinimaxAgent

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

game = TicTacToe()
agent = MinimaxAgent()
stats = {'wins': 0, 'losses': 0, 'draws': 0}

@app.route('/reset', methods=['POST', 'OPTIONS'])
def reset():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.get_json()
    difficulty = data.get('difficulty', 'medium')
    agent.difficulty = difficulty
    agent.set_difficulty()

    state = game.reset()
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'stats': stats
    })

@app.route('/move', methods=['POST', 'OPTIONS'])
def make_move():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.get_json()
    position = data['position']

    if game.make_move(position):
        response = {
            'board': game.board,
            'gameOver': game.game_over,
            'winner': game.winner
        }

        if game.game_over:
            update_stats(game.winner)
            response['stats'] = stats
        elif not game.game_over:
            state = game.get_state()
            valid_moves = game.get_valid_moves()
            ai_move = agent.get_action(state, valid_moves)
            game.make_move(ai_move)

            response.update({
                'board': game.board,
                'gameOver': game.game_over,
                'winner': game.winner,
                'aiMove': ai_move
            })

            if game.game_over:
                update_stats(game.winner)
                response['stats'] = stats

        return jsonify(response)
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/undo', methods=['POST', 'OPTIONS'])
def undo_move():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    if hasattr(game, 'undo') and game.undo():
        return jsonify({
            'board': game.board,
            'currentPlayer': game.current_player
        })
    return jsonify({'error': 'Cannot undo'}), 400

@app.route('/stats', methods=['GET', 'OPTIONS'])
def get_stats():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    return jsonify(stats)

def update_stats(winner):
    if winner == 'X':
        stats['wins'] += 1
    elif winner == 'O':
        stats['losses'] += 1
    else:
        stats['draws'] += 1

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
