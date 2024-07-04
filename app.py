from flask import Flask, jsonify, request, render_template
from tic_tac_toe import State, Player, HumanPlayer

app = Flask(__name__)

p1 = Player("computer", exploration_rate=0.1)
p1.loadPolicy("policy_p1")
p2 = HumanPlayer("human")
state = State(p1, p2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    position = (data['row'], data['col']) # type: ignore
    state.updateState(position)
    result = state.winner()
    
    # Check if human's move resulted in a win or tie
    if result is None:
        # Computer's turn
        positions = state.availablePositions()
        p1_action = p1.decideAction(positions, state.board, state.playerSymbol)
        state.updateState(p1_action)
        result = state.winner()
    
    response = {'board': state.board.tolist(), 'result': result}
    return jsonify(response)

@app.route('/reset', methods=['POST'])
def reset():
    state.reset()
    return jsonify({'board': state.board.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
