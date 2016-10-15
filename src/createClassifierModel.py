import sys
import os
SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(SCRIPT_DIR + "/../pyAudioAnalysis")
from pyAudioAnalysis import audioTrainTest as aT
import os
from sys import argv

dirname = SCRIPT_DIR + "/../data/training"
script, model_type = argv
model_filename = SCRIPT_DIR + "/../data/" + model_type

subdirectories = os.listdir(dirname)
subdirectories.pop(0)

subdirectories = [dirname + "/" + subDirName for subDirName in subdirectories]

print(subdirectories)
aT.featureAndTrain(subdirectories, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, model_type, model_filename, False)