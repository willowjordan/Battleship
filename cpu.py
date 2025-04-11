# This file contains the algorithms that CPU players will use.

import time
import random
import copy

from board import *

class Mode(Enum):
    """
    Mode that the CPU is in (determines targeting behavior).\n
    RANDOM - Making random (or semi-random) guesses.\n
    SINGLESHIP - CPU has located a single ship and is attempting to sink it.\n
    SHIPGROUP - CPU has located a group of connected ships and will find every ship connected with the group.
    """
    RANDOM = 0
    SINGLESHIP = 1
    SHIPGROUP = 2

class CPU():
    def __init__(self, slow:bool):
        self.slow = slow
        self.lastmove = None
        self.lastresult = None
    
    def setBoard(self, board:Board):
        self.board = board

    def setup(self): raise NotImplementedError()
    def getMove(self): raise NotImplementedError()

class RandomCPU(CPU):
    """
    A CPU that makes all of its moves randomly.
    Setup: Randomly places ships.
    Moves: Makes completely random moves. Only has access to RANDOM mode.
    """
    def setup(self):
        if self.slow: time.sleep(random.uniform(1.5, 4.5)) # add random time delay to make player think computer is running some super fancy algorithm
        shipsToPlace = [(5, "Carrier"), (4, "Battleship"), (3, "Destroyer"), (3, "Submarine"), (2, "Patrol Boat")]
        while len(shipsToPlace) > 0:
            nextShipInfo = shipsToPlace[0]
            shipsToPlace.pop(0)
            valid = -1
            while valid != 0:
                pos = (random.randint(self.board.MIN_X, self.board.MAX_X), random.randint(self.board.MIN_Y, self.board.MAX_Y))
                direction = random.choice(Ship.POSSIBLE_DIRECTIONS)
                nextShip = Ship(pos, nextShipInfo[0], direction, nextShipInfo[1])
                valid = self.board.isShipValid(nextShip)
            self.board.addShip(nextShip)
    
    def getMove(self):
        if self.slow: time.sleep(random.uniform(0.5, 1.5))
        valid = False
        while not valid:
            move = (random.randint(self.board.MIN_X, self.board.MAX_X), random.randint(self.board.MIN_Y, self.board.MAX_Y))
            if move not in self.board.myshots:
                valid = True
        return move
    
class IntermediateCPU(CPU):
    """
    Smarter than Random CPU.
    Setup: Tries to place ships with at least one square of space between them.
    Moves: Only has access to RANDOM and SHIPGROUP modes.
    """
    def __init__(self, slow:bool):
        super().__init__(slow)
        self.targetingMode = Mode.RANDOM
        self.shipGroup = [] # all confirmed spaces of the current ship group being fired upon
        self.shipGroupBorders = [] # spaces bordering the shipGroup squares that have not been fired upon yet

    def setup(self):
        if self.slow: time.sleep(random.uniform(1.5, 4.5))
        shipsToPlace = [(5, "Carrier"), (4, "Battleship"), (3, "Destroyer"), (3, "Submarine"), (2, "Patrol Boat")]
        while len(shipsToPlace) > 0:
            nextShipInfo = shipsToPlace[0]
            shipsToPlace.pop(0)
            valid = -1
            while valid != 0:
                pos = (random.randint(self.board.MIN_X, self.board.MAX_X), random.randint(self.board.MIN_Y, self.board.MAX_Y))
                direction = random.choice(Ship.POSSIBLE_DIRECTIONS)
                length = nextShipInfo[0]
                nextShip = Ship(pos, length, direction, nextShipInfo[1])
                valid = self.board.isShipValid(nextShip)
                # check squares around ship
                spaces = nextShip.spaces
                squaresAround = []
                for x in range(spaces[0][0]-1, spaces[length-1][0]+1):
                    for y in range(spaces[0][1]-1, spaces[length-1][1]+1):
                        if (x, y) in spaces: continue
                        if (x < self.board.MIN_X) | (x > self.board.MAX_X): continue
                        if (y < self.board.MIN_Y) | (y > self.board.MAX_Y): continue
                        squaresAround.append((x, y))
                for sq in squaresAround:
                    if sq in self.board.occupiedspaces:
                        valid = 1
            self.board.addShip(nextShip)
    
    def getMove(self):
        moveToReturn = None
        if self.slow: time.sleep(random.uniform(0.5, 1.5))
        if self.targetingMode == Mode.RANDOM:
            # If last move was a hit, switch modes.
            if self.lastresult == Result.HIT:
                self.targetingMode = Mode.SHIPGROUP
                self.shipGroupCenter = self.lastmove # space to build the ship group around
                moveToReturn = self.shipGroupMove()
            else:
                # Otherwise, return a random move
                moveToReturn = self.randomMove()
        else: # in SHIPGROUP mode
            moveToReturn = self.shipGroupMove()
            if moveToReturn is None:
                self.targetingMode = Mode.RANDOM
                self.shipGroupCenter = None
                moveToReturn = self.randomMove()
        
        self.lastmove = moveToReturn
        return moveToReturn
        
    def randomMove(self):
        """Return a random valid move."""
        valid = False
        while not valid:
            move = (random.randint(self.board.MIN_X, self.board.MAX_X), random.randint(self.board.MIN_Y, self.board.MAX_Y))
            if move not in self.board.myshots:
                valid = True
        return move
    
    def shipGroupMove(self):
        """Explore from ship group center until an unfired space has been found. Return that space. If the ship group is complete, return None."""
        spacesToExplore = [self.shipGroupCenter] # this will function as a queue
        exploredSpaces = []
        while len(spacesToExplore) > 0:
            nextSpace = spacesToExplore.pop(0)
            exploredSpaces.append(nextSpace)
            if nextSpace in self.board.myshots:
                if self.board.myshots[nextSpace] != Result.MISS:
                    # queue all unexplored neighboring spaces
                    neighbors = self.board.getNeighbors(nextSpace)
                    for nb in neighbors:
                        if (nb not in spacesToExplore) & (nb not in exploredSpaces):
                            spacesToExplore.append(nb)
            else:
                # this space hasn't been fired on yet
                return nextSpace
        
        # if all spaces have been explored
        return None

    '''def setShipGroup(self):
        """
        Automatically determine the ship group and set variables accordingly.
        This function should only be called when the last move was a hit.
        """
        self.targetingMode = Mode.SHIPGROUP
        self.shipGroup = []
        self.shipGroupBorders = []
        spacesToExplore = [self.lastmove] # this will function as a queue
        exploredSpaces = []
        while len(spacesToExplore) > 0:
            nextSpace = spacesToExplore.pop(0)
            exploredSpaces.append(nextSpace)
            if nextSpace in self.board.myshots:
                if self.board.myshots[nextSpace] == Result.HIT:
                    # add to ship group and queue all unexplored neighboring spaces
                    self.shipGroup.append(nextSpace)
                    neighbors = self.board.getNeighbors(nextSpace)
                    for nb in neighbors:
                        if (nb not in spacesToExplore) & (nb not in exploredSpaces):
                            spacesToExplore.append(nb)
            else:
                # this space hasn't been fired on, so add it to the borders of the ship group to be explored
                self.shipGroupBorders.append(nextSpace)'''

class AdvancedCPU(CPU):
    """
    Smarter than Intermediate
    Setup: TBD
    Moves: Has access to all modes. RANDOM mode is semi-random and attempts to maximize board coverage.
    """
    def setup(self):
        raise NotImplementedError()
    
    def getMove(self):
        raise NotImplementedError()
    
    def randomMove(self):
        pass
    
    def singleShipMove(self):
        """Return a move with the goal of sinking a single identified ship."""
        if self.lastresult == Result.SUNK: # sunk the ship, so leave targeting mode and start making random guesses
            self.targetingMode = Mode.RANDOM
            self.targetingDirection = None
        else:
            d = self.targetingDirection
            nextMove = (self.lastmove[0] + d[0], self.lastmove[1] + d[1])
            if (nextMove in self.board.myshots) | (self.lastresult == Result.MISS): # went off the edge, so come back the other direction
                d = self.targetingDirection = (-d[0], -d[1]) # update both attribute and abbreviated copy
                nextMove = (self.lastmove[0] + d[0], self.lastmove[1] + d[1])
                while nextMove not in self.board.myshots:
                    if self.board.myshots[nextMove] != Result.HIT: # went off the edge in both directions, so AI is being fooled by multiple ships right next to each other
                        # change mode and make shipgroup move instead
                        self.setShipGroup()
                        return self.shipGroupMove()
                    nextMove = (nextMove[0] + d[0], nextMove[1] + d[1])
            # regardless of if condition is true, we now have the correct value of nextMove
            return nextMove