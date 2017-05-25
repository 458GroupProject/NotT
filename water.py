# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#Description: Water class as the environment of each tank grid cell
#Programmer: Tien Huynh
#Reference:
#   + "Biology and Ecology of Bluefin Tuna" by Kitagawa et al.
#   + "Cannibalism among size classes of larvae may be a substantial mortality
#       component in tuna" by Reglero et al.
#   + "Relationship between the growth and survival of larval Pacific bluefin
#       tuna, Thunnus orientalis" by Satoh et al.
#-------------------------------------------------------------------------------
#Change Log
#jgn 5/25 adding a reference to the Tuna which is in this square, to make anim-
#ation easier, added maxPlankton constant
#-------------------------------------------------------------------------------
class water(object):
    

    
    
    #Plankton: mainly microscopic animals that are more suitable for larvae
    #    without a developed digestive system, but they could still be fed
    #    to more developed individuals; they have lesser nutritional value,
    #    so growth rate is lower for this food type.
    foodPlankton = 0.0
    
    #Fish: such as other fish species prey types including the case of tuna
    #    cannibalism; they offer much higher nutritional value.
    #
    #NOTE: fish food should give 50% more energy value vs. plankton food for
    #    the same amount of food (i.e. tuna that eat fish food should grow 50%
    #    faster than ones that eat plankton food)
    #    Inferred from Kitagawa's book, page 39
    foodFish = 0.0
    
    #-----------------NOTE on food----------------------------------------------
    #Kitagawa’s research show up to 50x difference in growth rate (dry weight)
    #    between tuna larvae fed only with rotifer and fed with extra fish.
    #    Correlation could be taken from this research.
    #Size different is the main factor in determining cannibalism success rate,
    #    so access to higher quality food could make a big difference in 
    #    finding the cannibalism rate
    #We might change the food system from a relative value (0.0-1.0)
    #    to an absolute system using weight or serving to accord for difference
    #    in food demand of varying tuna larvae sizes; A larger larvae should
    #    require more food intake every time step to maintain or grow in size.
    #---------------------------------------------------------------------------

    #Ambient temperature of the cell
    #Preferred temperature range for tune larvae is 25 to 30 Celsius.
    #Temperature significantly affects growth rate; higher temperature
    #    result in faster growth rate.
    #22 Celsius could be used as starting temperature for analysis, up to 30 Celsius.
    #Temperature’s correlation to growth rate could be inferred from Reglero model.
    #
    #NOTE: growth rate increases by ~15% for each increase of 1 Celsius degree
    #    Inferred from Satoh's research, page 699
    temperature = 0.0

    #Flag to check whether a tuna is present on the water cell
    #NOTE: might not be necessary if model use a list to keep track of all tuna location
    tuna = False
    
    #This is a reference to the actual tuna residing in this qater cell, set to 0
    #when empty
    resident=0
    
    def __init__(self, plankton, fish, temperature):
      self.foodPlankton = plankton
      self.foodFish = fish
      self.temperature = temperature 
      self.resident=0     

    #Method to update food amount to the water agent
    #Parameter:
    #   +planktonAmt: amount of plankton food type to be updated to the cell (in gram maybe)
    #   +fishAmt: amount of fish food type to be updated to the cell (in gram maybe)
    def updateFood(self, planktonAmt, fishAmt):
        self.foodPlankton += planktonAmt
        self.foodFish += fishAmt       

    #Method to change temperature to a new value
    #Parameter:
    #   +newTemp: the new temperature value to be changed to (in Celsius)
    def changeTemperature(self, newTemp):
        self.temperature = newTemp        

