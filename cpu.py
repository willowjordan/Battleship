# This file contains the algorithms that CPU players will use.

import time
import random

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
    def makeMove(self): raise NotImplementedError()

class RandomCPU(CPU):
    """A CPU that makes all of its moves randomly."""
    def setup(self):
        if self.slow: time.sleep(random.uniform(1.5, 4.5)) # add random time delay to make player think computer is running some super fancy algorithm
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
    
    def makeMove(self):
        if self.slow: time.sleep(random.uniform(0.5, 1.5))
        b = self.board
        valid = False
        while not valid:
            move = (random.randint(b.MIN_X, b.MAX_X), random.randint(b.MIN_Y, b.MAX_Y))
            if move not in b.myshots:
                valid = True
        return move
    
class IntermediateCPU(CPU):
    """
    Smarter than Random CPU
    Setup: Tries to place ships with at least one square of space between them
    Moves: Makes random moves until it hits a ship, then tries adjacent squares until it sinks a ship
    """
    def __init__(self):
        super.__init__()
        self.targinfo = {
            "mode": Mode.RANDOM,
            "direction": None, # what direction to move in when firing shots
            "shipGroup": [],
            "shipGroupBorders": [],
        }

    def setup(self):
        if self.slow: time.sleep(random.uniform(1.5, 4.5))
        b = self.board
        shipsToPlace = [(5, "Carrier"), (4, "Battleship"), (3, "Destroyer"), (3, "Submarine"), (2, "Patrol Boat")]
        while len(shipsToPlace) > 0:
            nextShipInfo = shipsToPlace[0]
            shipsToPlace.pop(0)
            valid = -1
            while valid != 0:
                pos = (random.randint(b.MIN_X, b.MAX_X), random.randint(b.MIN_Y, b.MAX_Y))
                direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
                length = nextShipInfo[0]
                nextShip = Ship(pos, length, direction, nextShipInfo[1])
                valid = b.isShipValid(nextShip)
                # check squares around ship
                spaces = nextShip.spaces
                squaresAround = []
                for x in range(spaces[0][0]-1, spaces[length][0]+1):
                    for y in range(spaces[0][1]-1, spaces[length][1]+1):
                        if (x, y) in spaces: continue
                        if (x < b.MIN_X) | (x > b.MAX_X): continue
                        if (y < b.MIN_Y) | (y > b.MAX_Y): continue
                        squaresAround.append((x, y))
                for sq in squaresAround:
                    if sq in b.occupiedspaces:
                        valid = 1
            b.addShip(nextShip)
    
    #NOTE: I might end up moving this to Advanced, my logic so far seems a little too sophisticated for Intermediate
    def makeMove(self):
        if self.slow: time.sleep(random.uniform(0.5, 1.5))
        b = self.board

        if self.targinfo["mode"] == Mode.SINGLESHIP:
            if self.lastresult == Result.SUNK: # sunk the ship, so leave targeting mode and start making random guesses
                self.targinfo["mode"] = Mode.RANDOM
                self.targinfo["direction"] = None
            else:
                d = self.targinfo["direction"]
                nextMove = (self.lastmove[0] + d[0], self.lastmove[1] + d[1])
                if (nextMove in self.board.myshots) | (self.lastresult == Result.MISS): # went off the edge, so come back the other direction
                    d = self.targinfo["direction"] = (-d[0], -d[1]) # update both attribute and abbreviated copy
                    nextMove = (self.lastmove[0] + d[0], self.lastmove[1] + d[1])
                    while nextMove not in self.board.myshots:
                        if self.board.myshots[nextMove] != Result.HIT: # went off the edge in both directions, so AI is being fooled by multiple ships right next to each other
                            # TODO: do something here
                            break
                        nextMove = (nextMove[0] + d[0], nextMove[1] + d[1])
                # regardless of if condition is true, we now have the correct value of nextMove
                return nextMove
        if self.targinfo["mode"] == Mode.SHIPGROUP:
            # first check if we have sunk the whole group
            
            pass
        # random mode
        valid = False
        while not valid:
            move = (random.randint(b.MIN_X, b.MAX_X), random.randint(b.MIN_Y, b.MAX_Y))
            if move not in b.myshots:
                valid = True
        return move

class AdvancedCPU(CPU):
    """Smarter than Intermediate"""
    def setup(self):
        raise NotImplementedError()
    
    def makeMove(self):
        raise NotImplementedError()