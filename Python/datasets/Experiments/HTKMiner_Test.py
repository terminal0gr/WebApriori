import os
import sys
import json


sparseData=True #tidSets (True) mode / diffSets (False)
bitSetMode=True #If bitSet will be used in transformation of the vertical database representation 
commitTimeout=300

datasetName='chess.dat'  
topK=1000
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
# datasetName='T16IT20D100K.dat'
# topK=1000
# separator=' '


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
        sparseData=True
    else:
        sparseData=False

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
if sparseData: AlgorithmName+="_sp"
else: AlgorithmName+="_df"
if bitSetMode: AlgorithmName+="_bs"

from HTKMiner.Code.HTKMiner import HTKMiner
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext1)

# It is vital for the parallel processing
if __name__ == '__main__':
    HTKAlgo = HTKMiner(filepath, topK, separator, sparseData, bitSetMode, commitTimeout)
    HTKAlgo.mine()

    HTKAlgo.writeFIM(outFimFilePath)

    outputDict = {}
    outputDict['Algorithm']=AlgorithmName
    outputDict['Language']="python"
    outputDict['library']="Mall"
    outputDict['minSup']=HTKAlgo.minSup
    outputDict['topK']=topK
    outputDict['totalFI']=len(HTKAlgo.finalTopK)
    outputDict['Rank']=HTKAlgo.heap.rankCount()
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
