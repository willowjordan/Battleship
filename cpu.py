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
        b = self.board
        shipsToPlace = [(5, "Carrier"), (4, "Battleship"), (3, "Destroyer"), (3, "Submarine"), (2, "Patrol Boat")]
        while len(shipsToPlace) > 0:
            nextShipInfo = shipsToPlace[0]
            shipsToPlace.pop(0)
            valid = -1
            while valid != 0:
                pos = (random.randint(b.MIN_X, b.MAX_X), random.randint(b.MIN_Y, b.MAX_Y))
                direction = random.choice(Ship.POSSIBLE_DIRECTIONS)
                nextShip = Ship(pos, nextShipInfo[0], direction, nextShipInfo[1])
                valid = b.isShipValid(nextShip)
            b.addShip(nextShip)
    
    def getMove(self):
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
    Smarter than Random CPU.
    Setup: Tries to place ships with at least one square of space between them.
    Moves: Only has access to RANDOM and SHIPGROUP modes.
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
                direction = random.choice(Ship.POSSIBLE_DIRECTIONS)
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
    
    def getMove(self):
        if self.slow: time.sleep(random.uniform(0.5, 1.5))
        if self.targinfo["mode"] == Mode.RANDOM: return self.randomMove()
        else: return self.shipGroupMove()
        
    def randomMove(self):
        """Return a random valid move. If last move was a hit, switch modes."""
        b = self.board

        if self.lastresult == Result.HIT:
            self.setShipGroup()
            return self.shipGroupMove()

        valid = False
        while not valid:
            move = (random.randint(b.MIN_X, b.MAX_X), random.randint(b.MIN_Y, b.MAX_Y))
            if move not in b.myshots:
                valid = True
        return move
    
    def shipGroupMove(self):
        """Make a move with the goal of sinking an entire group of connected ships. If ship group has been completely discovered, switch modes."""
        

    def setShipGroup(self):
        """
        Automatically determine the ship group and set variables accordingly.
        This funciton should only be called when the last move was a hit.
        """
        b = self.board
        self.targinfo["mode"] = Mode.SHIPGROUP
        group = [self.lastmove]
        while True: # continue exploring until all neighbors have been discovered
            newgroup = copy.deepcopy(group)
            neighbors = []
            for pos in group:
                neighbors.append(b.getNeighbors(pos))
            neighbors = list(set(neighbors)) # remove duplicates using set
            for nb in neighbors:
                if nb in b.myshots:
                    if b.myshots[nb] == Result.MISS:
                        neighbors.remove(nb)
                    else:
                        newgroup.append(nb)
            
            # loop condition
            if group == newgroup:
                self.targinfo["shipGroup"] = group
                self.targinfo["shipGroupBorders"] = neighbors
                break
            else:
                group = newgroup

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
                        # change mode and make shipgroup move instead
                        self.setShipGroup()
                        return self.shipGroupMove()
                    nextMove = (nextMove[0] + d[0], nextMove[1] + d[1])
            # regardless of if condition is true, we now have the correct value of nextMove
            return nextMove