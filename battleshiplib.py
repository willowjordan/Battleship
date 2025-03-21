import random
from enum import Enum
import time

class Result(Enum):
    MISS = 0
    HIT = 1
    SUNK = 2

class DuplicateShotError(Exception):
    """Exception raised when a player or opponent attempts to fire a shot in the same place twice."""
    def __init__(self, message):
        super().__init__(message)

class Ship():
    def __init__(self, pos:tuple, l:int, d:tuple, name:str=""):
        """
        :param pos: tuple(int, int) for the position of the origin of the ship
        :param l: int for length
        :param d: tuple(int, int) for direction the ship is pointing in; can be (1, 0), (0, 1), (-1, 0), or (0, -1)
        :param name: name/id of the ship
        """
        if d not in [(1, 0), (0, 1), (-1, 0), (0, -1)]: raise(ValueError, "Bad direction value")
        self.name = name
        self.pos = pos
        self.length = l
        self.direction = d
        self.generateSpaces()
    
    def generateSpaces(self):
        """Generate spaces list for ship based on position, length, and direction. ONLY use this function in SETUP PHASE"""
        self.spaces = [] # all spaces the ship occupies
        for i in range(0, self.length):
            self.spaces.append((self.pos[0] + self.direction[0]*i, self.pos[1] + self.direction[1]*i))
        self.spaces.sort()

    def translate(self, transVector:tuple):
        """Translate the ship based on translation vector. ONLY use this function in SETUP PHASE"""
        self.pos = (self.pos[0] + transVector[0], self.pos[1] + transVector[1])
        for i in range(0, len(self.spaces)):
            self.spaces[i] = (self.spaces[i][0] + transVector[0], self.spaces[i][1] + transVector[1])
        self.spaces.sort()
    
    def rotate(self):
        """Rotate the ship clockwise one time. ONLY use this function in SETUP PHASE"""
        # change direction var
        if self.direction == (1, 0):
            self.direction = (0, 1)
        elif self.direction == (0, 1):
            self.direction = (-1, 0)
        elif self.direction == (-1, 0):
            self.direction = (0, -1)
        elif self.direction == (0, -1):
            self.direction = (1, 0)
        else: raise(ValueError, "Bad direction value")

        self.generateSpaces()
    
    def isSunk(self):
        return len(self.spaces) == 0

class Board():
    def __init__(self, ships=None):
        self.ships = {}
        # shots the enemy has fired onto your grid
        # format - (xpos:int, ypos:int) => hit:bool
        self.enemyshots = {}
        # shots you have fired onto the enemy's grid
        # format - (xpos:int, ypos:int) => hit:bool
        self.myshots = {}
        self.occupiedspaces = []

        # constants
        self.MIN_X = 1
        self.MAX_X = 10
        self.MIN_Y = 1
        self.MAX_Y = 10

        if ships is not None:
            for s in ships:
                self.addShip(s)
    
    def addShip(self, ship):
        self.ships[ship.name] = ship
        for space in ship.spaces:
            self.occupiedspaces.append(space)

    def addMyShot(self, pos, result):
        """Add a shot to targeting board"""
        if pos in self.myshots:
            raise DuplicateShotError("There is already a shot there!")
        self.myshots[pos] = result

    def addEnemyShot(self, pos):
        """Add an enemy shot to the primary board and return the result of the shot"""
        if pos in self.enemyshots:
            raise DuplicateShotError("There is already an enemy shot there!")
        
        for ship in self.ships.values():
            if pos in ship.spaces:
                self.enemyshots[pos] = True # hit
                ship.spaces.remove(pos)
                if ship.isSunk(): return Result.SUNK # tells calling function to check victory conditions
                else: return Result.HIT
        self.enemyshots[pos] = False # miss
        return Result.MISS

    def allShipsSunk(self):
        for ship in self.ships:
            if not ship.isSunk(): return False
        return True
    
    def isShipValid(self, ship:Ship):
        """Returns 0 if ship placement is valid, 1 if out of bounds, 2 if inside an existing ship"""
        for space in ship.spaces:
            if (space[0] < self.MIN_X) | (space[0] > self.MAX_X) | (space[1] < self.MIN_Y) | (space[1] > self.MAX_Y):
                return 1
            if space in self.occupiedspaces:
                return 2
        return 0

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
    def __init__(self):
        super().__init__()
    
    def sendConfirmation(self):
        pass
    
    def getConfirmation(self):
        self.setupBoard()
        return True

    def setupBoard(self):
        time.sleep(random.random() * 5) # add random time delay to make player think computer is running some super fancy algorithm
        b = self.board
        shipsToPlace = [(5, "Carrier"), (4, "Battleship"), (3, "Destroyer"), (3, "Submarine"), (2, "Patrol Boat")]
        while len(shipsToPlace) > 0:
            nextShipInfo = shipsToPlace[0]
            shipsToPlace.pop(0)
            valid = -1
            while valid != 0:
                pos = (random.randint(b.MIN_X, b.MAX_X), random.randint(b.MIN_Y, b.MAX_Y))
                direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
                nextShip = Ship(pos, nextShipInfo[0], direction, nextShipInfo[1])
                valid = b.isShipValid(nextShip)
            b.addShip(nextShip)

    def sendMove(self, move:tuple):
        return self.board.addEnemyShot(move)
    
    def getMove(self):
        time.sleep(random.random() * 2) # add random time delay to make player think computer is running some super fancy algorithm
        b = self.board
        valid = False
        while not valid:
            move = (random.randint(b.MIN_X, b.MAX_X), random.randint(b.MIN_Y, b.MAX_Y))
            if move not in b.myshots:
                valid = True
        return move
    
    def sendMoveResult(self, move:tuple, result:Result):
        self.board.addMyShot(move, result)
        