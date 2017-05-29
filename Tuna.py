# -*- coding: utf-8 -*-
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


# Jeremy 24 May 7:30 PM
# Adding new submethods for the tuna move
# hunt, forage, schoolingBehavior
# Will need to change implementation of "eat" method
# Added variable flags alreadyAte
# jgn 5.25 added forage and hunt method implementation and VISION
# Notes:
# - Written for Python 3
# - See import statements throughout for more information on non-
#   built-in packages and modules required.
#





"""
Jeremy 5/24/2017
"Schooling was first observed at 25–27 days after hatching (26· 2–33· 8 mm, 
total length) in the Pacific bluefin tuna Thunnus orientalis. At this time, 
the mode of swimming changed from intermittent sprinting to continuous 
cruising, and this allowed the fish to adjust to an inertial hydrodynamic 
environment."
-http://onlinelibrary.wiley.com/doi/10.1111/j.1095-8649.2010.02598.x/full
"""
#=======================================================================

#-----------------------Constant variables------------------------------
MAX_ENERGY = 1.0
MIN_ENERGY = 0.0
HUNGRY=1.0 #not working yet
STARVE=0.0
STARVED_THRES = 0.2    #increased, as tuna grew too fast and starved
INIT_LENGTH = 3.0       #use mm as base length unit
INIT_ENERGY = 0.5
GROWTH_MULTIPLIER_BELOW_7MM = 0.055
GROWTH_MULTIPLIER_ABOVE_7MM = 0.128

ENERGY_SWIMMING = 0.05   #energy spent for regular swim
ENERGY_HUNTING = 0.1     #energy spent for hunting
SCHOOLING_SIZE = 28
VISION=2 #cells moore neghborhood
AGGRESSION=.20 #liklihood to attack another tuna
TEMP_LOW = 22 #lower temperature threshold for appropriate tuna life
TEMP_HIGH = 28 #higher temperature threshold for appropriate tuna life
TEMP_MULTIPLIER = 0.1 #temperature growth rate multiplier 



import numpy as np
from Consts import *

class Tuna:
    # jgn 5.25 added random factor to tuna init length for more variability of size
    def __init__(self, xLoc, yLoc, length = INIT_LENGTH+np.random.uniform(-0.5,0.5), sightRadius=1, energy=INIT_ENERGY, state="Alive"):
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
        
        #If the tuna ate during hunting phase, skip eating plankton
        self.alreadyAte=False
        
        #unfortunately it's the end of the line for this little fishy, it's been
        #eaten :(
        self.eaten=False
        
        #Flag for when tuna is large enough to follow schooling behavior
        self.isSchooling=False

    def stateInt(self):
        if self.state == "Alive":
            return 1
        elif self.state == "DeadStarved":
            return 2
        elif self.state == "DeadEaten":
            return 3
        else:
            raise ValueError
     
    """
    This is the main move method which will be called from the driver, depending
    on the tuna's state it will then call other methods:
    If isHungry (energy level below some constant) then it will search for food
    If not hungry it will do the next default move which is schooling behavior
    (we can implement this last as it only effects relatively large tuna (25 days old))
    for now just have it call random move
    
    Finally if it's not hungry and not large enough to follow schooling behavior
    do the default random move
    """       
    def move(self, movegrid, grid):
        
        if self.energy<HUNGRY:
            self.lookForFood(movegrid, grid)
        
        elif self.length>SCHOOLING_SIZE:
            self.randomMove(movegrid)
        
        else:
            self.randomMove(movegrid)
     
    """
    If the tuna is hungry (which will probably be all the time) this method
    will be called from the move method.
    
    If large enough it will call the hunt method, otherwise the forage method,
    which is basically just move to the nearest cell with the highest plankton
    count (including it's current cell)
    """   
    def lookForFood(self,moveGrid, grid):
        r=np.random.uniform()
        if self.length>PLANKTON_ONLY_SIZE and AGGRESSION>r: 
            self.hunt(moveGrid,grid)
        else:
            self.forage(moveGrid,grid)
    
    """
    Out of all cells in the Moore neighborhood including it's current cell
    find the empty cell with the highest plankton count and go there
    """
    def forage(self, moveGrid, grid):
        """Randomly move the tuna to a neighboring cell if available that has
        the most plankton
        Only one tuna is allowed on each cell

        + okayMoveGrid: the boolean grid that specifies which cell is okay to move
                        to (0 = unoccupied cell; 1 = boundary cell; 2 = tuna occupied cell)
                        Obtained by calling okayMoveGrid(baseGrid) in Driver.py

        """
        global tankh, tankw
        x = self.x
        y = self.y
        newX = x   #the next potential x-coordinate
        newY = y   #the next potential y-coordinate
        
        #available squares
        possible=[]
        mostFood=0
        
        #current grid is an option
        moveGrid[x,y]=0
        
        for yy in [-1,0,1]:
            for xx in [-1,0,1]:
                if not (y+yy<0 or y+yy>tankh or x+xx<0 or x+xx>tankw):
                    if moveGrid[y+yy,x+xx]==0 and grid[y+yy,x+xx].foodPlankton>mostFood:
                        newX=x+xx
                        newY=y+yy
                        mostFood=grid[y+yy,x+xx].foodPlankton+ np.random.uniform(-.01,.01) 
        self.x=newX
        self.y=newY
        self.energy -= ENERGY_SWIMMING
        if mostFood==0:
            self.randomMove(moveGrid)
    """
    Search all cells within sightRadius for a suitable prey target. If one is
    identified (pick the largest suitable one) Move to that square and remove
    the prey item, marking it as cannibalized if it was another tuna, update
    the energy levels of the predator accordingly and mark it as alreadyAte
    """
    
    def hunt(self, movegrid, grid):
        """Randomly move the tuna to a neighboring cell if available that has
        the most plankton
        Only one tuna is allowed on each cell

        + okayMoveGrid: the boolean grid that specifies which cell is okay to move
                        to (0 = unoccupied cell; 1 = boundary cell; 2 = tuna occupied cell)
                        Obtained by calling okayMoveGrid(baseGrid) in Driver.py

        Tien 05/28/2017: added cannibalism success rate

        """
        
        global VISIBILITY, tankh, tankw
        x = self.x
        y = self.y
        newX = 0   #the next potential x-coordinate
        newY = 0   #the next potential y-coordinate
        
        
        for yy in np.arange(VISION+1):
            for xx in np.arange(VISION-VISIBILITY+1):
                if not (y+yy<0 or y+yy>tankh or x+xx<0 or x+xx>tankw):
                    if not (grid[y+yy,x+xx]).resident==0:
                        if (grid[y+yy,x+xx]).resident.length<self.length:
                            #chance of successful cannibalism is based on size difference between hunter & huntee
                            cannibalSuccess = (self.length / grid[y+yy,x+xx].resident.length) - 1
                            if np.random.uniform() > cannibalSuccess:
                                print "CANNIBAL!"
                                newX=x+xx
                                newY=y+yy
                                self.energy -= ENERGY_HUNTING
                                
                                grid[newY,newX].resident.eaten=True
                                amtFishEat = min((MAX_ENERGY - self.energy) / FISH_ENERGY_MULTIPLIER * self.length, grid[newY, newX].resident.length)  
                                self.energy += amtFishEat * FISH_ENERGY_MULTIPLIER / self.length
                                
                                self.alreadyAte=True       
                                #for now it stays where it is
                                #self.x=newX
                                #self.y=newY
                                break
         
    
    """
    Schooling behavior which is for now, just random movement
    """
    def schoolMove(self, moveGrid):
        self.randomMove(moveGrid)

        
    
    def randomMove(self, okayMoveGrid):
        """Randomly move the tuna to a neighboring cell if available
        Only one tuna is allowed on each cell

        + okayMoveGrid: the boolean grid that specifies which cell is okay to move
                        to (0 = unoccupied cell; 1 = boundary cell; 2 = tuna occupied cell)
                        Obtained by calling okayMoveGrid(baseGrid) in Driver.py

        Tien 05/28/2017: add energy usage for random swim

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
                    self.energy -= ENERGY_SWIMMING

    
    """
    I think we are going to need to change this method a bit so that it only
    accounts for eating plankton, since tuna cannot occupy the same cell
    Cannibalization will take place during the move phase as one tuna takes the
    place of another. 
    """
    def eat(self, grid):
        """Tuna eats food and gains amount proportional to weight

        grid: the enviroment grid that holds the population

        """
        
        """
        If the tuna already hunted and ate another tuna during the move phase
        then skip eating plankton this phase.
        """
        if self.alreadyAte:
            self.alreadyAte=False
            pass
            
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
        #
        ##Subtract used energy
        #self.useEnergy()
        
        """
        remove tuna that have starved to death
        """
        if self.energy<STARVE:
            
            return False
        else:
            return True
    
    #"""
    #Tuna need to deplete energy swimming, for now this is constant every turn,
    #We may want to make them use more energy when they move and according to their
    #size, to be implemented later
    #"""
    #def useEnergy(self):
    #    self.energy-=(ENERGY_SWIMMING*self.length)
    
    """
    Growing algorithm
    grow and update values accordingly
    jgn 5.25, adding random factor to growth so all are not the same size
    Tien 05/28/2017: add temperature growth multiplier and size-dependent variable growth rate
    """
    def grow(self,grid):
        # If under STARVED_THRES, Tuna is starving and does not grow
        previousLength = self.length
        tempGrowthRate = 1.0
        if self.energy > STARVED_THRES:
            #determine temperature growth multiplier, with 22 Celsius as low, 28 Celsius as high
            #temperature above or below is range is not suitable for tuna, each 1 degree increase raises
            #growth rate by TEMP_MULTIPLIER 
            if grid[self.y, self.x].temperature >= TEMP_LOW and grid[self.y, self.x].temperature <= TEMP_HIGH:
                tempGrowthRate += ((grid[self.y, self.x].temperature % TEMP_LOW) * TEMP_MULTIPLIER)
            
            #growth rate varies based on size, below 7mm digestive system is not developed enough to eat fish-based food, hence
            # lower rate        
            if self.length < PLANKTON_ONLY_SIZE:
                self.length *= (1 + (self.energy * GROWTH_MULTIPLIER_BELOW_7MM) * tempGrowthRate * np.random.uniform(0.95,1.05))
            else:
                self.length *= (1 + (self.energy * GROWTH_MULTIPLIER_ABOVE_7MM) * tempGrowthRate * np.random.uniform(0.95,1.05))
            #new energy value after growth is relative to the growth in size
            self.energy = previousLength / self.length
