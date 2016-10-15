import sys
import os
SCRIPT_DIR = os.path.dirname(__file__)

sys.path.append(SCRIPT_DIR + "/../pyAudioAnalysis")
from pyAudioAnalysis import audioTrainTest as aT

from sys import argv
import numpy as np
import timeit

def main(argv):
  global filename, Result, P, classNames, winner
  script, model_type, filename = argv
  isSignificant = 0.8 #try different values.

  model_filename = SCRIPT_DIR + "/../data/" + model_type

  Result, P, classNames = aT.fileClassification(filename, model_filename, model_type)
  winner = np.argmax(P) #pick the result with the highest probability value.

  # is the highest value found above the isSignificant threshhold?
  if P[winner] > isSignificant :
    print("File: " +filename + " is in category: " + classNames[winner] + ", with probability: " + str(P[winner]))
  else :
    print("Can't classify sound: " + str(P))
    print("But: " +filename + " is the winner: " + classNames[winner] + ", with probability: " + str(P[winner]))

print(argv)
main(argv)
