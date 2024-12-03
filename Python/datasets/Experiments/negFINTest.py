import os
import sys
import json
import psutil


datasetName='chess.dat' 
minSup=0.9023779724655819
separator=' '
# datasetName='kosarak.dat' 
# minSup=0.022692883
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

ext1='_Aryabarzan_Mall_py.fim' 
ext2='_Aryabarzan_Mall_py.json'

filepath=os.path.join('datasets', datasetName)

############################
AlgorithmName='negFIN'
# from negFIN.neg_fin import NegFIN
from negFIN.negFIN_Mall import NegFIN
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1)
negFIN = NegFIN(filepath, minSup, outFimFilePath, separator, False)
negFIN.runAlgorithm()

process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss

negFIN.printStats() # just for console output. 

outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="Mall"
outputDict['minSup']=minSup
outputDict['totalFI']=negFIN.num_of_frequent_itemsets
outputDict['Runtime']=negFIN.execution_time/1000.
outputDict['Memory']=memoryUSS
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
print(AlgorithmName + " Done!")
############################
