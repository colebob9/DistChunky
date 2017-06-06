"""
DistChunky Client
Python 3
colebob9

java -Dchunky.home="ChunkyFiles" -jar ChunkyLauncher.jar
"""

import os, shutil
import subprocess, shlex

# Config

chunkyJarPath = "ChunkyLauncher.jar"
chunkyFilesPath = "ChunkyFiles"
workerID = "TestClient"

deleteScenesForWorkerDir = True

# Config End

sceneFilesExts = [".dump", ".foliage", ".grass", ".json", ".octree"]
scenesDir = "DC_ScenesForWorkers" + "/" + workerID

chunkySceneFilePath = chunkyFilesPath + "/" + "scenes"

# Detect all scenes in scenesDir
allScenes = []
for file in os.listdir(scenesDir):
    if file.endswith(".json"):
        allScenes.append(os.path.splitext(file)[0])
print("Found Chunky scenes:")
print(allScenes)
print("")

if deleteScenesForWorkerDir:
    if os.path.exists(chunkySceneFilePath):
        print("Deleting Worker Directory...")
        shutil.rmtree(chunkySceneFilePath)

if not os.path.exists(chunkySceneFilePath):
    os.mkdir(chunkySceneFilePath)
    print("Made " + chunkySceneFilePath + " directory.")
    
for scene in allScenes:
    for ext in sceneFilesExts:
        shutil.copy(scenesDir + "/" + scene + ext, chunkyFilesPath + "/" + "scenes" + "/" + scene + ext)

    print('')
    print("Now rendering: " + scene)
    print('')
    subprocess.call(shlex.split("java -Dchunky.home=\"%s\" -jar %s -render %s" % (chunkyFilesPath, chunkyJarPath, scene)))