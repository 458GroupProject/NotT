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
# - 23 May 2017: Tien Huynh
#                Changed move() to randomeMove() and implemented
#   23 May 2017 5:30-6:30 PM
#   updated & tested RandomMove, adding useEnergy
# Notes:
# - Written for Python 3
# - See import statements throughout for more information on non-
#   built-in packages and modules required.
#
#=======================================================================

#-----------------------Constant variables------------------------------
MAX_ENERGY = 1.0
MIN_ENERGY = 0.0
STARVE=0.1
STARVED_THRES = 0.2
INIT_LENGTH = 3.0
INIT_ENERGY = 0.5
PLANKTON_ONLY_SIZE = 6.0
PLANKTON_ENERGY_MULTIPLIER = 0.5
FISH_ENERGY_MULTIPLIER = 1.0
GROWTH_MULTIPLIER = 0.5
ENERGY_SWIMMING=.1


import numpy as np

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
        elif self.state == "DeadStarved":
            return 2
        elif self.state == "DeadEaten":
            return 3
        else:
            raise ValueError
            
    def move(self, movegrid):
        self.randomMove(movegrid)
        
    def randomMove(self, okayMoveGrid):
        """Randomly move the tuna to a neighboring cell if available
        Only one tuna is allowed on each cell

        + okayMoveGrid: the boolean grid that specifies which cell is okay to move
                        to (0 = unoccupied cell; 1 = boundary cell; 2 = tuna occupied cell)
                        Obtained by calling okayMoveGrid(baseGrid) in Driver.py

        """

        x = self.x
        y = self.y
        newX = 0   #the next potential x-coordinate
        newY = 0   #the next potential y-coordinate
        successMove = False    #flag to mark a successful move
        

        #check if there is any empty neighboring cell
        if 0 in okayMoveGrid[(y-1):(y+2), (x-1):(x+2)]:
            #randomly generate a move until found an empty neighboring cell
            while (successMove == False):
                newX = self.x + np.random.randint(-1, high=2)
                newY = self.y + np.random.randint(-1, high=2)
                if okayMoveGrid[newY, newX] == 0:
                    successMove = True
                    #update the okayMoveGrid of this new move
                    okayMoveGrid[y,x] = 0
                    okayMoveGrid[newY,newX] = 2
                    self.x = newX
                    self.y = newY


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
                amtPlanktonEat = min((MAX_ENERGY - self.energy) / PLANKTON_ENERGY_MULTIPLIER * self.length, grid[self.y, self.x].foodPlankton)
                #update energy value of the tuna
                self.energy += amtPlanktonEat * PLANKTON_ENERGY_MULTIPLIER / self.length
                #update food value of the water cell
                grid[self.y, self.x].updateFood(-amtPlanktonEat, -amtFishEat)
            #Case of large larvae that can eat both plankton and fish-based
            else:
                #priority fish-based food
                amtFishEat = min((MAX_ENERGY - self.energy) / FISH_ENERGY_MULTIPLIER * self.length, grid[self.y, self.x].foodFish)  
                self.energy += amtFishEat * FISH_ENERGY_MULTIPLIER / self.length
                #if tuna's energy is still not maxed out after eating fish-based food, eat plankton also
                if self.energy < MAX_ENERGY:
                    amtPlanktonEat = min((MAX_ENERGY - self.energy) / PLANKTON_ENERGY_MULTIPLIER * self.length, grid[self.y, self.x].foodPlankton) 
                    self.energy += amtPlanktonEat * PLANKTON_ENERGY_MULTIPLIER / self.length
                grid[self.y, self.x].updateFood(-amtPlanktonEat, -amtFishEat)           
            
            
    def update(self, grid):
        """Updates the weight and size of the Tuna.
        """
        self.useEnergy()
        
        if self.energy<STARVE:
            return False
        else:
            return True

    def useEnergy(self):
        self.energy-=ENERGY_SWIMMING
    
    def grow(self,grid):
        # If under STARVED_THRES, Tuna is starving and does not grow
        if self.energy > STARVED_THRES:
            self.length *= (1 + ((self.energy - STARVED_THRES) * GROWTH_MULTIPLIER))

