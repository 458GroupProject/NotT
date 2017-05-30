import numpy as N
from Consts import*
from Tuna import*
import matplotlib.pyplot as plt

import time
import pygame, sys
from pygame.locals import *
import pygame.event
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

#Special lines for centering pygame window
import pygame, os 

position = 10, 10
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

class animate:
    def __init__(self, mp,trial):
         self.maxPlankton=mp
         self.trial=trial
    
    def vis(self, grid, cycle, numAlive, avgLength, avgEnergy, numStarved, numEatenAlive, feedInterval,initTemperature,initPop,VISIBILITY):  
        # Center pygame window
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.init()
        
        # Allows program to actually close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # Set RGB colors
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)

        # Create window
        win = 12 #window size multiplier
        displaySim = pygame.display.set_mode((int((tankw+2)*win*2.5), (tankh+2)*win+150))
        displaySim.fill(WHITE)
        pygame.display.set_caption("Tuna Fishery")
        
        # Set running fps
        fpsClock = pygame.time.Clock()
        fpsClock.tick(60)

        r_c=N.shape(grid)
        
        #draw borders black jgn, working for big square borders
        pygame.draw.rect(displaySim, BLACK, pygame.Rect(0, 0, (tankw + 2) * win, (tankh + 2) * win))
        
        #iteration for water only
        #iteration through rows
        for r in range(1, tankh + 1):
            #it through columns
            for c in range(1, tankw + 1):

                w = grid[r, c]
                alpha = (w.foodPlankton * PLANKTON_ENERGY_MULTIPLIER + w.foodFish * FISH_ENERGY_MULTIPLIER) / self.maxPlankton
                
                if alpha > 1:
                    alpha = 1
                if alpha < 0:
                    alpha = 0
                
                T = w.resident
                
                size = 1
                # Make sure Tuna object is not an int
                if(T != 0):
                    size = int(T.length / 2)
                if size < 1:
                    size = 1
                
                #watercolor=(0, int(255 * alpha), 255 - int(alpha * 255), 200)
                watercolor=(0,int(255 * alpha),255 - int(alpha * 255),200)
                pygame.gfxdraw.box(displaySim, pygame.Rect(r*win, c*win, win, win), watercolor)

        #Iteration 2 for tuna only
        #iteration through rows
        for r in range(1, tankh + 1):
            #it through columns
            for c in range(1, tankw + 1):

                w=grid[r, c]
                
                if alpha > 1:
                    alpha = 1
                if alpha < 0:
                    alpha = 0
                
                T = w.resident
                
                size = 1
                if(T != 0):
                    size = int(T.length / 2)
                if size < 1:
                    size = 1

                if w.tuna:
                    if T.alreadyAte:
                        color = WHITE
                    else:
                        color = RED
                    pygame.draw.circle(displaySim, color, (r * win + int(0.5 * win), c * win + int(0.5 * win)), size, size)
        
        myfont = pygame.font.SysFont("arial", 20)

        # render text
        if cycle % 24 < 10:
            zero = "0"
        else:
            zero = ""
            
        if cycle < 240:
            zero2 = "0"
        else:
            zero2 = ""
        
        # Create labels
        labelvh = myfont.render("Trial # " + str(self.trial) + " Model Variables:", 1, BLACK)
        labelh = myfont.render("Day:Hour ", 1, BLACK)
        label = myfont.render(zero2 + str(round(cycle / 24, 2)) + ":" + zero + str(round(cycle % 24, 2)) + ":00", 1, BLACK)
        label2 = myfont.render("Feed #" + str(round(cycle / feedInterval, 0)), 1, BLACK)
        label3 = myfont.render("avg Length: " + str(round(avgLength, 2)) + " mm", 1, BLACK)
        label4 = myfont.render("avg Energy:" + str(round(avgEnergy, 2)), 1,BLACK)
        label6 = myfont.render("num Alive: " + str(numAlive), 1, BLACK)
        label7 = myfont.render("num Starved to Death: " + str(numStarved), 1, BLACK)
        label8 = myfont.render("num Eaten Alive: " + str(numEatenAlive), 1, BLACK)
        
        label9 = myfont.render("Red dot = Tuna  |  Greener square = more food" , 1, BLACK)
        label10 = myfont.render("Bluer square = less food  | White dot flash = Cannibal Tuna instance", 1, BLACK)
        
        label10b = myfont.render("Model Constants:", 1, RED)
        #calculating volume:
        width = tankw*tile_width #cm
        height = tankh*tile_width #cm
        depth = tile_width #cm
        volume = width/10.0*height/10.0*depth/10.0 #cm cubed
        volume = volume/1000 #L cubed 
        label11 = myfont.render("Tank cross-section dimensions:  width: " +str(width)+"mm x height: "+str(height)+"mm x depth: "+str(depth)+"mm", 1, RED)
        label11b = myfont.render("Tank volume:  "+str(volume)+" L", 1, RED)
        label11c = myfont.render("Initial Tuna pop: " + str(initPop), 1, RED)
        label12 = myfont.render("Initial hatchling density: " + str(round(initPop/volume,2))+" /L", 1, RED)
        
        label13 = myfont.render("Tuna Aggression: " +str(AGGRESSION)+" (probability to attack tuna when hungry)", 1, RED)
        label14 = myfont.render("Water Visibility Modifier: "+str(VISIBILITY)+" (-15cm of vision for hunting)", 1, RED)
        label15 = myfont.render("Water Temperature: "+str(initTemperature)+" c", 1, RED)
        label16 = myfont.render("Feed Interval : "+str(feedInterval)+" hrs", 1, RED)
        
        # Position Labels
        displaySim.blit(labelvh, (tankw * win + 100, 0))
        displaySim.blit(labelh, (tankw * win + 95, 30))
        displaySim.blit(label, (tankw * win + 100, 50))
        displaySim.blit(label2, (tankw * win + 100, 75))
        displaySim.blit(label3, (tankw * win + 100, 100))
        displaySim.blit(label4, (tankw * win + 100, 125))

        displaySim.blit(label6, (tankw * win + 100, 150))
        displaySim.blit(label7, (tankw * win + 100, 175))
        displaySim.blit(label8, (tankw * win + 100, 200))
        displaySim.blit(label9, (10, tankh * win + 50))
        displaySim.blit(label10, (10, tankh * win + 100))
        
        displaySim.blit(label10b, (tankw * win + 50, 250))
        displaySim.blit(label11, (tankw * win + 50, 275))
        displaySim.blit(label11b, (tankw * win + 50, 300))
        displaySim.blit(label11c, (tankw * win + 250, 300))
        displaySim.blit(label12, (tankw * win + 50, 325))
        displaySim.blit(label13, (tankw * win + 50, 350))
        displaySim.blit(label14, (tankw * win + 50, 375))
        displaySim.blit(label15, (tankw * win + 50, 400))
        displaySim.blit(label16, (tankw * win + 50, 425))
        pygame.display.update()
