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


