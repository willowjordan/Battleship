# This file contains the algorithms that CPU players will use.

import time
import random

from board import *

class CPU():
    def __init__(self, slow:bool):
        self.slow = slow
    
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
        if self.slow: time.sleep(random.uniform(0.5, 1.5)) # add random time delay to make player think computer is running some super fancy algorithm
        b = self.board
        valid = False
        while not valid:
            move = (random.randint(b.MIN_X, b.MAX_X), random.randint(b.MIN_Y, b.MAX_Y))
            if move not in b.myshots:
                valid = True
        return move
    
class IntermediateCPU(CPU):
    """Smarter than Random"""
    def setup(self):
        raise NotImplementedError()
    
    def makeMove(self):
        raise NotImplementedError()

class AdvancedCPU(CPU):
    """Smarter than Intermediate"""
    def setup(self):
        raise NotImplementedError()
    
    def makeMove(self):
        raise NotImplementedError()