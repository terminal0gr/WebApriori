import os
import sys
import json
import psutil



datasetName='chess.dat' 
TopK=100
separator=' '
# datasetName='kosarak.dat' 
# TopK=0.002392924458738467
# separator=' '
# datasetName='accidents.dat' 
# TopK=0.8196999850080692
# separator=' '
# datasetName='pumsb.dat'
# TopK=0.867879133874322
# separator=' '
# datasetName='T10I4D100K.dat'
# TopK=0.00227
# separator=' '
# datasetName='T40I10D100K.dat'
# TopK=0.01303
# separator=' '
# datasetName='L-0023.csv' 
# TopK=0.005296905492054642
# separator=';'
# datasetName='FpGrowthSampleWithoutQuotes.txt' 
# TopK=0.6
# separator=','
# datasetName='T16IT20D100K.dat'
# TopK=0.37865
# separator=' '
# datasetName='webdocs.dat'
# TopK=0.32720459173964384
# separator=' '


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
    TopK=float(sys.argv[2])

if len(sys.argv)>3:
    separator=str(sys.argv[3])

if len(sys.argv)>4:
    if str(sys.argv[4]) in ['True', 'true', '1']:
        memorySave=True
    else:
        memorySave=False

################################
################################
#End of call arguments    
################################
################################



ext1='_Mall_py.fim' 
ext2='_Mall_py.json'

filepath=os.path.join('datasets', datasetName)

############################
AlgorithmName='TK_negFIN'
# from negFIN.neg_fin import NegFIN
from negFIN.TK_negFIN import TK_NegFIN
outFimFilePath=os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(TopK)+"_"+AlgorithmName+ext1)

negFIN = TK_NegFIN(filepath, TopK, outFimFilePath, separator, memorySave)

negFIN.runAlgorithm()

# Only to sort results in descending order of absolute support value of every itemset
negFIN.finalFiDict = {k: v for k, v in sorted(negFIN.finalFiDict.items(), key=lambda item: item[1], reverse=True)}
negFIN.writeFIM(outFimFilePath)

negFIN.printStats() # just for console output. 

outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="Mall"
outputDict['TopK']=TopK
outputDict['totalFI']=negFIN.num_of_frequent_itemsets
outputDict['Runtime']=negFIN.execution_time/1000.
outputDict['Memory']=negFIN.maxMemoryUSS
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(TopK)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
print(AlgorithmName + " Done!")
############################
