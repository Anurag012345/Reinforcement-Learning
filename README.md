
# Tic-Tac-Toe Web Application

This is a web-based Tic-Tac-Toe game where you can play against a computer. The computer uses a trained policy to make its moves. The game is built using Flask for the backend and plain HTML, CSS, and JavaScript for the frontend.

## Features

- Play Tic-Tac-Toe against a computer.
- The computer's moves are determined by a trained policy.
- The board updates in real-time.
- The game declares a winner or a tie at the end of each game.

## Requirements

- Python 3.x
- Flask
- Numpy

## Setup and Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/tic-tac-toe.git
cd tic-tac-toe
```

2. **Set up a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required packages:**

```bash
pip install flask numpy
```

4. **Prepare the trained policy:**

Ensure you have a trained policy file named `policy_p1` in the same directory. You can train the policy using the provided `tic_tac_toe.py` script by running the training phase:

```python
from tic_tac_toe import State, Player

p1 = Player("p1")
p2 = Player("p2")
state = State(p1, p2)
state.Play(10000)
p1.savePolicy()
```

5. **Run the Flask server:**

```bash
python app.py
```

6. **Open your browser and navigate to:**

```
http://127.0.0.1:5000/
```

## File Structure

```
tic-tac-toe/
├── templates/
│   └── index.html
├── app.py
├── tic_tac_toe.py
└── README.md
```

- `templates/index.html`: Contains the HTML, CSS, and JavaScript for the frontend.
- `app.py`: Flask application that handles the game logic and routes.
- `tic_tac_toe.py`: Contains the game logic and player classes.
- `README.md`: Project documentation.

## How to Play

1. Open the game in your browser.
2. Click on a cell to make your move as the human player.
3. The computer will automatically make its move.
4. The game will continue until there is a winner or a tie.
5. Click the "Reset" button to start a new game.

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.
