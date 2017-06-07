"""
DistChunky SceneSplitter
Python 3
colebob9

This script takes scene files in a "scenes" directory and splits them up based on benchmark scores.

TODO:
Some extra tweaks to calculating SSP if the benchmark scores are too far from each other
Factor in already rendered SSP
put benchmark results into another config file to use across scripts
"""

import json
import math
import os, shutil
from collections import OrderedDict

print("")
print("DistChunky SceneSplitter")
print("")

# Config

scenesDir = "scenes/"

scenesForWorkersDir = "DC_ScenesForWorkers"
deleteScenesForWorkersDir = True

benchmarkResults = {"i7-4790K": 11197, "Pentium G645": 2598, "i5-4690": 7599, "TestClient": 432} # <- actual benchmarks
#benchmarkResults = {"i7-4790K": 432, "Pentium G645": 543, "i5-4690": 674} # <- made up tests


# End Config


# Detect all scenes in scenesDir
allScenes = []
for file in os.listdir(scenesDir):
    if file.endswith(".json"):
        allScenes.append(os.path.splitext(file)[0])
print("Found Chunky scenes:")
print(allScenes)
print("")

# Add all benchmark results together
added = 0
print("[Benchmark results:] ")
for key, value in benchmarkResults.items():
    print(key + ": " + str(value))
    added = value + added
    
print("Added: " + str(added))
print("")

# Convert into a percentage
benchmarkResultsPercentage = {}
for key, value in benchmarkResults.items():
    benchmarkResultsPercentage[key] = value / added
print("Calculated Percentages: " + str(benchmarkResultsPercentage))
print("")

# Deleting ScenesForWorkersDir
if deleteScenesForWorkersDir:
    if os.path.exists(scenesForWorkersDir):
        print("Deleting Workers Directory...")
        shutil.rmtree(scenesForWorkersDir)

for scene in allScenes:
    # Create ScenesForWorkersDirs
    if not os.path.exists(scenesForWorkersDir):
        os.mkdir(scenesForWorkersDir)
        print("Made " + scenesForWorkersDir + " directory.")

    #
    # Reading JSON and figuring out SSP for each computer.
    #
    print("\n[Chunky Scene Info:] ")
    sceneJsonFile = scenesDir + scene + ".json"

    print("Scene: " + scene)
    with open(sceneJsonFile, 'r') as f:
        data = json.load(f)
        sspTarget = data["sppTarget"]
        print("SPP Target: " + str(sspTarget))

    benchmarkResultsSSP = {}
    for key, value in benchmarkResultsPercentage.items():
        sspCalc = sspTarget * value
        benchmarkResultsSSP[key] = int(round(sspCalc, 0))
        
    # Create SSP Estimations
    print("SSP Estimations: " + str(benchmarkResultsSSP))
    sspAdded = 0
    for key, value in benchmarkResultsSSP.items():
        sspAdded = value + sspAdded
    #print("Added up: " + str(sspAdded)) # for testing that all workers have the same amount of SSP all together

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
    print("")

    # Copy files

    sceneFilesExts = [".dump", ".foliage", ".grass", ".json", ".octree", ".dump.backup", ".json.backup"]
    for key, value in benchmarkResults.items():
        for f in sceneFilesExts:
            workerSceneDir = scenesForWorkersDir + "/" + str(key)
            if not os.path.exists(workerSceneDir):
                os.mkdir(workerSceneDir)
                print("Made " + workerSceneDir + " directory.")
                
            if not os.path.isfile(scenesDir + scene + f): # check that if backup scene files exist
                pass
            else:
                shutil.copy(scenesDir + scene + f, workerSceneDir)
                print("Copied: " + scenesDir + scene + f + " to " + workerSceneDir + "/" + scene + f)

    # Edit json files
    workerScene = workerSceneDir + "/" + scene + ".json"
    with open(workerScene, 'r') as json_file:
        workerJson = json.load(json_file, object_pairs_hook=OrderedDict)
        
        workerJson["sppTarget"] = value
        with open(workerScene, 'w') as json_file:
            json.dump((workerJson), json_file, sort_keys=False, indent=2)
        print("Split scene \"" + scene + "\" for worker \"" + key + "\"" + "\n")
        