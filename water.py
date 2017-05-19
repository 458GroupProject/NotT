# -*- coding: utf-8 -*-
#water class as the environment of each tank grid cell
class water(object):
    #Rotifer: mainly microscopic animals that are more suitable for larvae
    #    without a developed digestive system, but they could still be fed
    #    to more developed individuals; they have lesser nutritional value,
    #    so growth rate is lower for this food type.
    foodRotifer = 0
    
    #Fish: such as other fish species prey types including the case of tuna
    #    cannibalism; they offer much higher nutritional value.
    foodFish = 0
    
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

    #Preferred temperature range for tune larvae is 25 to 30 Celsius.
    #Temperature significantly affects growth rate; higher temperature
    #    result in faster growth rate.
    #22 Celsius could be used as starting temperature for analysis, up to 30 Celsius.
    #Temperature’s correlation to growth rate could be inferred from Reglero model.
    temperature = 0
    
    def __init__(self):
        pass        

    #Method to add food amount to the water agent
    #Parameter:
    #   +rotifer: amount of rotifer food type to be added to the cell (in gram maybe)
    #   +fish: amount of fish food type to be added to the cell (in gram maybe)
    def addFood(self, rotifer, fish):
        pass        

    #Method to change temperature to a new value
    #Parameter:
    #   +newTemp: the new temperature value to be changed to (in Celsius)
    def changeTemperature(self, newTemp):
        pass     