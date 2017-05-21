#=======================================================================
#                        General Documentation

""" Allows the creation and manipulation of a Tuna object.
"""

#-----------------------------------------------------------------------
#                       Additional Documentation
# Modification History:
# - 18 May 2017:  Original by Arthur (Ky-Phuoc) Khuu
#
# Notes:
# - Written for Python 3
# - See import statements throughout for more information on non-
#   built-in packages and modules required.
#
#=======================================================================

class Tuna:
    def __init__(self, xLoc, yLoc, weight, sightRadius=1, energy=0.5):
        self.x = xLoc
        self.y = yLoc
        self.weight = weight
        self.sightRadius = sightRadius 
        self.energy = energy

    def move(environment):
        pass

    def eat(amount):
        pass




