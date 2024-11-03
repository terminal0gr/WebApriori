import os
import sys
import json



# datasetName='chess.dat' 
# minSup=0.8
# separator=' '
datasetName='FpGrowthSampleWithoutQuotes.txt' 
minSup=0.6
separator=','

filepath=os.path.join('datasets', datasetName)


data = [
    ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
    ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
    ['b', 'f', 'h', 'j', 'o', 'p'],
    ['b', 'c', 'k', 's', 'p'],
    ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
]


# AlgorithmName='Eclat_PAMI'
# from PAMI.frequentPattern.basic import ECLAT as PAMI
# obj1 = PAMI.ECLAT(iFile=filepath, minSup=minSup, sep=separator)
# # obj1 = PAMI.ECLAT(data, minSup=minSup, sep=separator)
# obj1.mine(False)
# frequentPatternsDF= obj1.getPatternsAsDataFrame()
# frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+'.rules'))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['totalFI']=str(len(frequentPatternsDF))
# outputDict['Runtime']=str(obj1.getRuntime())
# outputDict['Memory']=str(obj1.getMemoryUSS())
# ext='.json'
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)

# AlgorithmName='Eclat_PAMI_ms'
# from PAMI.frequentPattern.basic import ECLAT as PAMI
# obj1 = PAMI.ECLAT(iFile=filepath, minSup=minSup, sep=separator)
# # obj1 = PAMI.ECLAT(data, minSup=minSup, sep=separator)
# obj1.mine(True)
# frequentPatternsDF= obj1.getPatternsAsDataFrame()
# frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+'.rules'))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['totalFI']=str(len(frequentPatternsDF))
# outputDict['Runtime']=str(obj1.getRuntime())
# outputDict['Memory']=str(obj1.getMemoryUSS())
# ext='.json'
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)




# AlgorithmName='EclatDiffset_PAMI'
# from PAMI.frequentPattern.basic import ECLATDiffset as PAMI
# obj1 = PAMI.ECLATDiffset(iFile=filepath, minSup=minSup, sep=separator)
# # from editedCode.PAMIECLATDiffset import ECLATDiffset as PAMIedited
# # obj1 = PAMIedited.ECLATDiffset(data, minSup=minSup, sep=separator)
# obj1.mine()
# frequentPatternsDF= obj1.getPatternsAsDataFrame()
# frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+'.rules'))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['totalFI']=str(len(frequentPatternsDF))
# outputDict['Runtime']=str(obj1.getRuntime())
# outputDict['Memory']=str(obj1.getMemoryUSS())
# ext='.json'
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)



AlgorithmName='EclatBitset_PAMI'
from PAMI.frequentPattern.basic import ECLATbitset as PAMI
obj1 = PAMI.ECLATbitset(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)



AlgorithmName='FPGrowth_PAMI'
from PAMI.frequentPattern.basic import FPGrowth as PAMI
obj1 = PAMI.FPGrowth(iFile=filepath, minSup=minSup, sep=separator)
obj1.mine()
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+'.rules'))
# print(frequentPatternsDF)
outputDict = {}
outputDict['totalFI']=str(len(frequentPatternsDF))
outputDict['Runtime']=str(obj1.getRuntime())
outputDict['Memory']=str(obj1.getMemoryUSS())
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)



