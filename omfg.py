import numpy as N
from Consts import*
import matplotlib.pyplot as plt
"""
jgn 5/23 added coloring for plankton levels
"""
class animate:
    
    plt.ion()
    def vis(self, grid, cycle):
      
        r_c=N.shape(grid)
        plt.clf()

        for r in range(tankh+2):
            for c in range(tankw+2):

                w=grid[r,c]
                alpha=w.foodPlankton/10.0
                
                if w.tuna:
                    plt.scatter(c,r,color=(1,0,0,1),s=400)
                else:    
                    plt.scatter(c,r,color=(0,alpha,1-alpha,1),s=400,marker='s')
        
        plt.title("Tuna, cycle #"+str(cycle))
        plt.draw()
        plt.pause(.01)
