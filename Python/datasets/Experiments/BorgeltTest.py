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


# Read the file, treating each line as a single entry
with open(filepath) as f:
    data = [line.strip().split(sep=separator) for line in f]
# Convert data to a DataFrame, where each row is a list of items
# dataframe = pd.DataFrame(data)
# dataframe = pd.read_csv(filepath, sep=separator, header=None ) #nOT WORKING PROPERLY IN 1-mbl TYPE

startTime=time()
FIMs = eclat(data, target='s', supp=minSup, zmin=1)
endTime=time()
process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss

# outputDict = {}
# outputDict['totalFI']=str(len(get_ECLAT_indexes))
# outputDict['Runtime']=str(endTime-startTime)
# outputDict['Memory']=str(memoryUSS)
# ext='.json'
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
# json.dump(outputDict, file, indent=4)
# file.close()  
# json.dumps(outputDict, indent=4)

