"""
Model Driver
"""
import numpy as N

from Consts import*
from water import water
from Tuna import Tuna
from omfg import*


#-------------------------------------------------------------------------------
"""
History: 
    + Jeremy
    + Matt
    + 05/23/2017: Tien
        - Added boundary cells to the grid in the init() function
        - Added okayMoveGrid(baseGrid)
        
"""
#-------------------------------------------------------------------------------

 
"""
Simulation variables
"""           
numAlive=0
numCorpses=0
numEatenAlive=0
numCorpsesEaten=0

#list of all existing tuna
tuna=[]                      

grid=0                                          

"""
Initializes the grid with water agents, then adds food and prey according
to starting conditions,
also adds tuna larvae

Starting population will not be exact, but the target init popualtion/ grid area
will be the liklihookd of a larva starting in a certain cell
"""
def init():

    global numAlive, tuna, tankh, tankw
    #creating h by w water grid, with 1 boundary
    simplelist = [water(0,0,0) for w in xrange((tankh+2) * (tankw+2))]    
    grid=N.array(simplelist)
    grid=N.reshape(grid, (tankh + 2,tankw + 2))    
                
    #loop through rows along height        
    for row in range(tankh + 2):
        #loop through columns in width
        for col in range(tankw + 2):
            #update the food to -1 to mark boundary cells
            if row == 0 or row == tankh + 1 or col == 0 or col == tankw + 1:
                grid[row][col].updateFood(-1,-1)
            #randomly assign tuna
            else:
                rand = N.random.uniform()
                if rand < (float(initPop)/(tankw*tankh)):
                    t = Tuna(col,row)
                    tuna.append(t)
                    grid[row][col].tuna=True
    return grid                  


"""
Create a copy of the base grid and mark cells that are occupied by tuna or are
boundary cells (0 = unoccupied cell; 1 = boundary cell; 2 = tuna occupied cell)

    + baseGrid: the original base grid
"""
def okayMoveGrid(baseGrid):
    moveGrid = N.zeros(baseGrid.shape, dtype = int)
    #mark boundary cells
    moveGrid[:,0] = 1
    moveGrid[:,-1] = 1
    moveGrid[0,:] = 1
    moveGrid[-1,:] = 1
    #mark tuna occupied cells
    for i in tuna:
        moveGrid[i.y, i.x] = 2
    return moveGrid


"""
Loops through all tuna agents and calls tunaMayEat()
which will also trigger hunting behavior
"""    
def consumption():
    for t in tuna:
        t.eat(grid)

"""
Loops through all tuna agents and calls their move methods
"""
def movement():
    for t in tuna:
        t.move(grid)

"""
removes tuna who starved to death, or atleast marks them as dead
"""  
def remove():
    for t in tuna:
        t.update(grid)

"""
calls all the tuna grow methods
"""
def growth():
    for t in runa:
        t.grow(grid)


def run():
    global grid
    #how many time steps one simulation will last
    # 30 days, 1 time step per hour 30x24=720
    iterations=720
    
    runs=1
    
    phase=0

    A=animate()
    
    for i in range(runs):
    
        for j in range(iterations):
            if(phase==0):
                grid = init()
                
                                #testing visualization of init grid
                A.vis(grid)

                
            elif(phase==1):
                consumption() 
            elif(phase==2):
                movement()   
            elif(phase==3):
                remove()
            elif(phase==4):
                growth()

            phase+=1
            if phase==5:
                phase=1


run()
