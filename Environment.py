
class Environment:
    def __init__(self, width, length, temp, salinity):
        self.width = width
        self.length = length
        self.temperature = temp
        self.salinity = salinity

    def initEnvironment(self):
        pass

    def createEnvironment(self, xLoc, yLoc, width, length, temp, salinity):
        pass

    def modifyEnvironment(self, xLoc, yLoc, width, length, temp, salinity):
        pass