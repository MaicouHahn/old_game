from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Constantes do jogo
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ''
WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

# Variáveis globais
board = [EMPTY] * 9
current_player = PLAYER_X
scoreboard = {"wins": 0, "losses": 0, "draws": 0}
ai_enabled = False

def check_winner(board):
    for combo in WINNING_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != EMPTY:
            return board[combo[0]]
    if EMPTY not in board:
        return 'Tie'
    return None

def ai_move(board):
    for i in range(len(board)):
        if board[i] == EMPTY:
            return i

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global board, current_player, scoreboard, ai_enabled

    data = request.get_json()
    player_move = data['player_move']

    if board[player_move] == EMPTY:
        board[player_move] = current_player
        winner = check_winner(board)
        if winner:
            if winner == 'X':
                scoreboard['wins'] += 1
            elif winner == 'O':
                scoreboard['losses'] += 1
            else:
                scoreboard['draws'] += 1
            return jsonify({'board': board, 'winner': winner, 'scoreboard': scoreboard})
        
        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X

        if current_player == PLAYER_O and ai_enabled:
            ai_move_index = ai_move(board)
            board[ai_move_index] = current_player
            winner = check_winner(board)
            if winner:
                if winner == 'X':
                    scoreboard['wins'] += 1
                elif winner == 'O':
                    scoreboard['losses'] += 1
                else:
                    scoreboard['draws'] += 1
                return jsonify({'board': board, 'winner': winner, 'scoreboard': scoreboard})
            
            current_player = PLAYER_X

    return jsonify({'board': board, 'winner': None, 'scoreboard': scoreboard})

@app.route('/restart', methods=['POST'])
def restart():
    global board, current_player
    board = [EMPTY] * 9
    current_player = PLAYER_X
    return jsonify({'board': board, 'winner': None, 'scoreboard': scoreboard})

@app.route('/toggle_ai', methods=['POST'])
def toggle_ai():
    global ai_enabled
    ai_enabled = not ai_enabled
    return jsonify({'ai_enabled': ai_enabled})

if __name__ == '__main__':
    app.run(debug=True)
