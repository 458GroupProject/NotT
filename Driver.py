"""
Model Driver
"""
import numpy as N
from imports import*
from Consts import*
from water import water
from Tuna import Tuna
from Globalvars import*

from animator import*

            

"""
Initializes the grid with water agents, then adds food and prey according
to starting conditions,
also adds tuna larvae

Starting population will not be exact, but the target init popualtion/ grid area
will be the liklihookd of a larva starting in a certain cell
"""
def init():
    #global grid, numAlive, tuna, tankh, tankw
    #creating h by w water grid
    simplelist = [water(0,0,0) for w in xrange(tankh*tankw)]    
    grid=N.array(simplelist)
    grid=N.reshape(grid, (tankh,tankw))    
                
    #loop through rows along height        
    for r in range(tankh):
        #loop through columns in width
        for c in range(tankw):
                r = N.random.uniform()
                if r > initPop/(tankw*tankh):
                    t = Tuna(c,r)
                    tuna.append(t)
                    grid[r][c].tuna=True
                        

"""
Loops through all tuna agents and calls tunaMayEat()
which will also trigger hunting behavior
"""    
def consumption():
    pass

"""
Loops through all tuna agents and calls their move methods
"""
def movement():
    pass

"""
removes tuna who starved to death, or atleast marks them as dead
"""  
def remove():
    pass

"""
calls all the tuna grow methods
"""
def growth():
    pass


def run():
    
    global grid
    
    #how many time steps one simulation will last
    # 30 days, 1 time step per hour 30x24=720
    iterations=720
    
    runs=1
    
    phase=0
    
    A=animator()
    
    for i in range(runs):
    
        for j in range(iterations):
            if(phase==0):
                init()
                A.hello()
                
                #testing
                
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
            print phase

run()