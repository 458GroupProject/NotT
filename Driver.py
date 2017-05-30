"""
Model Driver
"""
import numpy as N

from Consts import *
from water import water

from Tuna import Tuna
from Animate import *
from Analysis import *


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
    + Tien 05/28/2017: added feeding interval and growth interval in run() method

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

avgLength=0.0
avgEnergy=0.0
totalLength = 0.0
totalEnergy = 0.0

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
    #randomly assign food value for each water cell up to a maximum value
    simplelist = [water(N.random.uniform(0.0, maxInitPlankton), 0.0, initTemperature) for w in xrange((tankh+2) * (tankw+2))]    
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
                    grid[row][col].resident = t
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
        elif not t.update(grid):
            grid[t.y,t.x].tuna=False
            grid[t.y,t.x].resident=0
            tuna.remove(t)
            numStarved+=1
            numAlive-=1
            

"""
calls all the tuna grow methods
Also updates average 
"""
def growth(growthInterval):
    global numAlive, avgLength, avgEnergy, numStarved, totalLength, totalEnergy
    totalLength = 0.0
    totalEnergy = 0.0
    for t in tuna:
        t.grow(grid, growthInterval)
        totalLength+=t.length
        totalEnergy+=t.energy
    avgLength = totalLength / numAlive
    avgEnergy = totalEnergy / numAlive


"""
Tien 05/28/2017: added feeding interval and growth interval

Parameter:  + iterations: number of time steps
            + feedInterval: feeding period after every specific number of time steps
            + growthInterval: larvae growth period after every specific number of time steps
            + fishFoodRatio: the ratio of fish:plankton food in floating point
                For example: 0.30 means 30% of fish food and 70% of plankton food
"""
def run(iterations, feedInterval, growthInterval, fishFoodRatio, run, animation=False):
    global grid, numAlive, avgLength, avgEnergy, numStarved, numEatenAlive, totalLength, totalEnergy, tuna

    #data for analysis
    arr_iterations = N.array([],dtype='i')
    arr_numAlive = N.array([],dtype='i')
    arr_numStarved = N.array([],dtype='i')
    arr_numCorpses = N.array([],dtype='i')
    arr_numEatenAlive = N.array([],dtype='i')
    arr_numCorpsesEaten = N.array([],dtype='i')
    arr_avgLength = N.array([],dtype='d')
    arr_avgEnergy = N.array([],dtype='d')

    #A=animate(maxFood)
    B=analysis(iterations, run)
    
    for i in range(run):
        maxPlankton = maxInitPlankton    #maximum value of plankton food each water cell can hold
        maxFish = 0.0        #maximum value of fish food each water cell can hold
        #maximum value of total food (fish & plankton) expressed in term of energy
        maxFood = (maxPlankton * PLANKTON_ENERGY_MULTIPLIER) + (maxFish * FISH_ENERGY_MULTIPLIER)
        cycle = 0
        numAlive = 0
        numStarved = 0
        numEatenAlive = 0
        phase = 0    #phases of the tuna cycle (consumption, movement, remove)
        tuna = []    #list to hold tuna for each simulation run

        arr_iterations = N.append(arr_iterations,0)
        arr_numAlive = N.append(arr_numAlive,numAlive)
        arr_numStarved = N.append(arr_numStarved,numStarved)
        arr_numCorpses = N.append(arr_numCorpses,numCorpses)
        arr_numEatenAlive = N.append(arr_numEatenAlive,numEatenAlive)
        arr_numCorpsesEaten = N.append(arr_numCorpsesEaten,numCorpsesEaten)
        arr_avgLength = N.append(arr_avgLength,avgLength)
        arr_avgEnergy = N.append(arr_avgEnergy,avgEnergy)
                
        for j in range(1, iterations + 1):
            if(phase==0):
                #create initial grid and calculate inital average length & energy
                grid = init()
                totalLength = 0.0
                totalEnergy = 0.0
                for t in tuna:
                    totalLength+=t.length
                    totalEnergy+=t.energy        
                avgLength = totalLength / numAlive
                avgEnergy = totalEnergy / numAlive
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

            #update larvae growth at the appropriate interval set by user
            if j % growthInterval == 0:  
                previousTotalLength = totalLength
                growth(growthInterval)
                #determine the total increase/decrease in larvae length from the previous growth period (in %)
                lengthPercentIncrease = (totalLength - previousTotalLength) / previousTotalLength
                #increase/decrease the maximum amount of feed of fish-based & plankton-based relative to the increase/decrease
                #   in total length
                maxPlankton = maxPlankton * (1 + lengthPercentIncrease)
                maxFish = maxFish * (1 + lengthPercentIncrease)

            #at the beginning larvae can only eat plankton, after they reach a specific length we will start adding
            #   fish-based food in to the feeding mix, based on a ratio set by user
            if avgLength >= PLANKTON_ONLY_SIZE:
                maxFish = maxFood * fishFoodRatio
                maxPlankton = (maxFood - maxFish) / PLANKTON_ENERGY_MULTIPLIER         

            #Feeding interval is set by user
            if (j % feedInterval == 0):
                #add appropriate amount of fish-based & plankton-based food, depending on how many feeding periods are
                #    in each day              
                addedPlankton = maxPlankton * (float(feedInterval) / HOUR_PER_DAY)
                addedFish = maxFish * (float(feedInterval) / HOUR_PER_DAY)
                #update the maximum amount of total food each water cell can hold after larvae growth
                maxFood = (maxPlankton * PLANKTON_ENERGY_MULTIPLIER) + (maxFish * FISH_ENERGY_MULTIPLIER)
                #add food to each water cell
                for row in range (1, tankh + 1):
                    for col in range (1, tankw + 1):
                        #randomly add food, but only up to the maximum amount of food value each water cell can hold based on the value calculated above in growth interval
                        grid[row,col].updateFood(min(N.random.uniform(0, addedPlankton), (maxPlankton - grid[row,col].foodPlankton)), min(N.random.uniform(0, addedFish), (maxFish - grid[row,col].foodFish)))            
                
            phase+=1
            
            if phase==4:
                phase=1
                
            if animation:
                A=animate(maxFood)
                A.vis(grid,cycle,numAlive, avgLength, avgEnergy, numStarved, numEatenAlive, feedInterval)

            print str(cycle)+" Avg Size: "+str(round(avgLength,1)) + " Avg Energy: "+ str(round(avgEnergy,2)) + " Alive: " + str(numAlive)
            
            arr_iterations = N.append(arr_iterations, j)
            arr_numAlive = N.append(arr_numAlive,numAlive)
            arr_numStarved = N.append(arr_numStarved,numStarved)
            arr_numCorpses = N.append(arr_numCorpses,numCorpses)
            arr_numEatenAlive = N.append(arr_numEatenAlive,numEatenAlive)
            arr_numCorpsesEaten = N.append(arr_numCorpsesEaten,numCorpsesEaten)
            arr_avgLength = N.append(arr_avgLength,avgLength)
            arr_avgEnergy = N.append(arr_avgEnergy,avgEnergy)
            
            cycle+=1
  
                    
        B.graph(i, arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy)
        
        # for data analysis
        B.collect(i, arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy)
        
    B.analyze()    

#test 720 time steps, feed every 12 steps, grow every 24 steps, 50:50 fish:plankton mix)
run(720, 12, 24, .5, 10, animation=True)
