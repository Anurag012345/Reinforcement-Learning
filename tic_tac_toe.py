import pickle
import numpy as np

NUMBER_OF_ROWS = 3  # Define the value of NUMBER_OF_ROWS
NUMBER_OF_COLUMNS = 3 # Define the value of NUMBER_OF_COLUMNS

class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS))
        self.p1 = p1
        self.p2 = p2
        self.playerSymbol = 1
        self.boardHash = None
        self.isEnd = False
        self.moves = []

    # get unique hash of current board state
    def getHash(self):
        self.boardHash = str(self.board.reshape(NUMBER_OF_ROWS * NUMBER_OF_COLUMNS))
        return self.boardHash

    # Function to update the State
    def updateState(self, position):
        self.board[position] = self.playerSymbol
        self.moves.append(position)
        # Remove the oldest move if more than 4 moves
        if len(self.moves) > 4:
            oldest_move = self.moves.pop(0)
            self.board[oldest_move] = 0
        # Switch the Player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # Function to check if the game has ended
    def winner(self):
        # scan rows for Winner
        for i in range(NUMBER_OF_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1

        # scan columns for Winner
        for i in range(NUMBER_OF_COLUMNS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1

        # check diagonals
        diag_sum1 = sum([self.board[i, i] for i in range(NUMBER_OF_COLUMNS)])
        diag_sum2 = sum([self.board[i, NUMBER_OF_COLUMNS - i - 1] for i in range(NUMBER_OF_COLUMNS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        # check if diagonals are occupied by the same player
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1

        # check if tie
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # game is still going on
        self.isEnd = False
        return None

    # Function to check the available positions
    def availablePositions(self):
        positions = []
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLUMNS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    # Function to reset the board
    def reset(self):
        self.board = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1
        self.moves = []

    # Give Reward at the end of the Game
    def giveReward(self):
        result = self.winner()
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    # Function to play the game
    def Play(self, rounds=100):
        for i in range(rounds):
            if i % 1000 == 0:
                print("Rounds {}".format(i))
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.decideAction(positions, self.board, self.playerSymbol)
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                win = self.winner()
                if win is not None:
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.decideAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)
                    win = self.winner()
                    if win is not None:
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break

    # Play Against Human
    def PlayHuman(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.decideAction(positions, self.board, self.playerSymbol)
            self.updateState(p1_action)
            self.showBoard()
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("Tie!")
                self.reset()
                break
            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.decideAction(positions)
                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("Tie!")
                    self.reset()
                    break

    # Function to display the Current State of the Board
    def showBoard(self):
        for i in range(NUMBER_OF_ROWS):
            print('-------------')
            out = '| '
            for j in range(NUMBER_OF_COLUMNS):
                if self.board[i, j] == 1:
                    token = '*'
                if self.board[i, j] == -1:
                    token = 'x'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '  # type: ignore
            print(out)
        print('-------------')


class Player:
    def __init__(self, name, exploration_rate=0.3):
        self.name = name
        self.exploration_rate = exploration_rate
        self.states = []
        self.decay_gamma = 0.9
        self.lr = 0.2
        self.states_value = {}  # state: value

    def decideAction(self, position, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exploration_rate:
            idx = np.random.choice(len(position))
            action = position[idx]
        else:
            value_max = -999
            for p in position:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = str(next_board.reshape(NUMBER_OF_ROWS * NUMBER_OF_COLUMNS))
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                if value >= value_max:  # type: ignore
                    value_max = value
                    action = p
        return action

    def getHash(self, board):
        return str(board.reshape(NUMBER_OF_ROWS * NUMBER_OF_COLUMNS))

    def reset(self):
        self.states = []

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]


    def addState(self, state):
        self.states.append(state)

    def loadPolicy(self, file):
        import pickle
        self.states_value = pickle.load(open(file, 'rb'))

    def savePolicy(self):
        import pickle
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def decideAction(self, position):
        while True:
            row = int(input("Enter row value:"))
            col = int(input("Enter column value:"))
            action = (row, col)
            if action in position:
                return action

    def reset(self):
        pass

    def feedReward(self, reward):
        pass

    def addState(self, state):
        pass


if __name__ == "__main__":
     # Training Phase
     p1 = Player("p1")
     p2 = Player("p2")

     state = State(p1, p2)
     print("Training...")

     state.Play(10000)

     p1.savePolicy()

     # Play Against Human
     p1 = Player("computer", exploration_rate=0.1)
     p1.loadPolicy("policy_p1")

     p2 = HumanPlayer("human")
     state = State(p1, p2)
     state.PlayHuman()





