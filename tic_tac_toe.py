import numpy as np;

NUMBER_OF_ROWS = 3  # Define the value of NUMBER_OF_ROWS
NUMBER_OF_COLUMNS = 3 # Define the value of NUMBER_OF_COLUMNS
class State:

    def __init__(self, p1,p2):
        self.board = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS))
        self.p1 = p1
        self.p2 = p2
        self.playerSymbol = 1
        self.boardHash = None
        self.isEnd = False
    
    # get unique hash of current board state
    def getHash(self):
        self.boardHash = str(self.board.reshape(NUMBER_OF_ROWS*NUMBER_OF_COLUMNS))
        return self.boardHash
    
    # Function to Update the State
    def updateState(self,position):
        #Lock the position
        self.board[position] = self.playerSymbol
        #Switch the Player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # Function to check if the game has ended
    def winner(self):
        #scan rows for Winner
        for i in range(NUMBER_OF_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
            
        #scan columns for Winner
        for i in range (NUMBER_OF_COLUMNS):
            if sum(self.board[:,i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:,i]) == -3:
                self.isEnd = True
                return -1
        #check diagonals
        diag_sum1 = sum([self.board[i, i] for i in range(NUMBER_OF_COLUMNS)])
        diag_sum2 = sum([self.board[i, NUMBER_OF_COLUMNS-i-1] for i in range(NUMBER_OF_COLUMNS)])
        diag_sum = max(abs(diag_sum1),abs(diag_sum2))
        #check if diagonal are occupied by same player
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1
            
        #check if tie
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        #game is still going on
        self.isEnd = False
        return None
    
    # Function to check the available positions
    def availablePositions(self):
        positions = []
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLUMNS):
                if self.board[i,j] == 0:
                    positions.append((i,j))
        return positions
    
    # Function to reset the board
    def reset(self):
        self.board = np.zeros((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

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
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
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
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
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
    
    #Play Against Human
    def PlayHuman(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
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
                p2_action = self.p2.chooseAction(positions)
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
                out += token + ' | '
            print(out)
        print('-------------')


class Player:

    #deafult Constructor
    def __init__(self,name,exploration_rate=0.3):
        self.name = name
        self.exploration_rate = exploration_rate

        #List to record the positions taken
        self.states = []
        self.decay_gamma = 0.9
        self.lr = 0.2
        self.states_value = {} #state: value




