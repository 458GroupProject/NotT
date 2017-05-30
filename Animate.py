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

jgn 5/29 making display larger, making plankton squares visble, tuna increase in size
add borders
"""


class animate:
    def __init__(self, mp):
         self.maxPlankton=mp
    
    def vis(self, grid, cycle, numAlive, avgLength, avgEnergy, numStarved, numEatenAlive, feedInterval):        
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
        #window size multiplier
        win=10
        displaySim = pygame.display.set_mode(((tankw+4)*win*2, (tankh+4)*win))
        displaySim.fill(BLUE)
        pygame.display.set_caption("Tuna Fishery")
        
        self.createBorders(displaySim, BLACK)
        
        # Set running fps
        fpsClock = pygame.time.Clock()
        fpsClock.tick(60)

        r_c=N.shape(grid)
        #draw borders black
        pygame.draw.rect(displaySim, BLACK, pygame.Rect(0, 0, (tankw+2)*win, (tankh+2)*win))
        
        #iteration for water only
        #iteration through rows
        for r in range(1, tankh+1):
            #it through columns
            for c in range(1, tankw+1):

                w=grid[r,c]
                alpha=(w.foodPlankton * PLANKTON_ENERGY_MULTIPLIER + w.foodFish * FISH_ENERGY_MULTIPLIER)/self.maxPlankton
                
                if alpha>1:
                    alpha=1
                if alpha<0:
                    alpha=0
                
                T=w.resident
                
                size=1
                if(T!=0):
                    size=int(T.length/2)
                if size <1:
                    size=1
                
                #watercolor=(0, int(255 * alpha), 255 - int(alpha * 255), 200)
                watercolor=(0,int(255 * alpha),255 - int(alpha * 255),200)
                pygame.gfxdraw.box(displaySim, pygame.Rect(r*win, c*win, win, win), watercolor)
                self.createBorders(displaySim, BLACK)


        #Iteration 2 for tuna only
        #iteration through rows
        for r in range(1, tankh+1):
            #it through columns
            for c in range(1, tankw+1):

                w=grid[r,c]
                
                if alpha>1:
                    alpha=1
                if alpha<0:
                    alpha=0
                
                T=w.resident
                
                size=1
                if(T!=0):
                    size=int(T.length/2)
                if size <1:
                    size=1

                if w.tuna:
                    if T.alreadyAte:
                        color=WHITE
                    else:
                        color=RED
                    pygame.draw.circle(displaySim, color, (r*win+int(.5*win), c*win+int(.5*win)), size, size)
        
        
        myfont = pygame.font.SysFont("monospace", 15)

        # render text
        if cycle%24<10:
            zero="0"
        else:
            zero=""
            
        if cycle<240:
            zero2="0"
        else:
            zero2=""
        labelh=myfont.render("Day:Hour ", 1, (255,255,0))
        label = myfont.render(zero2+str(cycle/24)+":"+zero+str(cycle%24)+":00", 1, (255,255,0))
        label2 = myfont.render("Feed #"+str(cycle/feedInterval), 1, (255,255,0))
        label3 = myfont.render("avg Length: "+str(round(avgLength,2))+" mm", 1, (255,255,0))
        label4 = myfont.render("avg Energy:"+str(avgEnergy), 1, (255,255,0))
        label6 = myfont.render("num Alive: "+str(numAlive), 1, (255,255,0))
        label7 = myfont.render("num Starved to Death: "+str(numStarved), 1, (255,255,0))
        label8 = myfont.render("num Eaten Alive: " + str(numEatenAlive), 1, (255,255,0))
        
        displaySim.blit(labelh, (tankw*win+195, 80))
        displaySim.blit(label, (tankw*win+200, 100))
        displaySim.blit(label2, (tankw*win+200, 150))
        displaySim.blit(label3, (tankw*win+200, 200))
        displaySim.blit(label4, (tankw*win+200, 250))

        displaySim.blit(label6, (tankw*win+200, 300))
        displaySim.blit(label7, (tankw*win+200, 350))
        displaySim.blit(label8, (tankw*win+200, 400))
        
        pygame.display.update()

    def createBorders(self, screen, color):
        pygame.draw.rect(screen, color, (0, 0, tankw, 2)) 
        pygame.draw.rect(screen, color, (0, 0, 2, tankh))
        pygame.draw.rect(screen, color, (tankw - 2, 0, 2, tankh))
        pygame.draw.rect(screen, color, (0, tankh - 2, tankw, 2))
