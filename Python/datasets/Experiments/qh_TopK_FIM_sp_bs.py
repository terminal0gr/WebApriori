import os
import json
import psutil


sparseData=False #tidSets (True) mode instead of diffSets (False)
bitSetMode=False #If bitSet will be used in transformation of the vertical database representation 

datasetName='chess.dat'  
topK=10000
separator=' '
# datasetName='kosarak.dat' 
# topK=100
# separator=' '
# datasetName='accidents.dat' 
# topK=100
# separator=' '
# datasetName='T10I4D100K.dat'
# topK=1000
# separator=' '
# datasetName='1_L-0023.csv'
# topK=1000
# separator=';'
# datasetName='FpGrowthSampleWithoutQuotes.txt'  
# topK=5
# separator=','




# datasetName='1_L-0023.csv' 
# minSup=0.01
# separator=';'
# datasetName='FpGrowthSampleWithoutQuotes.txt' 
# minSup=0.6
# separator=','
# datasetName='negFINPaperSample.txt' 
# minSup=0.4
# separator=','

ext1='_Mall_py.fim' 
ext2='_Mall_py.json'

filepath=os.path.join('datasets', datasetName)

############################
AlgorithmName='HTK'
if sparseData: AlgorithmName+="_sp"
else: AlgorithmName+="_df"
if bitSetMode: AlgorithmName+="_bs"

from Python.datasets.Experiments.qh_TopK_FIM.Code.HTKMiner import qh_TopK_FIM
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext1)

TKalgo = qh_TopK_FIM(filepath, topK, separator, sparseData, bitSetMode)
TKalgo.mine()

process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss

TKalgo.writeFIM(outFimFilePath)

outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="Mall"
outputDict['minSup']=TKalgo.minSup
outputDict['totalFI']=len(TKalgo.finalTopK)
outputDict['Runtime']=TKalgo.execution_time
outputDict['Memory']=memoryUSS
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
print(f"Memory:{memoryUSS}")
print(AlgorithmName + " Done!")
############################
