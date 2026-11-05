#Calls carver in a loop to generate n number of possible maps
#
# Authored by Zach Strahan
#

#args to run "python3 maps.py n [Collection Name]"
#n = number of maps to generate
#collection name = string for master directory for all maps

import sys
import os
import subprocess
import shutil
import pathlib

#if (len(sys.argv)<2):
#   print("errors in command args")
#   sys.exit(1)

numMaps = int(sys.argv[1])
#outerDir = sys.argv[2]
PYTHON_INT = sys.executable
processArgs = [PYTHON_INT, 'carver.py', '30', '30', '30', '1', '_', '0']
for i in range(numMaps):
    processArgs[6] = str(i)
    result = subprocess.run(processArgs)
    pathlib.Path("Test_"+str(i)).mkdir(parents=True, exist_ok=True)
    pathlib.Path("Testing_Battery").mkdir(parents=True, exist_ok=True)
    curDir = str(pathlib.Path.cwd())
    dirPath = curDir + ("/Test_"+str(i))
    outerDir = curDir + ("/Testing_Battery")
    stl_File = curDir + ("/Test " + str(i) + ".stl")
    png_file = curDir + ("/Test " + str(i) + ".png")
    shutil.move(stl_File, dirPath)
    shutil.move(png_file, dirPath)
    shutil.move(dirPath, outerDir)