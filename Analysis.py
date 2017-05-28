import numpy as N
from Consts import*
import matplotlib.pyplot as plt
"""
Matt 5/28: class created
"""

class analysis:
    def __init__(self,it, rn):
        self.iterations = it
        self.runs = rn
        
    def graph(self, arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy):
        global current_run
        plt.figure(current_run)
        plt.subplot(311)
        plt.ylabel('Number')
        plt.plot(arr_iterations,arr_numAlive,'b.',label='Alive')
        plt.plot(arr_iterations,arr_numStarved,'g.',label='Starved')
        plt.plot(arr_iterations,arr_numCorpses,'k.',label='Corpses')
        plt.plot(arr_iterations,arr_numEatenAlive,'c.',label='EatenAlive')
        plt.plot(arr_iterations,arr_numCorpsesEaten,'r.',label='CorpsesEaten')
        plt.legend(loc='lower left', bbox_to_anchor=(0., 1.02, 1., .102),ncol=5)
        plt.subplot(312)
        plt.ylabel('Average Length')
        plt.plot(arr_iterations,arr_avgLength)
        plt.subplot(313)
        plt.xlabel('Iteration')
        plt.ylabel('Average Energy')
        plt.plot(arr_iterations,arr_avgEnergy)
        plt.show()
        
    def collect(self, arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy):
        global current_run
        current_run = current_run + 1
        
    def analyze(self):
        pass
