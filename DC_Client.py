"""
DistChunky Client
Python 3
colebob9

java -Dchunky.home="ChunkyFiles" -jar ChunkyLauncher.jar
"""

import subprocess, shlex

# Config

chunkyJarPath = "ChunkyLauncher.jar"
chunkyFilesPath = "ChunkyFiles"
sceneName = "ChunkyTest"

deleteScenesForWorkerDir = True

# Config End


import os, shutil

sceneFilesExts = [".dump", ".foliage", ".grass", ".json", ".octree"]
scenesForWorkersDir = "DC_ScenesForWorkers"
workerID = "TestClient"
chunkySceneFilePath = chunkyFilesPath + "/" + "scenes"


if deleteScenesForWorkerDir:
    if os.path.exists(chunkySceneFilePath):
        print("Deleting Worker Directory...")
        shutil.rmtree(chunkySceneFilePath)



if not os.path.exists(chunkySceneFilePath):
    os.mkdir(chunkySceneFilePath)
    print("Made " + chunkySceneFilePath + " directory.")

for ext in sceneFilesExts:
    shutil.copy(scenesForWorkersDir + "/" + workerID + "/" + sceneName + ext, chunkyFilesPath + "/" + "scenes" + "/" + sceneName + ext)


print("Starting Chunky Process!")
subprocess.call(shlex.split("java -Dchunky.home=\"%s\" -jar %s -render %s" % (chunkyFilesPath, chunkyJarPath, sceneName)))