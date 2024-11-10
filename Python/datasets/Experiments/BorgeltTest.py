import os
import sys
import json
import pandas as pd
from time import time
import psutil
from pyfim import eclat


datasetName='chess.dat'
minSup=0.8
separator=' '

ext1='_Borgelt.fim'
ext2='_Borgelt.json'


filepath=os.path.join('datasets', datasetName)




# Input data list of lists 
# data = [
#     ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
#     ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
#     ['b', 'f', 'h', 'j', 'o', 'p'],
#     ['b', 'c', 'k', 's', 'p'],
#     ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
# ]

AlgorithmName='Eclat'
# Read the file, treating each line as a single entry
# creates a list of lists
with open(filepath) as f:
    data = [line.strip().split(sep=separator) for line in f]

startTime=time()
Fiml=[]
FIMs = eclat(data, target='s', supp=minSup, zmin=1, out=Fiml)
endTime=time()

# FIMs.to_csv(os.path.join(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))

process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss

outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="Borgelt"
outputDict['minSup']=minSup
outputDict['totalFI']=len(FIMs)
outputDict['Runtime']=endTime-startTime
outputDict['Memory']=memoryUSS
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close()  
json.dumps(outputDict, indent=4)

