import os
import sys
import json


tidSet=True #tidSets (True) mode / diffSets (False)
bitSetMode=True #If bitSet will be used in transformation of the vertical database representation 
commitTimeout=1000

# datasetName='mushroom.dat'  
# topK=70
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
# datasetName='L-0023.csv'
# topK=10000
# separator=';'
# datasetName='pumsb_star.dat'
# topK=10000
# separator=' '
# datasetName='FpGrowthSampleWithoutQuotes.txt'  
# topK=5
# separator=','
# datasetName='T16IT20D100K.dat'
# topK=100
# separator=' '
# datasetName='webdocs.dat'
# topK=100
# separator=' '
# datasetName='HTK-MinerPaperSample.txt'
# topK=10
# separator=' '
# datasetName='SubsumePaperSample.txt'
# topK=10
# separator=' '




'''
Call arguments          
1) datasetName  
    The name of the dataset. The program expect to find it in a file named dataset
2) TopK 
    The number of Top-K frequent itemsets that the user demands 
3) separator 
    The separator of the dataset For space, write " ".
4) tidSet 
    True  -> tidSets  with intersection 
    False -> diffSets with difference 
5) bitSetMode
    True  -> Transform of items transactions to bitsets
    False -> items transactions are represented by integers
6) commitTimeout (overall execution time threshold in seconds) default=0
    if 0 then execution time is unlimited. 
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
        tidSet=True
    else:
        tidSet=False

if len(sys.argv)>5:
    if str(sys.argv[5]) in ['True', 'true', '1']:
        bitSetMode=True
    else:
        bitSetMode=False

if len(sys.argv)>6:
    commitTimeout=int(sys.argv[6])        

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
if tidSet: 
    if bitSetMode:
        AlgorithmName+="_BSN"
    else:
        AlgorithmName+="_TS"
else:
    if bitSetMode:
        AlgorithmName+="_DBSN"
    else:
        AlgorithmName+="_DTS"

from HTKMiner.Code.HTKMiner import HTKMiner
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext1)

# It is vital for the parallel processing
if __name__ == '__main__':
    HTKAlgo = HTKMiner(filepath, topK, separator, tidSet, bitSetMode, commitTimeout)
    HTKAlgo.mine()

    HTKAlgo.writeFIM(outFimFilePath)

    outputDict = {}
    outputDict['Algorithm']=AlgorithmName
    outputDict['Language']="python"
    outputDict['library']="Mall"
    outputDict['minSup']=HTKAlgo.minSup
    outputDict['minSupAbsolute']=HTKAlgo.heap.heapList[-1]
    outputDict['topK']=topK
    outputDict['totalFI']=len(HTKAlgo.finalTopK)
    outputDict['Rank']=HTKAlgo.heap.rankCount()
    Top1KItemsets=sum(1 for key in HTKAlgo.finalTopK if len(key) == 1)
    outputDict['Items']=HTKAlgo.itemCount
    outputDict['TopK 1-itemsets']=Top1KItemsets
    print(f"1-item: {sum(1 for key in HTKAlgo.finalTopK if len(key) == 1)} / {HTKAlgo.itemCount}")

    if HTKAlgo.execution_time>HTKAlgo.commitTimeout:
        outputDict['Runtime']=str(HTKAlgo.commitTimeout)+'+++'
    else:    
        outputDict['Runtime']=HTKAlgo.execution_time
    outputDict['Memory']=HTKAlgo.maxMemoryUSS
    file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext2),'w')
    json.dump(outputDict, file, indent=4)
    file.close() 
    json.dumps(outputDict, indent=4)


    ############################
    print(AlgorithmName + " Done!")
