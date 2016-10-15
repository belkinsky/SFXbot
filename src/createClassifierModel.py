import sys
import os
SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(SCRIPT_DIR + "/../pyAudioAnalysis")
from pyAudioAnalysis import audioTrainTest as aT
import os
from sys import argv

dirname = SCRIPT_DIR + "/../data/training/"
script, model_type = argv
model_filename = SCRIPT_DIR + "/../data/" + model_type

entries = os.listdir(dirname)
print("all entries: ", entries)
subdirectories = [i for i in entries if os.path.isdir(dirname+i)]
print("dirs only: ",subdirectories)

subdirectories = [dirname + subDirName for subDirName in subdirectories]

print("final dirs: ", subdirectories)
aT.featureAndTrain(subdirectories, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, model_type, model_filename, False)