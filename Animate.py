import numpy as N
from Consts import*
import matplotlib.pyplot as plt

import time
import pygame, sys
from pygame.locals import *
import pygame.gfxdraw

"""
jgn 5/23 added coloring for plankton levels
5/25 added size changes in tuna, labels with additional info,

Matt 5/27: added graph def to use to output/analyze data
change color of cannibalizing tuna

Arthur 5/28: Added pygame functionality for display to replace matplotlib
"""


class animate:
    def __init__(self, mp):
         self.maxPlankton=mp
    
    def vis(self, grid, cycle, numAlive, avgLength, avgEnergy, numStarved, numEatenAlive):        
        #plt.title("Hour "+str(cycle)+":00")
        #plt.xlabel("Tuna Alive: "+str(numAlive)+"  AvgSize: "+str(round(avgLength,1)) + "  AvgEnergy: "+ str(round(avgEnergy,2)))
        #plt.ylabel("numStarved "+ str(numStarved)+"\n" + "numEatenAlive " +str(numEatenAlive))
        #plt.draw()
        #plt.pause(.01)
        
        pygame.init()

        # Set RGB colors
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)

        # Create window
        displaySim = pygame.display.set_mode((tankw, tankh))
        displaySim.fill(BLUE)
        pygame.display.set_caption("Tuna Fishery")
        
        self.createBorders(displaySim, BLACK)
        
        # Set running fps
        fpsClock = pygame.time.Clock()
        fpsClock.tick(60)

        global maxPlankton
        r_c=N.shape(grid)

        for r in range(tankh+2):
            for c in range(tankw+2):

                w=grid[r,c]
                alpha=w.foodPlankton/maxPlankton
                T=w.resident

                pygame.gfxdraw.box(displaySim, pygame.Rect(r, c, 1, 1), (0, int(255 * alpha), 255 - int(alpha * 255), 200))
                self.createBorders(displaySim, BLACK)

                if w.tuna:
                    if T.alreadyAte:
                        pygame.draw.circle(displaySim, WHITE, (r, c), 1, 1)
                    else:
                        pygame.draw.circle(displaySim, RED, (r, c), 1, 1)

        pygame.display.update()

    def createBorders(self, screen, color):
        pygame.draw.rect(screen, color, (0, 0, tankw, 2)) 
        pygame.draw.rect(screen, color, (0, 0, 2, tankh))
        pygame.draw.rect(screen, color, (tankw - 2, 0, 2, tankh))
        pygame.draw.rect(screen, color, (0, tankh - 2, tankw, 2))
