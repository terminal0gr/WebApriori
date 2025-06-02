# Unable to finish even for example2 which is given as an example with thw implementation.

import os
import sys
import json
import math
from eclat_goethal_python.goethal_Eclat_Mall import goethals_Eclat
from time import time
import psutil

datasetName='chess.dat'
minSup=0.945244055068836
separator=' '
# datasetName='FpGrowthSampleWithoutQuotes.txt' 
# minSup=0.6
# separator=','


ext1='_Goethals_Mall_py.fim'
ext2='_Goethals_Mall_py.json'

filepath=os.path.join('datasets', datasetName)

AlgorithmName='Eclat'

eclat=goethals_Eclat(filepath,minSup,separator)
startTime=time()
eclat.mine()
endTime=time()
process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss

outputDict = {}
outputDict['Algorithm']=AlgorithmName
print(f"Algorithm: {AlgorithmName}")
outputDict['library']="Goethal"
print("library: Goethal")
outputDict['minSup']=minSup
outputDict['minSupAbsolute']=minSup
outputDict['totalFI']=eclat.FIM_Count
outputDict['Runtime']=endTime-startTime
outputDict['Memory']=int(round(memoryUSS/(1024*1024),0)) 
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
print(AlgorithmName + " Done!")






