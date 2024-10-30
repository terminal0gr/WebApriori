import os
import sys
import json

datasetName='1base2.csv' 
minSup=0.01
separator=','

filepath=os.path.join('datasets', datasetName)


AlgorithmName='Apriori_PAMI'
from PAMI.frequentPattern.basic import Apriori as PAMI
obj1 = PAMI.Apriori(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close()  
json.dumps(outputDict, indent=4)
# print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
# print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
# print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
# print('Memory (USS): ' + str(obj1.getMemoryUSS()))



AlgorithmName='Apriori_bitset_PAMI'
from PAMI.frequentPattern.basic import Aprioribitset as PAMI
obj1 = PAMI.Aprioribitset(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)



AlgorithmName='Eclat_PAMI'
from PAMI.frequentPattern.basic import ECLAT as PAMI
obj1 = PAMI.ECLAT(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)



AlgorithmName='EclatDiffset_PAMI'
from PAMI.frequentPattern.basic import ECLATDiffset as PAMI
obj1 = PAMI.ECLATDiffset(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)



AlgorithmName='EclatBitset_PAMI'
from PAMI.frequentPattern.basic import ECLATbitset as PAMI
obj1 = PAMI.ECLATbitset(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)



AlgorithmName='FPGrowth_PAMI'
from PAMI.frequentPattern.basic import FPGrowth as PAMI
obj1 = PAMI.FPGrowth(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)



AlgorithmName='FAE_PAMI'
from PAMI.frequentPattern.topk import FAE as PAMI
obj1 = PAMI.FAE(iFile=filepath, k=100, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)

