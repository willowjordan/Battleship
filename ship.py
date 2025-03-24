class Ship():
    POSSIBLE_DIRECTIONS = (1, 0), (0, 1), (-1, 0), (0, -1)

    def __init__(self, pos:tuple, l:int, d:tuple, name:str=""):
        """
        :param pos: tuple(int, int) for the position of the origin of the ship
        :param l: int for length
        :param d: tuple(int, int) for direction the ship is pointing in; can be (1, 0), (0, 1), (-1, 0), or (0, -1)
        :param name: name/id of the ship
        """
        if d not in Ship.POSSIBLE_DIRECTIONS: raise(ValueError, "Bad direction value")
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