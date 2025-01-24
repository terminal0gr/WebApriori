import os
import sys
import json


commitTimeout=300

datasetName='chess.dat'  
topK= 1000
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
datasetName='L-0023.csv'
topK=92
separator=';'
# datasetName='BTKSample.dat'  
# topK=25
# separator=' '

sys.setrecursionlimit(10000)


'''
Call arguments          
1) datasetName  
    The name of the dataset. The program expect to find it in a file named dataset
2) TopK 
    The number of Top-K Rank frequent itemsets that the user demands 
3) separator 
    The separator of the dataset For space, write " ".
4) commitTimeout (overall execution time threshold in seconds) default=0
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
    commitTimeout=int(sys.argv[4])        

################################
################################
#End of call arguments    
################################
################################



ext1='_Mall_py.fim' 
ext2='_Mall_py.json'

filepath=os.path.join('datasets', datasetName)

############################
AlgorithmName='BTK'

from BTK.BTK import BTK
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext1)


BTKAlgo = BTK(filepath, topK, separator, commitTimeout)
if BTKAlgo.mine()!=1:

    BTKAlgo.writeFIM(outFimFilePath)

    outputDict = {}
    outputDict['Algorithm']=AlgorithmName
    outputDict['Language']="python"
    outputDict['library']="Mall"
    outputDict['minSup']=BTKAlgo.minSup
    outputDict['totalFI']=BTKAlgo.finalTopK
    if BTKAlgo.execution_time>BTKAlgo.commitTimeout:
        outputDict['Runtime']=str(BTKAlgo.commitTimeout)+'+++'
    else:    
        outputDict['Runtime']=BTKAlgo.execution_time
    outputDict['Memory']=BTKAlgo.maxMemoryUSS
    file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(topK)+"_"+AlgorithmName+ext2),'w')
    json.dump(outputDict, file, indent=4)
    file.close() 
    ############################
    print(AlgorithmName + " Done!")
else:    
    print(AlgorithmName + " Failed!")
