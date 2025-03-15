class Ship():
    # pos:[int, int] - position of the origin of the ship
    # l:int - length
    # d:[int, int] - direction the ship is pointing in; can be [1, 0], [0, 1], [-1, 0], or [0, -1]
    # name:str - name/id of ship
    def __init__(self, pos:list[int, int], l:int, d:list[int, int], name:str=""):
        self.name = name
        self.pos = pos
        self.length = l
        self.direction = d
        self.generateSpaces()
    
    def generateSpaces(self):
        self.spaces = [] # all spaces the ship occupies
        for i in range(0, self.length):
            self.spaces.append([self.pos[0] + self.direction[0]*i, self.pos[1] + self.direction[1]*i])
        self.spaces.sort()

    # translate the ship based on translation vector
    def translate(self, transVector:list[int, int]):
        self.pos[0] += transVector[0]
        self.pos[1] += transVector[1]

        for space in self.spaces:
            space[0] += transVector[0]
            space[1] += transVector[1]
        self.spaces.sort()
    
    # rotate the ship clockwise one time
    def rotateClockwise(self):
        # change direction var
        temp = self.direction[1]
        self.direction[1] = self.direction[0]
        if self.direction[1] == 0:
            self.direction[0] = -temp
        else: self.direction[0] = 0

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

class Player():
    def __init__(self):
        self.board = Board()
    
    def getMove(self):
        pass

class LocalPlayer(Player):
    def __init__(self):
        super().__init__()

class RemotePlayer(Player):
    def __init__(self):
        super().__init__()

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()