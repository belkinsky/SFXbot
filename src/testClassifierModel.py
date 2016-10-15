import sys
import os
sys.path.append(os.path.dirname(__file__) + "/../pyAudioAnalysis")
from pyAudioAnalysis import audioTrainTest as aT

from sys import argv
import numpy as np
import timeit

def main():
  global filename, Result, P, classNames, winner
  # P: list of probabilities
  Result, P, classNames = aT.fileClassification(filename, "svmModel", "svm")
  winner = np.argmax(P) #pick the result with the highest probability value.

script, filename = argv
isSignificant = 0.8 #try different values.

consumed = timeit.timeit(main, number=1)
print("consumed=", consumed, " s")
# is the highest value found above the isSignificant threshhold? 
if P[winner] > isSignificant :
  print("File: " +filename + " is in category: " + classNames[winner] + ", with probability: " + str(P[winner]))
else :
  print("Can't classify sound: " + str(P))
  print("But: " +filename + " is the winner: " + classNames[winner] + ", with probability: " + str(P[winner]))
