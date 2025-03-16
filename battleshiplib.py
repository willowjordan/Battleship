import random

class Ship():
    # pos:[int, int] - position of the origin of the ship
    # l:int - length
    # d:[int, int] - direction the ship is pointing in; can be (1, 0), (0, 1), (-1, 0), or (0, -1)
    # name:str - name/id of ship
    def __init__(self, pos:tuple, l:int, d:tuple, name:str=""):
        if d not in [(1, 0), (0, 1), (-1, 0), (0, -1)]: raise(ValueError, "Bad direction value")
        self.name = name
        self.pos = pos
        self.length = l
        self.direction = d
        self.generateSpaces()
    
    # ONLY use this function in SETUP PHASE
    def generateSpaces(self):
        self.spaces = [] # all spaces the ship occupies
        for i in range(0, self.length):
            self.spaces.append((self.pos[0] + self.direction[0]*i, self.pos[1] + self.direction[1]*i))
        self.spaces.sort()

    # translate the ship based on translation vector
    # ONLY use this function in SETUP PHASE
    def translate(self, transVector:tuple):
        self.pos = (self.pos[0] + transVector[0], self.pos[1] + transVector[1])
        for i in range(0, len(self.spaces)):
            self.spaces[i] = (self.spaces[i][0] + transVector[0], self.spaces[i][1] + transVector[1])
        self.spaces.sort()
    
    # rotate the ship clockwise one time
    # ONLY use this function in SETUP PHASE
    def rotate(self):
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
        return len(self.spaces == 0)

class Board():
    def __init__(self, ships=None):
        self.ships = {}
        # shots the enemy has fired onto your grid
        # format - (xpos:int, ypos:int, hit:bool)
        self.enemyshots = []
        # shots you have fired onto the enemy's grid
        # format - (xpos:int, ypos:int, hit:bool)
        self.myshots = []
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

    def addEnemyShot(self, pos):
        # error checking
        if pos in self.enemyshots:
            raise(ValueError, "There is already an enemy shot there!")
        
        for ship in self.ships:
            if pos in ship.spaces:
                self.enemyshots.append(pos + True)
                ship.spaces.remove(pos)
                if ship.isSunk(): return 1 # tells calling function to check victory conditions
                else: return 0
        self.enemyshots.append(pos + False) # miss

    def allShipsSunk(self):
        for ship in self.ships:
            if not ship.isSunk(): return False
        return True
    
    # return 0 if valid
    # return 1 if out of bounds
    # return 2 if inside an already placed ship
    def isShipValid(self, ship:Ship):
        for space in ship.spaces:
            if (space[0] < self.MIN_X) | (space[0] > self.MAX_X) | (space[1] < self.MIN_Y) | (space[1] > self.MAX_Y):
                return 1
            if space in self.occupiedspaces:
                return 2
        return 0

class Player():
    def __init__(self):
        self.board = Board()
    
    def sendConfirmation(self):
        pass

    def getConfirmation(self):
        pass
    
    def getMove(self):
        pass

class LocalPlayer(Player):
    def __init__(self):
        super().__init__()

class RemotePlayer(Player):
    def __init__(self):
        super().__init__()

    # send confirmation to remote player that local player has finished setting up their pieces
    def sendConfirmation(self):
        pass

    # wait for confirmation that other player is ready
    def getConfirmation(self):
        pass

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()
    
    # send confirmation to computer that local player has finished setting up their pieces
    # this function does nothing in this case
    def sendConfirmation(self):
        pass
    
    # wait for confirmation that other player is ready
    # in this case, computer sets up its board and signals that it's ready
    def getConfirmation(self):
        b = self.board
        shipsToPlace = [(5, "Carrier"), (4, "Battleship"), (3, "Destroyer"), (3, "Submarine"), (2, "Patrol Boat")]
        while len(shipsToPlace) > 0:
            nextShipInfo = shipsToPlace[0]
            shipsToPlace.pop(0)
            valid = -1
            while valid != 0:
                pos = (random.randint(b.MIN_X, b.MIN_X), random.randint(b.MIN_X, b.MAX_Y))
                direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
                nextShip = Ship(pos, nextShipInfo[0], direction, nextShipInfo[1])
                valid = b.isShipValid(nextShip)
            b.addShip(nextShip)
        
        return True
        