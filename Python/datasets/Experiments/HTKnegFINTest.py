import os
import sys
import json
import psutil

sys.setrecursionlimit(10000)

datasetName='kosarak.dat' 
TopK=100
separator=' '
# datasetName='negFINPaperSample.txt'
# TopK=13
# separator=','


memorySave=False

'''
Call arguments          
1) datasetName  
    The name of the dataset. The program expect to find it in a file named dataset
2) min_Support Value in [0..1] 
3) separator 
    The separator of the dataset For space, write " "
4) memorySave 
    True  -> less memory consuption, a little slower
    False -> more memory consuption, a little quicker
'''
#identity
if len(sys.argv)>1:
    datasetName=str(sys.argv[1])

if len(sys.argv)>2:
    TopK=int(sys.argv[2])

if len(sys.argv)>3:
    separator=str(sys.argv[3])

if len(sys.argv)>4:
    if str(sys.argv[4]) in ['True', 'true', '1']:
        memorySave=True
    else:
        memorySave=False

commitTimeout=0
if len(sys.argv)>5:
    commitTimeout=int(sys.argv[5])


################################
################################
#End of call arguments    
################################
################################



ext1='_Mall_py.fim' 
ext2='_Mall_py.json'

filepath=os.path.join('datasets', datasetName)

############################
AlgorithmName='HTKnegFIN'
from negFIN.HTKnegFIN import HTKnegFIN
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(TopK)+"_"+AlgorithmName+ext1)

algo = HTKnegFIN(filepath, TopK, outFimFilePath, separator, memorySave, commitTimeout)

algo.runAlgorithm()

# Only to sort results in descending order of absolute support value of every itemset
# algo.finalTopK = {k: v for k, v in sorted(algo.finalTopK.items(), key=lambda item: item[1], reverse=True)}
algo.writeFIM(outFimFilePath)

algo.printStats() # just for console output. 

outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="Mall"
outputDict['transactions']=algo.num_of_transactions
outputDict['TopK']=TopK
outputDict['totalFI']=len(algo.finalTopK)
outputDict['Rank']=algo.heap.rankCount()
outputDict['minSup']=algo.min_count
outputDict['minSupAbsolute']=algo.min_count/algo.num_of_transactions
outputDict['total candidates']=algo.num_of_candidate_FI
outputDict['Runtime']=algo.execution_time
outputDict['Memory']=algo.maxMemoryUSS
Top1KItemsets=sum(1 for key in algo.finalTopK if len(key) == 1)
outputDict['Items']=algo.itemCount
outputDict['TopK 1-itemsets']=Top1KItemsets

file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(TopK)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
############################
