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
# datasetName='1_L-0023.csv' 
# minSup=0.01
# separator=';'

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
with open(filepath,encoding='utf-8-sig') as f:
    data = [line.strip().split(sep=separator) for line in f]

startTime=time()
Fiml=[]
FIMs = eclat(data, target='s', supp=minSup, zmin=1, out=Fiml)
endTime=time()

# FIMs sample
# list of tuples with each tuple to have:
# 1) A tuple of frequent items as the first element
# 2) The support of FIM as the second element.
# [
#     (('a',), 36),
#     (('b','c'), 42),
#     (('d',), 5)
# ]

# Specify the output file path
output_file = os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1)
# Open the file for writing
with open(output_file, 'w') as f:
    # Iterate over each item in the list
    for item, count in FIMs:
        # Join the elements of the inner tuple with a semicolon if there are multiple
        line = ';'.join(item) + ',' + str(count)
        # Write the line to the file
        f.write(line + '\n')

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

