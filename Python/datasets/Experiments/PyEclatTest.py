# Unable to finish even for example2 which is given as an example with thw implementation.

import os
import sys
import json
import pandas as pd
from pyECLAT import ECLAT
from time import time
import psutil

datasetName='T10I4D100K.dat'
minSup=0.01
separator=' '

filepath=os.path.join('datasets', datasetName)


AlgorithmName='Eclat_pyECLAT'

from pyECLAT import Example1, Example2
# dataframe = Example1().get()
dataframe = Example2().get()

# Read the file, treating each line as a single entry
# with open(filepath) as f:
#     data = [line.strip().split(sep=separator) for line in f]
# Convert data to a DataFrame, where each row is a list of items
# dataframe = pd.DataFrame(data)
# dataframe = pd.read_csv(filepath, sep=separator, header=None ) #nOT WORKING PROPERLY IN 1-mbl TYPE

startTime=time()
eclat_instance = ECLAT(data=dataframe, verbose=False) #verbose=True to see the loading bar
eclat_instance.df_bin   #generate a binary dataframe, that can be used for other analyzes.
eclat_instance.uniq_    #a list with all the names of the different items
get_ECLAT_indexes, get_ECLAT_supports = eclat_instance.fit(min_support=0.01,
                                                           min_combination=1,
                                                           max_combination=3,
                                                           separator=',',
                                                           verbose=False)
endTime=time()
process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss

outputDict = {}
outputDict['totalFI']=str(len(get_ECLAT_indexes))
outputDict['Runtime']=str(endTime-startTime)
outputDict['Memory']=str(memoryUSS)
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close()  
json.dumps(outputDict, indent=4)

print(get_ECLAT_indexes)
print(len(get_ECLAT_indexes))
print(get_ECLAT_supports)

# process = _ab._psutil.Process(_ab._os.getpid())
# self._endTime = _ab._time.time()
# self._memoryUSS = float()
# self._memoryRSS = float()
# self._memoryUSS = process.memory_full_info().uss
# self._memoryRSS = process.memory_info().rss





