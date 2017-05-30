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
        
        self.final_arr_numAlive_data = N.empty([self.runs], dtype='d')
        self.final_arr_numStarved_data = N.empty([self.runs], dtype='d')
        self.final_arr_numCorpses_data = N.empty([self.runs], dtype='d')
        self.final_arr_numEatenAlive_data = N.empty([self.runs], dtype='d')
        self.final_arr_numCorpsesEaten_data = N.empty([self.runs], dtype='d')
        self.final_arr_avgLength_data = N.empty([self.runs], dtype='d')
        self.final_arr_avgEnergy_data = N.empty([self.runs], dtype='d')
    
    # Create graph for simulation
    def graph(self, run, arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy):
        plt.figure(run)
        plt.subplot(311)
        plt.ylabel('Number')
        plt.plot(arr_iterations,arr_numAlive, 'b.', label='Alive')
        plt.plot(arr_iterations,arr_numStarved, 'g.', label='Starved')
        plt.plot(arr_iterations,arr_numEatenAlive, 'c.', label='EatenAlive')
        plt.legend(loc='lower left', bbox_to_anchor=(0., 1.02, 1., 0.102), ncol=3)
        plt.subplot(312)
        plt.ylabel('Average Length')
        plt.plot(arr_iterations, arr_avgLength,'k.')
        plt.subplot(313)
        plt.xlabel('Iteration')
        plt.ylabel('Average Energy')
        plt.plot(arr_iterations, arr_avgEnergy,'k.')
        plt.show()
    
    # Get data for variables
    def collect(self, run, arr_iterations, arr_numAlive, arr_numStarved, arr_numCorpses, arr_numEatenAlive, arr_numCorpsesEaten, arr_avgLength, arr_avgEnergy):
        self.final_arr_numAlive_data[run] = arr_numAlive[-1]
        self.final_arr_numStarved_data[run] = arr_numStarved[-1]
        self.final_arr_numCorpses_data[run] = arr_numCorpses[-1]
        self.final_arr_numEatenAlive_data[run] = arr_numEatenAlive[-1] 
        self.final_arr_numCorpsesEaten_data[run] = arr_numCorpsesEaten[-1]
        self.final_arr_avgLength_data[run] = arr_avgLength[-1]
        self.final_arr_avgEnergy_data[run] = arr_avgEnergy[-1]
        
    # Print and return average for each variable  
    def analyze(self):
        final_numAlive_avg = N.average(self.final_arr_numAlive_data)
        print("Average Final Alive: " + str(final_numAlive_avg))
        
        final_numStarved_avg = N.average(self.final_arr_numStarved_data)
        print("Average Final Starved: " + str(final_numStarved_avg))

        final_numEatenAlive_avg = N.average(self.final_arr_numEatenAlive_data)
        print("Average Final Eaten Alive: " + str(final_numEatenAlive_avg))
        
        final_avgLength_avg = N.average(self.final_arr_avgLength_data)
        print("Average Final Length: " + str(final_avgLength_avg))
        
        final_avgEnergy_avg = N.average(self.final_arr_avgEnergy_data)
        print("Average Final Energy: " + str(final_avgEnergy_avg))
        
        final = (final_numAlive_avg, final_numStarved_avg, final_numEatenAlive_avg, final_avgLength_avg, final_avgEnergy_avg)
        return final
        
