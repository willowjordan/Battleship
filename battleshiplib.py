class Space():
    def __init__(self, occupied=False, shot=0):
        self.occupied = occupied # True if occupied by a ship (this will only be true for primary grid)
        self.shot = shot # 0 if not shot yet, -1 if miss, 1 if hit

class Board():
    def __init__(self, ships=None):
        self.primaryGrid = {}
        self.targetingGrid = {}

        if ships is not None:
            for s in ships:
                pass # populate primary grid
    
    def fireShot(self, other, pos):
        pass

class Player():
    def __init__(self):
        self.board = Board()

class LocalPlayer(Player):
    def __init__(self):
        super().__init__()

class RemotePlayer(Player):
    def __init__(self):
        super().__init__()

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()