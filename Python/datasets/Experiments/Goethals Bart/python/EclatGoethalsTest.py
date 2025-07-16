import os
import sys
from EclatGoethalsMall import goethals_Eclat
from time import time
import pandas as pd
import json
import psutil

datasetName='../../datasets/kosarak.dat' 
minSup=0.00634443162741085
separator=' '
# datasetName='../../datasets/L-0023.csv' 
# minSup=0.00529690549205464
# separator=';'

'''
Call arguments          
1) datasetName  
    The name of the dataset. The program expect to find it in a file named dataset
2) min_Support Value in [0..1] 
3) separator 
    The separator of the dataset For space, write " "
'''
#identity
if len(sys.argv)>1:
    datasetName=str(sys.argv[1])

if len(sys.argv)>2:
    minSup=float(sys.argv[2])

if len(sys.argv)>3:
    separator=str(sys.argv[3])

AlgorithmName='Eclat'
ext1='_Goethals_py.fim'
ext2='_Goethals_py.json'

startTime=time()
process = psutil.Process(os.getpid()) # Needed to measure memory

Algo = goethals_Eclat(datasetName, minSup, separator)
Algo.memoryUSS=0 #Memory initialization
Algo.mine()

# End time
endTime=time()

# Memory measurement only there...
m=process.memory_full_info().uss
if Algo.memoryUSS < m:
    Algo.memoryUSS=m

# output frequentPatterns
# frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# results

# Statistics
outputDict = {} 
outputDict['dataset']=datasetName
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="Goethals"
outputDict['minSup']=minSup
outputDict['totalFI']=Algo.FIM_Count    
outputDict['Runtime']=round(endTime-startTime,2)
outputDict['Memory']=round(Algo.memoryUSS/(1024*1024))
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close()  
print(json.dumps(outputDict, indent=4))
print(AlgorithmName + " Done!")