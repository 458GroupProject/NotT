import numpy as N
from Consts import*
import matplotlib.pyplot as plt
"""
jgn 5/23 added coloring for plankton levels
5/25 added size changes in tuna, labels with additional info,
Matt 5/27: added graph def to use to output/analyze data
change color of cannibalizing tuna
"""


class animate:
    def __init__(self, mp):
         self.maxPlankton=mp
    
    plt.ion()
    
    def vis(self, grid, cycle, numAlive, avgLength, avgEnergy, numStarved, numEatenAlive):
        global maxPlankton
        r_c=N.shape(grid)
        plt.clf()

        for r in range(tankh+2):
            for c in range(tankw+2):

                w=grid[r,c]
                alpha=w.foodPlankton/maxPlankton
                T=w.resident
                
                if T != 0:
                    if T.alreadyAte:
                        tuna_color=(1,0,0,1)
                    else:
                        tuna_color=(0,0,0,1)
                
                plt.scatter(c,r,color=(0,alpha,1-alpha,1),s=100,marker='s')
                
                if w.tuna:
                    plt.scatter(c,r,color=tuna_color,s=T.length*2)
                   
                    
        
        
        plt.title("Hour "+str(cycle)+":00")
        plt.xlabel("Tuna Alive: "+str(numAlive)+"  AvgSize: "+str(round(avgLength,1)) + "  AvgEnergy: "+ str(round(avgEnergy,2)))
        plt.ylabel("numStarved "+ str(numStarved)+"\n" + "numEatenAlive " +str(numEatenAlive))
        plt.draw()
        plt.pause(.01)
        
    def graph(self, arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy):
        return
