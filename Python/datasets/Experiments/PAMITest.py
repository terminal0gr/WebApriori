import os
import sys
import json


datasetName='chess.dat' 
minSup=0.5
separator=' '
# datasetName='1_L-0023.csv' 
# minSup=0.01
# separator=';'
# datasetName='FpGrowthSampleWithoutQuotes.txt' 
# minSup=0.6
# separator=','

ext1='_PAMI.fim'
ext2='_PAMI.json'



# data = [
#     ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
#     ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
#     ['b', 'f', 'h', 'j', 'o', 'p'],
#     ['b', 'c', 'k', 's', 'p'],
#     ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
# ]

filepath=os.path.join('datasets', datasetName)



############################
AlgorithmName='Apriori_TID_bitset'
from PAMI.frequentPattern.basic import Aprioribitset as PAMI
obj1 = PAMI.Aprioribitset(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine(False)
frequentPatterns= obj1.getPatternsAsDataFrame()
frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# print(frequentPatternsDF)
outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="PAMI"
outputDict['minSup']=minSup
outputDict['totalFI']=len(frequentPatterns)
outputDict['Runtime']=obj1.getRuntime()
outputDict['Memory']=obj1.getMemoryUSS()
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
############################

############################
AlgorithmName='Eclat_bitset'
from PAMI.frequentPattern.basic import ECLATbitset as PAMI
obj1 = PAMI.ECLATbitset(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine(False)
frequentPatterns= obj1.getPatternsAsDataFrame()
frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# print(frequentPatternsDF)
outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="PAMI"
outputDict['minSup']=minSup
outputDict['totalFI']=len(frequentPatterns)
outputDict['Runtime']=obj1.getRuntime()
outputDict['Memory']=obj1.getMemoryUSS()
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
############################



############################
AlgorithmName='FPGrowth'
from PAMI.frequentPattern.basic import FPGrowth as PAMI
obj1 = PAMI.FPGrowth(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
frequentPatterns= obj1.getPatternsAsDataFrame()
frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
outputDict = {}
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="PAMI"
outputDict['minSup']=minSup
outputDict['totalFI']=len(frequentPatterns)
outputDict['Runtime']=obj1.getRuntime()
outputDict['Memory']=obj1.getMemoryUSS()
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
############################

# ############################
# AlgorithmName='Eclat'
# from PAMI.frequentPattern.basic import ECLAT as PAMI
# obj1 = PAMI.ECLAT(iFile=filepath, minSup=minSup, sep=separator)
# obj1.mine(False)
# frequentPatterns= obj1.getPatternsAsDataFrame()
# frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['Algorithm']=AlgorithmName
# outputDict['Language']="python"
# outputDict['library']="PAMI"
# outputDict['minSup']=minSup
# outputDict['totalFI']=len(frequentPatterns)
# outputDict['Runtime']=obj1.getRuntime()
# outputDict['Memory']=obj1.getMemoryUSS()
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)
# ############################

# ############################
# AlgorithmName='Apriori'
# from PAMI.frequentPattern.basic import Apriori as PAMI
# obj1 = PAMI.Apriori(iFile=filepath, minSup=minSup, sep=separator)
# obj1.mine(False)
# frequentPatterns= obj1.getPatternsAsDataFrame()
# frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['Algorithm']=AlgorithmName
# outputDict['Language']="python"
# outputDict['library']="PAMI"
# outputDict['minSup']=minSup
# outputDict['totalFI']=len(frequentPatterns)
# outputDict['Runtime']=obj1.getRuntime()
# outputDict['Memory']=obj1.getMemoryUSS()
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)
# ############################

# ############################
# AlgorithmName='DEclat'
# from PAMI.frequentPattern.basic import ECLATDiffset as PAMI
# obj1 = PAMI.ECLATDiffset(iFile=filepath, minSup=minSup, sep=separator)
# # from editedCode.PAMIECLATDiffset import ECLATDiffset as PAMIedited
# # obj1 = PAMIedited.ECLATDiffset(data, minSup=minSup, sep=separator)
# obj1.mine()
# frequentPatterns= obj1.getPatternsAsDataFrame()
# frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['Algorithm']=AlgorithmName
# outputDict['Language']="python"
# outputDict['library']="PAMI"
# outputDict['minSup']=minSup
# outputDict['totalFI']=len(frequentPatterns)
# outputDict['Runtime']=obj1.getRuntime()
# outputDict['Memory']=obj1.getMemoryUSS()
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)
# ############################