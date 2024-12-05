#import libraries
import copy
import preProcessing as pd
import time as t

#initialize variables
itemset = dict()
data = dict()# for storing diffsets
topKList = dict()#for showing end results
topKItem = dict() #for showing top K itemset
userRequired = int(0) # how much items are required by the user
leastItemset = int(0) # item with least support in itemset/previous top K.
support = int(0) # support of an item (trx)
diffset = set() # is the actual diffset of an item.
givenTopK = dict()

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
    for k,v in data.items():
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
    givenTopK = {}
    givenTopK = Merge(givenTopK, initialTopK)
    minKey = min(givenTopK, key=givenTopK.get)
    smallestK = givenTopK[minKey]
    itemCount =  int(1)

    while itemCount > 0:

        k = int(0)

        listOFKeys = list(givenTopK.keys())

        while(k < len(listOFKeys)):
            k1 = int(k + 1)
            while (k1 < len(listOFKeys)):

                firstClass = listOFKeys[k]
                secondClass = listOFKeys[k1]

                if len(firstClass) <= 2:
                    diffset = list(set(data[firstClass]) - set(data[secondClass]))
                    support = len(data[firstClass]) - len(diffset)
                    key = firstClass +"," + secondClass
                    # transactions = [ele for ele in set(data[firstClass]) if ele not in diffset]
                    transactions = list(set(data[firstClass]))
                    for each in set(diffset):
                        transactions.remove(each)

                    data[key] = transactions #add class alongside diffset in data for upcoming classes

                    if support >= smallestK:
                        itemset[key] = support
                    else:
                        break

                else:

                    prefixA = firstClass.split(",")
                    prefixB = secondClass.split(",")

                    length_of_classes = len(prefixA)-1

                    itemA = prefixA.pop(length_of_classes)
                    itemB = prefixB.pop(length_of_classes)

                    if prefixA == prefixB:
                        # print("I am true too")
                        # key = firstClass +","+secondClass
                        # key = makePrefix(key)
                        items = [itemA, itemB]

                        key = prefixA + items
                        key = ",".join(key)

                        diffset = list(set(data[firstClass]) - set(data[secondClass]))
                        support = len(data[firstClass]) - len(diffset)

                        # transactions = [ele for ele in set(data[firstClass]) if ele not in diffset]
                        transactions = list(set(data[firstClass]))
                        for each in set(diffset):
                            transactions.remove(each)
                        # transactions = list(data[firstClass])
                        #print(f"transactions: \t {transactions}")
                        data[key] = transactions #add class alongside diffset in data for upcoming classes

                        # print(f"Key : {key}\t Support: {support}\t Diffset: {diffset}\n")
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

        if(len(itemset) == 0):
            itemCount = 0
        else:
            itemCount += 1
        # print(f"Item Count \t {itemCount}")
        givenTopK.clear()
        itemset = dict(itemset)
        givenTopK = Merge(givenTopK, itemset)
        # print(itemset)
        itemset.clear()
        # print("Length of 40: \t", len(data['40']))
    return topKList

###Run codes/functions here.####
# data = {
#     'A' : [1,2,3,6,7,8,9,10],
#     'B' : [1,2,4,5,6,7,8,9,10],
#     'C' : [4,5,9,10],
#     'D' : [1,3,4,5,7,9],
#     'E' : [4,5,10],
#     'F' : [1,2,3,4,5,6,7,8,9,10],
#     #'G' : [3,4,2,4,5,6,7,8,9]
#     }

# file = open("T401vertical.txt", "r+")
# data = dict(file.read())
# file.close()

data = pd.d

#
# file.seek(0)
# file.write(str(data))
# file.close()

# print(f"lenght of 58:\t {len(dataset['58'])}")
# K = int(input("Enter the number of item's you require: \n"))
K = 1000
# print(f"support of 58: \t {dataset['58']}")

start = t.time()#Start Time.
initialTopK = firstTopKList()

#print("--------------Top ",K," List (Round 1)----------------")
print(initialTopK)
#print(type(initialTopK))
finalTopK = getFromTopK(initialTopK)
print(finalTopK)
print(f"Total FI Count: {len(finalTopK)}")
end = t.time()#Final Time
print(f"\nTotal Execution Time: {end - start} Seconds")
