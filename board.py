from enum import Enum
from ship import Ship

class Result(Enum):
    MISS = 0
    HIT = 1
    SUNK = 2

class DuplicateShotError(Exception):
    """Exception raised when a player or opponent attempts to fire a shot in the same place twice."""
    def __init__(self, message):
        super().__init__(message)

class Board():
    def __init__(self, ships=None):
        # shots the enemy has fired onto your grid
        # format - (xpos:int, ypos:int) => hit:bool
        self.enemyshots = {}
        # shots you have fired onto the enemy's grid
        # format - (xpos:int, ypos:int) => hit:bool
        self.myshots = {}
        self.occupiedspaces = []
        self.aliveShips = []
        self.deadShips = []

        # constants
        self.MIN_X = 1
        self.MAX_X = 10
        self.MIN_Y = 1
        self.MAX_Y = 10

        if ships is not None:
            for s in ships:
                self.addShip(s)

    def getNeighbors(self, pos):
        """Return a list of valid neighboring squares of position pos."""
        rv = []
        for dir in Ship.POSSIBLE_DIRECTIONS:
            neighbor = (pos[0] + dir[0], pos[1] + dir[1])
            if (neighbor[0] < self.MIN_X) | (neighbor[0] > self.MAX_X): continue
            if (neighbor[1] < self.MIN_Y) | (neighbor[1] > self.MAX_Y): continue
            rv.append(neighbor)
        return rv
    
    def addShip(self, ship):
        self.aliveShips.append(ship)
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
        
        for ship in self.aliveShips:
            if pos in ship.spaces:
                self.enemyshots[pos] = True # hit
                ship.spaces.remove(pos)
                if ship.isSunk():
                    self.aliveShips.remove(ship)
                    self.deadShips.append(ship)
                    return Result.SUNK # tells calling function to check victory conditions
                else: return Result.HIT
        self.enemyshots[pos] = False # miss
        return Result.MISS
    
    def isShipValid(self, ship:Ship):
        """Return 0 if ship placement is valid, 1 if out of bounds, 2 if inside an existing ship"""
        for space in ship.spaces:
            if (space[0] < self.MIN_X) | (space[0] > self.MAX_X) | (space[1] < self.MIN_Y) | (space[1] > self.MAX_Y):
                return 1
            if space in self.occupiedspaces:
                return 2
        return 0

    def lastShipSunk(self):
        """Return the last ship sunk"""
        return self.deadShips[len(self.deadShips)-1]