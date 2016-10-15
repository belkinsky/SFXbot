import sys
import os
sys.path.append(os.path.dirname(__file__) + "/../pyAudioAnalysis")
from pyAudioAnalysis import audioTrainTest as aT
import os
from sys import argv
script, dirname = argv

subdirectories = os.listdir(dirname)
subdirectories.pop(0)

subdirectories = [dirname + "/" + subDirName for subDirName in subdirectories]

print(subdirectories)
aT.featureAndTrain(subdirectories, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svmModel", False)