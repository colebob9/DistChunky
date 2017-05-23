"""
DistChunky SceneSplitter
Python 3
colebob9

This script takes scene files in a "scenes" directory and splits them up based on any benchmark score.

TODO:
Add messages for copying files
Some extra tweaks to calculating SSP if the benchmark scores are too far from each other
Tweak messages
"""

import json
import math
import operator
import os, shutil
from collections import OrderedDict

# Config

sceneName = "ChunkyTest"
scenesDir = "scenes/"

scenesForWorkersDir = "DC_ScenesForWorkers"
deleteScenesForWorkersDir = True

benchmarkResults = {"i7-4790K": 11197, "Pentium G645": 2598, "i5-4690": 7599, "TestClient": 432} # <- actual benchmarks
#benchmarkResults = {"i7-4790K": 432, "Pentium G645": 543, "i5-4690": 674} # <- made up tests


# End Config

#
# Reading JSON and figuring out SSP for each computer.
#
print("[Chunky Scene Info:] ")
sceneJsonFile = scenesDir + sceneName + ".json"

with open(sceneJsonFile, 'r') as f:
    data = json.load(f)
    sspTarget = data["sppTarget"]
    print("SPP Target: " + str(sspTarget))
    
print("")

added = 0
print("[Benchmark results:] ")
# Add all benchmark results together
for key, value in benchmarkResults.items():
    print(key + ": " + str(value))
    added = value + added
    
print("Added: " + str(added))
print("")

# Convert into a percentage
benchmarkResultsPercentage = {}
for key, value in benchmarkResults.items():
    benchmarkResultsPercentage[key] = value / added
print("Percentages: " + str(benchmarkResultsPercentage))

benchmarkResultsSSP = {}
for key, value in benchmarkResultsPercentage.items():
    sspCalc = sspTarget * value
    benchmarkResultsSSP[key] = int(round(sspCalc, 0))
    
    
print("SSP Estimations: " + str(benchmarkResultsSSP))
sspAdded = 0
for key, value in benchmarkResultsSSP.items():
    sspAdded = value + sspAdded
print("Added up: " + str(sspAdded))

if not sspAdded == sspTarget:
    maxSSPKey = max(benchmarkResults.items(), key=operator.itemgetter(1))[0]
    maxSSPValue = benchmarkResultsSSP.get(maxSSPKey)
    sspCorrection = sspTarget - sspAdded
    print("Giving " + maxSSPKey + " " + str(sspCorrection) + " more SSP.")
    benchmarkResultsSSP[maxSSPKey] = maxSSPValue + sspCorrection
    print(maxSSPKey + " will now render " + str(benchmarkResultsSSP[maxSSPKey]) + " SSP.")
    
    sspAdded = 0
    for key, value in benchmarkResultsSSP.items():
        sspAdded = value + sspAdded
    print("Added up: " + str(sspAdded))
    
# Check that numbers are the same
if not sspAdded == sspTarget:
    print("Something went wrong, the numbers dont add up right.\nReport this as an issue on GitHub please.")
    print(sspAdded, "=/=", sspTarget)
    exit()
    
#
# Splitting scene file into separate scenes for each PC
#

if deleteScenesForWorkersDir:
    if os.path.exists(scenesForWorkersDir):
        print("Deleting Workers Directory...")
        shutil.rmtree(scenesForWorkersDir)

# Creating worker directories and copy files


if not os.path.exists(scenesForWorkersDir):
    os.mkdir(scenesForWorkersDir)
    print("Made " + scenesForWorkersDir + " directory.")

sceneFilesExts = [".dump", ".foliage", ".grass", ".json", ".octree"]
for key, value in benchmarkResultsSSP.items():
    for f in sceneFilesExts:
        workerSceneDir = scenesForWorkersDir + "/" + str(key)
        if not os.path.exists(workerSceneDir):
            os.mkdir(workerSceneDir)
            print("Made " + workerSceneDir + " directory.")
        shutil.copy(scenesDir + sceneName + f, workerSceneDir)

    # Edit json files
    workerScene = workerSceneDir + "/" + sceneName + ".json"
    with open(workerScene, 'r') as json_file:
        workerJson = json.load(json_file, object_pairs_hook=OrderedDict)
        
        workerJson["sppTarget"] = value
        with open(workerScene, 'w') as json_file:
            json.dump((workerJson), json_file, sort_keys=False, indent=2)
        print("Wrote for: " + key)
    