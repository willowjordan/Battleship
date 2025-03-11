class Ship():
    # name:str - name/id of ship
    # pos:(int, int) - position of the origin of the ship
    # l:int - length
    # d:(int, int) - direction the ship is pointing in; can be (1, 0), (0, 1), (-1, 0), or (0, -1)
    def __init__(self, name, pos, l, d):
        self.name = name
        self.pos = pos
        self.length = l
        self.direction = d
        self.spaces = [] # all spaces the ship occupies
        for i in range(0, l):
            self.spaces.append((pos[0] + d[0]*i, pos[1] + d[1]*i))
    
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