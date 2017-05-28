"""
Model Driver
"""
import numpy as N

from Consts import*
from water import water

from Tuna import Tuna
from omfg import*
from Analysis import*


#-------------------------------------------------------------------------------
"""
History: 
    + Jeremy
    + Matt
    + 05/23/2017: Tien
        - Added boundary cells to the grid in the init() function
        - Added okayMoveGrid(baseGrid)
      Jeremy 5/23 17:45-19:00 integrating random move and animate  
      Matt 5/27: added support for data collection of various data
"""
#-------------------------------------------------------------------------------
"""
simulation constants
"""
 
"""
Simulation variables
"""           
numAlive=0
numStarved=0
numCorpses=0
numEatenAlive=0
numCorpsesEaten=0

avgLength=0
avgEnergy=0

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

    global numAlive, tuna, tankh, tankw, maxPlankton
    #creating h by w water grid, with 1 boundary
    #starting food values & temp
    simplelist = [water(maxPlankton,10,25) for w in xrange((tankh+2) * (tankw+2))]    
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
                    numAlive+=1
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
        if not t.eaten:
            t.eat(grid)

"""
Loops through all tuna agents and calls their move methods
"""
def movement():

    for t in tuna:
        if t.eaten or t.alreadyAte:
            pass
        else:
            moveGrid=okayMoveGrid(grid)
            grid[t.y,t.x].tuna=False
            grid[t.y,t.x].resident=0
            t.move(moveGrid,grid)
            grid[t.y,t.x].tuna=True
            grid[t.y,t.x].resident=t

"""
removes tuna who starved to death, or atleast marks them as dead
"""  
def remove():
    global tuna, numStarved, numAlive, numEatenAlive
    for t in tuna:
        if t.eaten:
            grid[t.y,t.x].tuna=False
            grid[t.y,t.x].resident=0
            tuna.remove(t)
            numEatenAlive+=1
            numAlive-=1 
        #removing starving tuna
        if not t.update(grid):
            grid[t.y,t.x].tuna=False
            grid[t.y,t.x].resident=0
            tuna.remove(t)
            numStarved+=1
            numAlive-=1
            

"""
calls all the tuna grow methods
Also updates average 
"""
def growth():
    global numAlive, avgLength, avgEnergy, numStarved
    for t in tuna:
        t.grow(grid)
        avgLength+=t.length
        avgEnergy+=t.energy
    avgLength/=numAlive
    avgEnergy/=numAlive

def run():
    global grid, numAlive, avgLength, avgEnergy, numStarved, numEatenAlive
    #how many time steps one simulation will last
    # 30 days, 1 time step per hour 30x24=720
    iterations=720
    
    runs=1
    
    phase=0
    cycle=0
    
    #data for analysis
    arr_iterations = N.array([],dtype='i')
    arr_numAlive = N.array([],dtype='i')
    arr_numStarved = N.array([],dtype='i')
    arr_numCorpses = N.array([],dtype='i')
    arr_numEatenAlive = N.array([],dtype='i')
    arr_numCorpsesEaten = N.array([],dtype='i')
    arr_avgLength = N.array([],dtype='d')
    arr_avgEnergy = N.array([],dtype='d')

    A=animate(maxPlankton)
    B=analysis(iterations, runs)
    
    for i in range(runs):
        
        arr_iterations = N.append(arr_iterations,0)
        arr_numAlive = N.append(arr_numAlive,numAlive)
        arr_numStarved = N.append(arr_numStarved,numStarved)
        arr_numCorpses = N.append(arr_numCorpses,numCorpses)
        arr_numEatenAlive = N.append(arr_numEatenAlive,numEatenAlive)
        arr_numCorpsesEaten = N.append(arr_numCorpsesEaten,numCorpsesEaten)
        arr_avgLength = N.append(arr_avgLength,avgLength)
        arr_avgEnergy = N.append(arr_avgEnergy,avgEnergy)
                
        for j in range(iterations):
            if(phase==0):
                grid = init()
                
                                #testing visualization of init grid
                #A.vis(grid,cycle)

                
            elif(phase==1):
                consumption() 
            elif(phase==2):
                movement()   
            elif(phase==3):
                remove()
                if numAlive<=0:
                    break
            elif(phase==4):
                growth()

            phase+=1
            if phase==5:
                phase=1
                A.vis(grid,cycle,numAlive, avgLength, avgEnergy, numStarved, numEatenAlive)
                print str(cycle)+" Avg Size: "+str(round(avgLength,1)) + " Avg Energy: "+ str(round(avgEnergy,2))
                
                arr_iterations = N.append(arr_iterations, j)
                arr_numAlive = N.append(arr_numAlive,numAlive)
                arr_numStarved = N.append(arr_numStarved,numStarved)
                arr_numCorpses = N.append(arr_numCorpses,numCorpses)
                arr_numEatenAlive = N.append(arr_numEatenAlive,numEatenAlive)
                arr_numCorpsesEaten = N.append(arr_numCorpsesEaten,numCorpsesEaten)
                arr_avgLength = N.append(arr_avgLength,avgLength)
                arr_avgEnergy = N.append(arr_avgEnergy,avgEnergy)
                
                cycle+=1
            
        B.graph(arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy)
        
        # for data analysis
        B.collect(arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy)
        
    B.analyze()    


run()
