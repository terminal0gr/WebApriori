#import libraries
import numpy as np
import pandas as p
import copy

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
    for i in range(1, 3):
        # print("####Min TOP K######")
        # print(initialTopK)
        #print(smallestK)
        for k in givenTopK.keys():
            for k1 in givenTopK.keys():
                if k!=k1 and k+k1 not in itemset and k1+k not in itemset:
                    # print(k)
                    # print(k1)
                    if k not in dataset and k1 not in dataset:
                        key = k+k1
                        key = makePrefix(key)

                        diffset = list(set(data[k]) - set(data[k1]))
                        support = len(data[k]) - len(diffset)
                        # print('###########Key and SUPPORT###############')
                        # print(key, support)
                        #print(support)
                        data[key] = diffset # add class alongside diffset in data for upcoming classes

                    else:
                        key = k+k1
                        #print(key)
                        key = makePrefix(key)
                        diffset = list(set(dataset[k]) - set(dataset[k1]))
                        # print("############# Diffset ############")
                        # print(diffset)
                        support = len(dataset[k]) - len(diffset)
                        data[key] = diffset # add class alongside diffset in data for upcoming classes

                    if support >= smallestK:
                        itemset[key] = support
                    #print(data['FB'])
                    #print(itemset['FBA'])
        # print("############# itemset before ############")
        # print(itemset)

        itemset = sorted(itemset.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        # print("############# itemset After Sorting ############")
        # print(itemset)
        topKList = {}
        topKCount = int(0)
        for k,v in itemset:
            if v not in topKList.values():
                topKCount += 1
            if topKCount<=K:
                topKList[k] = v
        # print("############# Top K List before ############")
        # print(topKList)
        topKList = Merge(initialTopK, topKList)
        topKList = dict(sorted(topKList.items(), key= lambda kv:(kv[1], kv[0]), reverse = True))
        # print("############# Top K List After ############")
        #print(topKList)
        topKList = GetTopKListOnly(topKList, K)
        #print(topKList)
        topKList = dict(sorted(topKList.items(), key= lambda kv:(kv[1], kv[0]), reverse = True))
        #print(topKList)
        minKey = min(topKList, key=topKList.get)
        smallestK = topKList[minKey]# for reset smallest K
        #print(f"Now smallest K is {smallestK}")
        #print(itemset)
        givenTopK.clear()
        itemset = dict(itemset)
        givenTopK = copy.deepcopy(itemset)
        #print(givenTopK)
        itemset.clear()

    return topKList

###Run codes/functions here.####
dataset = {
    'A' : [1,2,3,6,7,8,9,10],
    'B' : [1,2,4,5,6,7,8,9,10],
    'C' : [4,5,9,10],
    'D' : [1,3,4,5,7,9],
    'E' : [4,5,10],
    'F' : [1,2,3,4,5,6,7,8,9,10],
    #'G' : [3,4,2,4,5,6,7,8,9]
    }

K = int(input("Enter the number of item's you require: \n"))
initialTopK = firstTopKList()

#print("--------------Top ",K," List (Round 1)----------------")
print(initialTopK)
#print(type(initialTopK))
finalTopK = getFromTopK(initialTopK)
print(finalTopK)
