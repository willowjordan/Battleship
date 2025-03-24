import random
import time

from cpu import * # CPUs, Board, Ship, etc

class Player():
    def __init__(self):
        self.board = Board()
    
    def sendConfirmation(self): """Send confirmation to computer that local player has finished setting up their pieces."""; raise NotImplementedError()
    def getConfirmation(self): """Wait for confirmation that other player is ready."""; raise NotImplementedError()
    def sendMove(self, move:tuple): """Send move to opponent. Returns the result of the move."""; raise NotImplementedError()
    def getMove(self): """Get move from opponent"""; raise NotImplementedError()
    def sendMoveResult(self, move:tuple, result:Result): """Send an opponent a move they made and the result of the move."""; raise NotImplementedError()

class RemotePlayer(Player):
    def __init__(self):
        super().__init__()

    def sendConfirmation(self):
        pass

    def getConfirmation(self):
        pass

class ComputerPlayer(Player):
    def __init__(self, ai:CPU):
        super().__init__()
        self.ai = ai
        self.ai.setBoard(self.board)
    
    def sendConfirmation(self):
        pass
    
    def getConfirmation(self):
        self.ai.setup()
        return True

    def sendMove(self, move:tuple):
        return self.board.addEnemyShot(move)
    
    def getMove(self):
        return self.ai.getMove()
    
    def sendMoveResult(self, move:tuple, result:Result):
        self.board.addMyShot(move, result)
        self.ai.lastmove = move
        self.ai.lastresult = result
        