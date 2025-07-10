import os
import sys
from mlxtend.frequent_patterns import apriori, fpgrowth, hmine, association_rules
from time import time
import pandas as pd
import json
import psutil

datasetName='chess.dat' 
minSup=0.945244055068836
separator=' '
# datasetName='1_L-0023.csv' 
# minSup=0.01
# separator=';'

'''
Call arguments          
1) datasetName  
    The name of the dataset. The program expect to find it in a file named dataset
2) min_Support Value in [0..1] 
3) separator 
    The separator of the dataset For space, write " "
'''
#identity
if len(sys.argv)>1:
    datasetName=str(sys.argv[1])

if len(sys.argv)>2:
    minSup=float(sys.argv[2])

if len(sys.argv)>3:
    separator=str(sys.argv[3])

use_colnames=True

ext1='_mlxtend_py.fim'
ext2='_mlxtend_py.json'

# Sample transactions
# transactions = [
#     ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
#     ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
#     ['b', 'f', 'h', 'j', 'o', 'p'],
#     ['b', 'c', 'k', 's', 'p'],
#     ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
# ]

# transactions = [
#     ['A', 'B', 'D'],
#     ['B', 'C', 'E'],
#     ['A', 'B', 'C', 'E'],
#     ['B', 'E']
# ]

# transactions = [
#     ['c','d','e','f','g','i'],
#     ['a','c','d','e','m'],
#     ['a','b','d','e','g','k'],
#     ['a','c','d','h']
# ]

startTime=time()
process = psutil.Process(os.getpid()) # Needed to measure memory
memoryUSS=0 #Memory initialization

# Read the file, treating each line as a single entry
# creates a list of lists
filepath=os.path.join('datasets', datasetName)
with open(filepath,encoding='utf-8-sig') as f:
    transactions = [line.strip().split(sep=separator) for line in f]

# Convert transactions to one-hot encoded DataFrame
from mlxtend.preprocessing import TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)

df = pd.DataFrame(te_ary, columns=te.columns_) 

midTime=time()

# Memory measurement only there...
m=process.memory_full_info().uss
if memoryUSS < m:
    memoryUSS=m


# AlgorithmName='FPGrowth'
# frequentPatterns = fpgrowth(df, min_support=minSup, use_colnames=use_colnames)
AlgorithmName='HMine'
frequentPatterns = hmine(df, min_support=minSup, use_colnames=use_colnames)
# AlgorithmName='Apriori'
# frequentPatterns = apriori(df, min_support=minSup, low_memory=False, use_colnames=use_colnames)


# End time
endTime=time()

# Memory measurement only there...
m=process.memory_full_info().uss
if memoryUSS < m:
    memoryUSS=m

# output frequentPatterns
# frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext1))
# results

# Statistics
outputDict = {} 
outputDict['dataset']=datasetName
outputDict['Algorithm']=AlgorithmName
outputDict['Language']="python"
outputDict['library']="mlxtend"
outputDict['minSup']=minSup
outputDict['totalFI']=len(frequentPatterns)
outputDict['Read and transformation time']=round(midTime-startTime,2)
outputDict['mining time']=round(endTime-midTime,2)
outputDict['Runtime']=round(endTime-startTime,2)
outputDict['Memory']=round(memoryUSS/(1024*1024))
# file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext2),'w')
# json.dump(outputDict, file, indent=4)
# file.close()  
print(json.dumps(outputDict, indent=4))
print(AlgorithmName + " Done!")