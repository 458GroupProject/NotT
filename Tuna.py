#=======================================================================
#                        General Documentation

""" Allows the creation and manipulation of a Tuna object.
"""

#-----------------------------------------------------------------------
#                       Additional Documentation
# Modification History:
# - 18 May 2017:  Original by Arthur (Ky-Phuoc) Khuu
# - 22 May 2017: Tien Huynh
#                Removed weight attribute, added length
#                Changed eat() and update() methods
# Notes:
# - Written for Python 3
# - See import statements throughout for more information on non-
#   built-in packages and modules required.
#
#=======================================================================

#-----------------------Constant variables------------------------------
MAX_ENERGY = 1.0
MIN_ENERGY = 0.0
STARVED_THRES = 0.2
INIT_LENGTH = 3.0
INIT_ENERGY = 0.5
PLANKTON_ONLY_SIZE = 6.0
PLANKTON_ENERGY_MULTIPLIER = 0.5
FISH_ENERGY_MULTIPLIER = 1.0
GROWTH_MULTIPLIER = 0.5


import numpy as np
from Consts import*

class Tuna:
    
    def __init__(self, xLoc, yLoc, length = INIT_LENGTH, sightRadius=1, energy=INIT_ENERGY, state="Alive"):
        """Constructor that makes a Tuna object.

        xLoc: gives the x-coordinate also known as Column
        yLoc: gives the y-coordinate also known as Row
        weight: gives the weight
        size: gives the size
        sightRadius: gives the amount of squares the Tuna can see
        energy: gives the energy level of Tuna, based off of food eaten

        """
        self.x = xLoc
        self.y = yLoc
        self.length = length
        self.sightRadius = sightRadius 
        self.energy = energy
        self.state = state

    def stateInt(self):
        if self.state == "Alive":
            return 1
        elif self.state == "Starving":
            return 2
        elif self.state == "DeadStarved":
            return 3
        elif self.state == "DeadEaten":
            return 4
        else:
            raise ValueError
            
        
    def move(self, grid):
        """Moves the Tuna object

        xMax: grid x boundary
        yMax: grid y boundary
            
            Random moving for now
        """
        xMax=np.shape(grid)[1]-1  #max rows
        yMax=np.shape(grid)[0]-1  #max cols
        
        grid[self.y,self.x].tuna=False
        
        # Make Tuna move a square
        move = [-1,0,1]
        
        np.random.shuffle(move)
        self.x += move[0]
        
        np.random.shuffle(move)
        self.y += move[0]
        
        # Check for x boundaries
        if self.x < 0:
            self.x = 0
        if self.x > xMax:
            self.x = xMax
            
        # Check for y boundaries
        if self.y < 0:
            self.y = 0
        if self.y > yMax:
            self.y = yMax
    
        grid[self.y,self.x].tuna=True        
        
    def eat(self, grid):
        """Tuna eats food and gains amount proportional to weight

        grid: the enviroment grid that holds the population

        """
        # Make Tuna energy gain proportional to weight
        amtPlanktonEat = 0.0
        amtFishEat = 0.0
        #only eat if energy is not maxed
        if self.energy < MAX_ENERGY:
            #Case of small larvae that can only eat plankton
            if self.length < PLANKTON_ONLY_SIZE:
                #check the maximum food it can eat from the cell
                amtPlanktonEat = min((MAX_ENERGY - self.energy) / PLANKTON_ENERGY_MULTIPLIER * self.length, grid[self.x, self.y].foodPlankton)
                #update energy value of the tuna
                self.energy += amtPlanktonEat * PLANKTON_ENERGY_MULTIPLIER / self.length
                #update food value of the water cell
                grid[self.x, self.y].updateFood(-amtPlanktonEat, -amtFishEat)
            #Case of large larvae that can eat both plankton and fish-based
            else:
                #priority fish-based food
                amtFishEat = min((MAX_ENERGY - self.energy) / FISH_ENERGY_MULTIPLIER * self.length, grid[self.x, self.y].foodFish)  
                self.energy += amtFishEat * FISH_ENERGY_MULTIPLIER / self.length
                #if tuna's energy is still not maxed out after eating fish-based food, eat plankton also
                if self.energy < MAX_ENERGY:
                    amtPlanktonEat = min((MAX_ENERGY - self.energy) / PLANKTON_ENERGY_MULTIPLIER * self.length, grid[self.x, self.y].foodPlankton) 
                    self.energy += amtPlanktonEat * PLANKTON_ENERGY_MULTIPLIER / self.length
                grid[self.x, self.y].updateFood(-amtPlanktonEat, -amtFishEat)           
            
            
    def update(self, grid):
        """Updates the weight and size of the Tuna.
        """
        global STARVE
        if self.energy<STARVE:
            return False
        else:
            return True

    def grow(self):
        # If under STARVED_THRES, Tuna is starving and does not grow
        if self.energy > STARVED_THRES:
            self.length *= (1 + ((self.energy - STARVED_THRES) * GROWTH_MULTIPLIER))

