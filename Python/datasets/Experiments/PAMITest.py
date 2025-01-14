import os
import sys
import json


# datasetName='chess.dat' 
# minSup=0.886107634543179
# separator=' '
# datasetName='kosarak.dat' 
# minSup=0.002392924458738467
# separator=' '
# datasetName='1_L-0023.csv' 
# minSup=0.01
# separator=';'
# datasetName='FpGrowthSampleWithoutQuotes.txt' 
# minSup=0.6
# separator=','
datasetName='L-0023.csv' 
minSup=0.005296905492054642
separator=';'
# datasetName='BTKSample.dat'  
# topK=0.8
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
    minSup=float(sys.argv[2])

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


ext1='_PAMI_py.fim'
ext2='_PAMI_py.json'



# data = [
#     ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
#     ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
#     ['b', 'f', 'h', 'j', 'o', 'p'],
#     ['b', 'c', 'k', 's', 'p'],
#     ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
# ]

filepath=os.path.join('datasets', datasetName)



############################
# AlgorithmName='Apriori_TID_bitset'
# from PAMI.frequentPattern.basic import Aprioribitset as PAMI
# obj1 = PAMI.Aprioribitset(iFile=filepath, minSup=minSup, sep=separator)
# obj1.mine(False)
# # frequentPatterns= obj1.getPatternsAsDataFrame()
# # frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['Algorithm']=AlgorithmName
# outputDict['Language']="python"
# outputDict['library']="PAMI"
# outputDict['minSup']=minSup
# outputDict['totalFI']=len(obj1._finalPatterns.items())
# outputDict['Runtime']=obj1.getRuntime()
# outputDict['Memory']=obj1.getMemoryUSS()
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)
# print(AlgorithmName + " Done!")
############################

############################
# AlgorithmName='Eclat_bitset'
# from PAMI.frequentPattern.basic import ECLATbitset as PAMI
# obj1 = PAMI.ECLATbitset(iFile=filepath, minSup=minSup, sep=separator)
# obj1.mine(memorySave)
# frequentPatterns= obj1.getPatternsAsDataFrame()
# frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# print(frequentPatterns)
# outputDict = {}
# outputDict['Algorithm']=AlgorithmName
# outputDict['Language']="python"
# outputDict['library']="PAMI"
# outputDict['minSup']=minSup
# outputDict['totalFI']=len(obj1._finalPatterns.items())
# outputDict['Runtime']=obj1.getRuntime()
# outputDict['Memory']=obj1.getMemoryUSS()
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)
# print(AlgorithmName + " Done!")
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
outputDict['totalFI']=len(obj1._finalPatterns.items())
outputDict['Runtime']=obj1.getRuntime()
outputDict['Memory']=obj1.getMemoryUSS()
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
json.dump(outputDict, file, indent=4)
file.close() 
json.dumps(outputDict, indent=4)
print(AlgorithmName + " Done!")
############################

# ############################
# AlgorithmName='Eclat'
# from PAMI.frequentPattern.basic import ECLAT as PAMI
# obj1 = PAMI.ECLAT(iFile=filepath, minSup=minSup, sep=separator)
# obj1.mine(False)
# # frequentPatterns= obj1.getPatternsAsDataFrame()
# # frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['Algorithm']=AlgorithmName
# outputDict['Language']="python"
# outputDict['library']="PAMI"
# outputDict['minSup']=minSup
# outputDict['totalFI']=len(obj1._finalPatterns.items())
# outputDict['Runtime']=obj1.getRuntime()
# outputDict['Memory']=obj1.getMemoryUSS()
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)
# print(AlgorithmName + " Done!")
# ############################

# ############################
# AlgorithmName='Apriori'
# from PAMI.frequentPattern.basic import Apriori as PAMI
# obj1 = PAMI.Apriori(iFile=filepath, minSup=minSup, sep=separator)
# obj1.mine(False)
# # frequentPatterns= obj1.getPatternsAsDataFrame()
# # frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['Algorithm']=AlgorithmName
# outputDict['Language']="python"
# outputDict['library']="PAMI"
# outputDict['minSup']=minSup
# outputDict['totalFI']=len(obj1._finalPatterns.items())
# outputDict['Runtime']=obj1.getRuntime()
# outputDict['Memory']=obj1.getMemoryUSS()
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)
# print(AlgorithmName + " Done!")
# ############################

# ############################
# AlgorithmName='DEclat'
# from PAMI.frequentPattern.basic import ECLATDiffset as PAMI
# obj1 = PAMI.ECLATDiffset(iFile=filepath, minSup=minSup, sep=separator)
# # from editedCode.PAMIECLATDiffset import ECLATDiffset as PAMIedited
# # obj1 = PAMIedited.ECLATDiffset(data, minSup=minSup, sep=separator)
# obj1.mine()
# # frequentPatterns= obj1.getPatternsAsDataFrame()
# # frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# # print(frequentPatternsDF)
# outputDict = {}
# outputDict['Algorithm']=AlgorithmName
# outputDict['Language']="python"
# outputDict['library']="PAMI"
# outputDict['minSup']=minSup
# outputDict['totalFI']=len(obj1._finalPatterns.items())
# outputDict['Runtime']=obj1.getRuntime()
# outputDict['Memory']=obj1.getMemoryUSS()
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close() 
# json.dumps(outputDict, indent=4)
# print(AlgorithmName + " Done!")
# ############################