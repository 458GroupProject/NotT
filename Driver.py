"""
Model Driver
"""
import Consts.py
import Globalvars.py
            

"""
Initializes the grid with water agents, then adds food and prey according
to starting conditions,
also adds tuna larvae
"""
def init():
    pass

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


#how many time steps one simulation will last
# 30 days, 1 time step per hour 30x24=720
iterations=720

runs=1

phase=0

for i in range(runs):
    
    for j in range(iterations):
        if(phase==0):
            init()
        elif(phase==1):
            consumption() 
        elif(phase==2):
            movement()   
        elif(phase==3):
            remove()
        elif(phase==4):
            growth()
