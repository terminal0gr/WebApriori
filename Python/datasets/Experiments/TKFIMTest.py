import os
import sys
import json
import psutil


datasetName='chess.dat' 
topK=100
separator=' '
# datasetName='kosarak.dat' 
# topK=100
# separator=' '


# datasetName='1_L-0023.csv' 
# minSup=0.01
# separator=';'
# datasetName='FpGrowthSampleWithoutQuotes.txt' 
# minSup=0.6
# separator=','
# datasetName='negFINPaperSample.txt' 
# minSup=0.4
# separator=','

ext1='_Iqbal_Mall_py.fim' 
ext2='_Iqbal_Mall_py.json'

filepath=os.path.join('datasets', datasetName)

############################
AlgorithmName='TKFIM'
from TKFIM.Code.TKFIM_Mall import TKFIM
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext1)
TKalgo = TKFIM(filepath, topK, separator)
TKalgo.readDatasetFile()
TKalgo.mine()

process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss

TKalgo.writeFIM(outFimFilePath)

outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="Mall"
outputDict['minSup']=TKalgo.minSup
outputDict['totalFI']=TKalgo.topK
outputDict['Runtime']=TKalgo.execution_time/1000.
outputDict['Memory']=memoryUSS
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
print(AlgorithmName + " Done!")
############################
