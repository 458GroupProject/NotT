"""
Model Driver
"""
import Consts.py
import Globalvars.py
            

"""
Initializes the grid with water agents, then adds food and prey according
to starting conditions,
also adds tuna larvae

Starting population will not be exact, but the target init popualtion/ grid area
will be the liklihookd of a larva starting in a certain cell
"""
def init():
            Global grid, numAlive
    #creating h by w water grid
    simplelist = [water() for w in xrange(42*42)]    
    grid=N.array(simplelist)
    grid=N.reshape(grid, (42,42)     
            
            
    #loop through rows along height        
    for r in range(tankh):
            #loop through columns in width
            for c in range(tankw):
                   r = N.random.uniform()
                   if r > initPop/(tankw*tankh):
                        t = tuna()
                        tuna.append(t)
                        grid[r][c].tuna=true
                        

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
