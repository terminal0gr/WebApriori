#import libraries
import numpy as np
import pandas as p
import copy
import preProcessing as pd
import time as t

#initialize variables
dataset = dict()
itemset = dict()
data = dict()# for storing diffsets
topKList = dict()#for showing end results
topKItem = dict() #for showing top K itemset
userRequired = int(0) # how much items are required by the user
leastItemset = int(0) # item with least support in itemset/previous top K.
support = int(0) # support of an item (trx)
diffset = set() # is the actual diffset of an item.

#define necessary functions
def makePrefix(key):
    #this functions is responsible for generating classes i.e FBA, ABC etc
    tem_var = ""

    for i in range(0, len(key)):
        if key[i] not in tem_var:
            tem_var += key[i]
    return tem_var

def Merge(dict1, dict2):
    #this function is responsible for merging two dictionaries
    res = {**dict1, **dict2}
    return res

def GetTopKListOnly(data, k):
    res = {}
    # print("#### Printing res ##############")
    # print(res)
    topKCount = int(0)
    for k,v in data.items():
        # print("#### Printing res ##############")
        # print(res)
        if v not in res.values():
            topKCount += 1
        if topKCount<=K:
            res[k] = v
    return res


def firstTopKList():
    itemset = {}
    for k,v in dataset.items():
        c=len(v)
        itemset[k] = c
        data[k] = v # store all dataset into data...
    # print(f"itemset 5: \t {itemset['5']}")
        # print(f"Key {k}: \t value:\t {len(v)}")
    itemset = sorted(itemset.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

    firstTopKList = {}
    for k,v in itemset:
        firstTopKList[k] = v

    firstTopKList = GetTopKListOnly(firstTopKList, K)
    itemset.clear()
    # print("--------------Top ",K," List (Round 1)----------------")
    # print(topKList)
    return firstTopKList

def getFromTopK(initialTopK):

    itemset = {}
    topKList = {}

    givenTopK = copy.deepcopy(initialTopK)
    minKey = min(givenTopK, key=givenTopK.get)
    smallestK = givenTopK[minKey]
    itemCount =  int(1)

    while itemCount > 0:
        # print("####Min TOP K######")
        # print(initialTopK)
        #print(smallestK)

        #for k in list(givenTopK.keys()):
        k = int(0)

        listOFKeys = list(givenTopK.keys())
        # print(f"itemset of {i}\t {listOFKeys}")
        while(k < len(listOFKeys)):
            k1 = int(k + 1)
            while (k1 < len(listOFKeys)):
                # if k!=k1 and k+k1 not in itemset and k1+k not in itemset:
                firstClass = listOFKeys[k]
                secondClass = listOFKeys[k1]
                # key = ""

                if len(firstClass) <= 2:
                    #print(f"firstClass[prefix]\t {firstClass}")           key = firstClass + secondClass
                    diffset = list(set(data[firstClass]) - set(data[secondClass]))
                    support = len(data[firstClass]) - len(diffset)
                    key = firstClass +"," + secondClass
                    transactions = [ele for ele in set(data[firstClass]) if ele not in diffset]
                    #print(f"transactions: \t {transactions}")
                    data[key] = transactions #add class alongside diffset in data for upcoming classes
                    print(f"Key : {key}\t Support: {support}\t Diffset: {diffset}\n")
                    if support >= smallestK:
                        itemset[key] = support
                    else:
                        break

                else:
                    prefixA = firstClass[:-1]
                    prefixB = secondClass[:-1]


                    print(f"firstClass[0]\t {prefixA[0]} \t secondClass[0] {prefixB[0]}\t Length: {len(prefixA)}")
                    if prefixA == prefixB:
                        # print("I am true too")
                        key = firstClass +","+secondClass
                        # key = makePrefix(key)
                        diffset = list(set(data[firstClass]) - set(data[secondClass]))
                        support = len(data[firstClass]) - len(diffset)

                        transactions = [ele for ele in set(data[firstClass]) if ele not in diffset]
                        #print(f"transactions: \t {transactions}")
                        data[key] = transactions #add class alongside diffset in data for upcoming classes
                        print(f"Key : {key}\t Support: {support}\t Diffset: {diffset}\n")
                        if support >= smallestK:
                            itemset[key] = support
                        elif support < smallestK:
                            break

                #print(listOFKeys[k1])
                # itemset = sorted(itemset.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
                # itemset = dict(itemset)
                k1 += 1
                # k1 = int(k + 1)
            k+=1


        itemset = sorted(itemset.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        # print(itemset)
        # topKList = {}
        topKCount = int(0)
        for k,v in itemset:
            if v not in topKList.values():
                topKCount += 1
            if topKCount<=K:
                topKList[k] = v

        #print(topKList)
    # print("############# Top K List before ############")
    # print(topKList)
        topKList = Merge(initialTopK, topKList)
        topKList = dict(sorted(topKList.items(), key= lambda kv:(kv[1], kv[0]), reverse = True))
        # print("############# Top K List After ############")
        #print(topKList)
        topKList = GetTopKListOnly(topKList, K)
        #print(topKList)
        topKList = dict(sorted(topKList.items(), key= lambda kv:(kv[1], kv[0]), reverse = True))
        #print(topKList)\
        minKey = min(topKList, key=topKList.get)
        smallestK = topKList[minKey]# for reset smallest K

        # print(f"TopK List for round {i}\t{topKList}")
    #print(f"Now smallest K is {smallestK}")
        # print(f"Itemset: \t{itemset}")
        # print(len(itemset))
        if(len(itemset) == 0):
            itemCount = 0
        else:
            itemCount += 1
        print(f"Item Count \t {itemCount}")
        givenTopK.clear()
        itemset = dict(itemset)
        givenTopK = copy.deepcopy(itemset)
        # print(itemset)
        itemset.clear()
        
    return topKList

###Run codes/functions here.####
# dataset = {
#     'A' : [1,2,3,6,7,8,9,10],
#     'B' : [1,2,4,5,6,7,8,9,10],
#     'C' : [4,5,9,10],
#     'D' : [1,3,4,5,7,9],
#     'E' : [4,5,10],
#     'F' : [1,2,3,4,5,6,7,8,9,10],
#     #'G' : [3,4,2,4,5,6,7,8,9]
#     }

start = t.time()#Start Time.
dataset = pd.d
# print(f"lenght of 58:\t {len(dataset['58'])}")
K = int(input("Enter the number of item's you require: \n"))
# print(f"support of 58: \t {dataset['58']}")
initialTopK = firstTopKList()

#print("--------------Top ",K," List (Round 1)----------------")
print(initialTopK)
#print(type(initialTopK))
finalTopK = getFromTopK(initialTopK)
print(finalTopK)
end = t.time()#Final Time
print(f"\nTotal Execution Time: {end - start} Seconds")
