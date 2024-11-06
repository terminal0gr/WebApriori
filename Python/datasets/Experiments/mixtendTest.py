import os
from mlxtend.frequent_patterns import apriori, fpgrowth, hmine, association_rules
from time import time
import pandas as pd
import json
import psutil

datasetName='chess.dat' 
minSup=0.7
separator=' '

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

# Read the file, treating each line as a single entry
# creates a list of lists
filepath=os.path.join('datasets', datasetName)
with open(filepath) as f:
    transactions = [line.strip().split(sep=separator) for line in f]

# Convert transactions to one-hot encoded DataFrame
from mlxtend.preprocessing import TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_) 


################################
AlgorithmName='FPGrowth_mlxtend'
# FI mining
startTime=time()
frequentPatterns = fpgrowth(df, min_support=minSup, use_colnames=True)
endTime=time()
# output frequentPatterns
frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+'.rules'))
# results
process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss
outputDict = {} 
outputDict['totalFI']=str(len(frequentPatterns))
outputDict['Runtime']=str(str(endTime-startTime))
outputDict['Memory']=str(memoryUSS)
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close()  
json.dumps(outputDict, indent=4)
################################

################################
AlgorithmName='HMine_mlxtend'
# FI mining
startTime=time()
frequentPatterns = hmine(df, min_support=minSup, use_colnames=True)
endTime=time()
# output frequentPatterns
frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+'.rules'))
# results
process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss
outputDict = {} 
outputDict['totalFI']=str(len(frequentPatterns))
outputDict['Runtime']=str(str(endTime-startTime))
outputDict['Memory']=str(memoryUSS)
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close()  
json.dumps(outputDict, indent=4)
################################


################################
AlgorithmName='Apriori_mlxtend'
# FI mining
startTime=time()
frequentPatterns = apriori(df, min_support=minSup, low_memory=False, use_colnames=True)
endTime=time()
# output frequentPatterns
frequentPatterns.to_csv(os.path.join('output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+'.rules'))
# results
process = psutil.Process(os.getpid())
memoryUSS = process.memory_full_info().uss
outputDict = {} 
outputDict['totalFI']=str(len(frequentPatterns))
outputDict['Runtime']=str(str(endTime-startTime))
outputDict['Memory']=str(memoryUSS)
ext='.json'
file = open(os.path.join('Output',os.path.splitext(datasetName)[0]+"_"+str(minSup)+"_"+AlgorithmName+ext),'w')
json.dump(outputDict, file, indent=4)
file.close()  
json.dumps(outputDict, indent=4)
################################

