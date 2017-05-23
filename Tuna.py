#=======================================================================
#                        General Documentation

""" Allows the creation and manipulation of a Tuna object.
"""

#-----------------------------------------------------------------------
#                       Additional Documentation
# Modification History:
# - 18 May 2017:  Original by Arthur (Ky-Phuoc) Khuu
#
# Notes:
# - Written for Python 3
# - See import statements throughout for more information on non-
#   built-in packages and modules required.
#
#=======================================================================

import numpy as np

class Tuna:
    weightGain = 0.0274
    sizeGain = 0.9906
    
    def __init__(self, xLoc, yLoc, weight=0.0767, size=2.794, sightRadius=1, energy=0.5, state="Alive"):
        """Constructor that makes a Tuna object.

        xLoc: gives the x-coordinate
        yLoc: gives the y-coordinate
        weight: gives the weight
        size: gives the size
        sightRadius: gives the amount of squares the Tuna can see
        energy: gives the energy level of Tuna, based off of food eaten

        """
        self.x = xLoc
        self.y = yLoc
        self.weight = weight
        self.size = size
        self.sightRadius = sightRadius 
        self.energy = energy
        self.state = state

    def stateInt(self):
        if self.state = "Alive":
            return 1
        elif self.state = "DeadStarved":
            return 2
        elif self.state = "DeadEaten":
            return 3
        else:
            raise ValueError
            
        
    def move(self, xMax, yMax):
        """Moves the Tuna object

        xMax: grid x boundary
        yMax: grid y boundary

        """
        # Make Tuna move a square
        move = [-1, 1]
        
        np.random.shuffle(move)
        self.xLoc += move[0]
        
        np.random.shuffle(move)
        self.yLoc += move[0]
        
        # Check for x boundaries
        if self.xLoc < 0:
            self.xLoc = 0
        if self.xLoc > xMax:
            self.xLoc = xMax
            
        # Check for y boundaries
        if self.yLoc < 0:
            self.yLoc = 0
        if self.yLoc > yMax:
            self.yLoc = yMax

    def eat(self, amount):
        """Tuna eats food and gains amount proportional to weight

        amount: value of food eaten

        """
        # Make Tuna energy gain proportional to weight
        self.energy += (amount / self.weight)
        
        if self.energy > 1.0:
            self.energy = 1.0
            
    def update(self):
        """Updates the weight and size of the Tuna.
        """
        # If under 0.2 energy, Tuna is starving and does not grow
        if self.energy > 0.2:
            self.weight += (weightGain * (1 + (self.energy - 0.2)))
            self.size += (sizeGain * (1 + (self.energy - 0.2)))




