"""
All Global variables go here
"""
import numpy as N
from imports import*
from Consts import*
from water import water
from Tuna import Tuna
from Globalvars import*




numAlive=0
numCorpses=0
numEatenAlive=0
numCorpsesEaten=0

#2-day array object of water agents
Grid = N.zeros((tankh,tankw))

#list of all existing tuna
tuna=[]