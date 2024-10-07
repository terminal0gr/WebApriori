import os
import sys

identity='79d1727987f200802593e3599119c966' 
# datasetName='H-MineSample.txt'
# datasetName='0fish_catches.csv'
datasetName='invoiceType1.csv'
datasetName='Transactional_T10I4D100K.csv'
public=0
minSup=0.01

if public==0:
    filepath=os.path.join('datasets', identity, datasetName)
else:
    filepath=os.path.join('public', datasetName)



from PAMI.frequentPattern.topk import FAE as PAMI
obj1 = PAMI.FAE(iFile=filepath, k=100, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv('FAE.csv')
#print(frequentPatternsDF)
print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
print('Memory (USS): ' + str(obj1.getMemoryUSS()))
sys.exit()



from PAMI.frequentPattern.basic import Apriori as PAMI
obj1 = PAMI.Apriori(iFile=filepath, minSup=minSup, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv('Apriori.csv')
# print(frequentPatternsDF)
print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
print('Memory (USS): ' + str(obj1.getMemoryUSS()))

from PAMI.frequentPattern.basic import Aprioribitset as PAMI
obj1 = PAMI.Aprioribitset(iFile=filepath, minSup=minSup, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv('Aprioribitset.csv')
# print(frequentPatternsDF)
print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
print('Memory (USS): ' + str(obj1.getMemoryUSS()))

from PAMI.frequentPattern.basic import ECLAT as PAMI
obj1 = PAMI.ECLAT(iFile=filepath, minSup=minSup, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv('Eclat.csv')
# print(frequentPatternsDF)
print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
print('Memory (USS): ' + str(obj1.getMemoryUSS()))

from PAMI.frequentPattern.basic import ECLATDiffset as PAMI
obj1 = PAMI.ECLATDiffset(iFile=filepath, minSup=minSup, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv('dEclat.csv')
# print(frequentPatternsDF)
print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
print('Memory (USS): ' + str(obj1.getMemoryUSS()))

from PAMI.frequentPattern.basic import ECLATbitset as PAMI
obj1 = PAMI.ECLATbitset(iFile=filepath, minSup=minSup, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv('ECLATbitset.csv')
# print(frequentPatternsDF)
print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
print('Memory (USS): ' + str(obj1.getMemoryUSS()))

from PAMI.frequentPattern.basic import FPGrowth as PAMI
# fileURL = "https://u-aizu.ac.jp/~udayrage/datasets/transactionalDatabases/Transactional_T10I4D100K.csv"
#obj = alg.FPGrowth(iFile=fileURL, minSup=minSup, sep='\t')
obj1 = PAMI.FPGrowth(iFile=filepath, minSup=minSup, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv('FPGrowth.csv')
# print(frequentPatternsDF)
print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
print('Memory (USS): ' + str(obj1.getMemoryUSS()))

from PAMI.frequentPattern.topk import FAE as PAMI
obj1 = PAMI.FAE(iFile=filepath, k=100, sep='\t')
obj1.mine()
frequentPatternsDF= obj1.getPatternsAsDataFrame()
frequentPatternsDF.to_csv('FAE.csv')
print(frequentPatternsDF)
print('Total No of patterns: ' + str(len(frequentPatternsDF))) #print the total number of patterns
print('Runtime: ' + str(obj1.getRuntime())) #measure the runtime
print('Memory (RSS): ' + str(obj1.getMemoryRSS()))
print('Memory (USS): ' + str(obj1.getMemoryUSS()))

