import os
import sys
import json
import psutil


sparseData=True #tidSets (True) mode / diffSets (False)
bitSetMode=True #If bitSet will be used in transformation of the vertical database representation 

# datasetName='chess.dat'  
# topK=1000
# separator=' '
datasetName='kosarak.dat' 
topK=100
separator=' '
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


'''
Call arguments          
1) datasetName  
    The name of the dataset. The program expect to find it in a file named dataset
2) TopK 
    The number of Top-K frequent itemsets that the user demands 
3) separator 
    The separator of the dataset For space, write " ".
4) sparseData 
    True  -> tidSets  with intersection 
    False -> diffSets with difference 
5) bitSetMode
    True  -> Transform of items transactions to bitsets
    False -> items transactions are represented by integers
'''
#identity
if len(sys.argv)>1:
    datasetName=str(sys.argv[1])

if len(sys.argv)>2:
    topK=int(sys.argv[2])

if len(sys.argv)>3:
    separator=str(sys.argv[3])

if len(sys.argv)>4:
    if str(sys.argv[4]) in ['True', 'true', '1']:
        sparseData=True
    else:
        sparseData=False

if len(sys.argv)>5:
    if str(sys.argv[5]) in ['True', 'true', '1']:
        bitSetMode=True
    else:
        bitSetMode=False

################################
################################
#End of call arguments    
################################
################################



ext1='_Mall_py.fim' 
ext2='_Mall_py.json'

filepath=os.path.join('datasets', datasetName)

############################
AlgorithmName='HTKMiner'
if sparseData: AlgorithmName+="_sp"
else: AlgorithmName+="_df"
if bitSetMode: AlgorithmName+="_bs"
print(sparseData)
print(bitSetMode)
print(AlgorithmName)

from HTKMiner.Code.HTKMiner import HTKMiner
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext1)

TKalgo = HTKMiner(filepath, topK, separator, sparseData, bitSetMode)
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
