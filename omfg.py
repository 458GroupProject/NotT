import numpy as N
from Consts import*
import matplotlib.pyplot as plt

class animate:
    
    plt.ion()
    def vis(self, grid, cycle):
      
        r_c=N.shape(grid)

        for r in range(tankh):
            for c in range(tankw):

                w=grid[r,c]
                if w.tuna:
                    plt.scatter(c,r,color=(1,0,0,1),marker='s')
                else:    
                    plt.scatter(c,r,color=(0,0,1,1),marker='s')
        
        plt.title("Tuna, cycle #"+str(cycle))
        plt.draw()
        plt.pause(.01)
