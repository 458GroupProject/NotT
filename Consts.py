

#tank width and height
tankw=int(60)

tankh=int(60)

#initial tuna larvae
initPop=3000.0

#maxPlankton value per cell initially so that a larvae with initial energy value
#   of 0.5 at and average lenth of 3mm could eat and reach 1.0 energy value
maxPlankton=3.0

#initial temperature value
initTemperature = 25.0

#Starvation death level
STARVE=0

#WaterVisibility (subracted from tuna visual range)
VISIBILITY=0

#global_run for data graphing
current_run = 1

PLANKTON_ENERGY_MULTIPLIER = 0.5
FISH_ENERGY_MULTIPLIER = 1.0
PLANKTON_ONLY_SIZE = 7.0 #larvae below this size can only eat plankton food