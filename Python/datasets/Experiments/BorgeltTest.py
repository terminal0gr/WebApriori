import os
import sys
import json
import pandas as pd
from time import time
import psutil
from pyfim import eclat


datasetName='T10I4D100K.dat'
minSup=0.01
separator=' '

filepath=os.path.join('datasets', datasetName)


AlgorithmName='Eclat_Borgelt'


# Input data list of lists 
# data = [
#     ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
#     ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
#     ['b', 'f', 'h', 'j', 'o', 'p'],
#     ['b', 'c', 'k', 's', 'p'],
#     ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
# ]

# Read the file, treating each line as a single entry
# creates a list of lists
with open(filepath) as f:
    data = [line.strip().split(sep=separator) for line in f]

startTime=time()
Fiml=[]
FIMs = eclat(data, target='s', supp=minSup, zmin=1, out=Fiml)
endTime=time()

FIMs.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+'.rules'))

process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss

outputDict = {}
outputDict['minSup']=str(minSup)
outputDict['totalFI']=str(len(FIMs))
outputDict['Runtime']=str(endTime-startTime)
outputDict['Memory']=str(memoryUSS)
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close()  
json.dumps(outputDict, indent=4)

