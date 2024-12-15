#import libraries
import numpy as np
import pandas as pd
import copy
import time as t
import json

# made obsolete at 10/12/2024 by Malliaridis
# def Merge(dict1, dict2):
#     #this function is responsible for merging two dictionaries
#     res = {**dict1, **dict2}
#     return res

class TKFIM:

    def __init__(self, dataset_file, topK, delimiter=' ', sparseData=True):
        self.dataset_file = dataset_file
        self.minSup = None  # The relative minimum support
        self.min_count = None  # The absolute minimum support
        self.delimiter = delimiter 
        self.num_of_transactions = None 
        self.execution_time = None # Overall time of mining
        self.topK = topK #User defined Tok-K threshold
        self.sparseData=sparseData

        #initialize variables for TKFIM algorithm
        self.data = None # stores original data in its vertical representation (Key is the 1-item while value is a list of all the transactions containing that item)
        self.finalTopK = dict() #for showing final results
        self.maxLevel=0 # The max length of itemsets grater than minSup
        self.heap=FixedSizeHeap(topK) #Tok-K absolute support values heap initialization

    def readDatasetFile(self):

        with open(self.dataset_file, encoding='utf-8-sig') as f:
            transactions = [line.strip().split(sep=self.delimiter) for line in f]

        self.num_of_transactions=len(transactions)

        d = {}
        for i, row in enumerate(transactions):
            for item in row:
                if item not in d:
                    d[item] = []  # Initialize a new list if the key is not in the dictionary
                d[item].append(i)  # Append the transaction index to the list                

        self.data=d
        ##################################################
        # +1 +3 This Code is changed with the above at 3/12/2024 from Malliaridis.
        # pandas dataFrame cannot manipulate in right manner transactional dataset (1-MBL type)
        # df1 = pd.read_csv(self.dataset_file, sep=self.delimiter, header=None)
        # self.num_of_transactions = df1.count(axis=0)[0]# total num of rows.
        # trx = [str(i) for i in range(1, int(df1.max().max()) + 1)]#list containing values from 0 to max value in dataFrame
        # #print(trx)
        # trxIds = []
        # d = dict.fromkeys(trx)#initialize dict with trx as keys and assign empty values.
        # row = df1.values.tolist()
        # for each in trx:
        #     i = 0
        #     while(i != self.num_of_transactions): #loop through every row for each iteration of trx.
        #         #current  = row[i]# i is the current row number, Var row contains complete row data.
        #         if float(each) in row[i]: #if value is present in current row.
        #             # if not d[each]: #if d[each] is currently empty
        #             #     d[each] = i # then assign row number to d[each]
        #             # else:
        #             #     d[each] = str(d[each]) + ", " + str(i)# get current value of d[each], add current row number to the value and assign back to d[each].
        #             trxIds.append(int(i))
        #             # print(trxIds)
        #         # else:
        #         # 	print(f"{each} not found in {i}")
        #         i+=1 #increment until total num of rows == i.
        #     d[each] = trxIds.copy()
        #     # d[each] = trxIds
        #     trxIds.clear()
        #return d


    #define necessary functions
    # def makePrefix(self, key):
    #     #this functions is responsible for generating classes i.e FBA, ABC etc
    #     tem_var = ""

    #     for i in range(0, len(key)):
    #         if key[i] not in tem_var:
    #             tem_var += key[i]
    #     return tem_var


    def getTopKFI(self, topKList):
        # TODO Documentation
        # TODO Documentation
        # TODO Documentation

        topKList = dict(sorted(topKList.items(), key=lambda itemSet:(itemSet[1], itemSet[0]), reverse = True))

        res=dict()
        mS=-1
        for index, (key, value) in enumerate(topKList.items()):
            # TODO Documentation
            if index>=self.topK-1:
                if mS==-1:
                    mS=value
                elif value!=mS:    
                    mS=value
                    break

            res[key]=value

        # if mS==-1:
        #     self.min_count=value
        # else:
            self.min_count=mS

        # res=dict(list(TopKList.items())[:self.topK])
        ##################################################
        # This Code is changed with the above at 3/12/2024 from Malliaridis.
        # res = {}
        # topKCount = 1
        # for k,v in TopKList.items():
        #     if v not in res.values():
        #         topKCount += 1
        #     if topKCount<=self.topK:
        #         res[k] = v
        #     else:
        #         break
        # self.finalTopK=res
        return res

    def firstTopKList(self):
        item1TopKList = {} # 
        for k,v in self.data.items():
            c=len(v)
            item1TopKList[k] = c

        # item1TopKList = {k: v for k, v in sorted(itemset.items(), key=lambda item: item[1], reverse=True)}
        item1TopKList = self.getTopKFI(item1TopKList)

        self.heap.initialFill(list(item1TopKList.values()))

        item1TopKList.clear()

        return item1TopKList

    def getFromTopK(self, initialTopK):

        itemset = {}

        topKList = {}

        # Correction 3/12/2024
        # copy the dictionary
        currentLevelTopK = {**initialTopK}


        #the number of items in itemset
        level =  int(1)

        while level > 0:

            # initialization of the first itemset counter
            k = int(0)

            # Collect only the first topK items. the rest are discarded
            # malliaridis 10/12/2024 (+10)
            listOFKeys = list(currentLevelTopK.keys())[:self.topK]
            # listOFKeys = list(currentLevelTopK.keys())

            while(k < len(listOFKeys)):

                firstClass = listOFKeys[k]
                # stop current iteration if firstClass itemset has already been above the current minSup.
                if currentLevelTopK[firstClass]<=self.min_count:
                    break

                # initialization of the first itemset counter
                k1 = int(k + 1)

                while (k1 < len(listOFKeys)):

                    secondClass = listOFKeys[k1]

                    # Malliaridis gave at least 5x in chess 1000 (and not only) with intersect (7.9s vs 1.3s)
                    #stop current iteration if any of the two engaging itemsets has already been above the current minSup.
                    if currentLevelTopK[firstClass]<=self.min_count or currentLevelTopK[secondClass]<=self.min_count:
                        break

                    # To find the candidate 2-item itemSets    
                    if level==1:

                        if self.sparseData:
                            transactions=set(self.data[firstClass]) & set(self.data[secondClass])
                            support = len(transactions)
                        else:
                            # (+11) 
                            transactions = set(self.data[firstClass]) - set(self.data[secondClass])
                            support = currentLevelTopK[firstClass]-len(transactions)
                    
                        if support >= self.min_count:

                            #recalculate the new absolute minSup value
                            self.min_count=self.heap.insert(support)                            

                            key = firstClass +"," + secondClass

                            # Correction 3/1/2024
                            # 10x faster at least the below than the above in chess.dat at least!
                            # if not self.sparseData:
                            #     transactions=list(transactions)
                            # else:
                            #     transactions = list(set(self.data[firstClass])-set(diffSet))
                            #     transactions = list(set(self.data[firstClass]))
                            #     for each in set(diffSet):
                            #         transactions.remove(each)

                            self.data[key] = list(transactions) #add the frequent itemset to vertical database because it would help finding the superSet candidates.
                            itemset[key] = support

                        # 10/12/2024 Malliaridis (+7) obsolete and non working. loses itemsets.
                        # elif self.fastMode:
                            # break #ignores all the other candidates (from current k1 to len(listOFKeys))
                            #loss of FIs but to about 40% quicker

                    # To find the candidate (3 or more)-item itemSets 
                    else:
                        prefixA = firstClass.split(",")
                        prefixB = secondClass.split(",")

                        itemA = prefixA.pop(level-1)
                        itemB = prefixB.pop(level-1)

                        if prefixA == prefixB:

                            if self.sparseData:
                                transactions=set(self.data[firstClass]) & set(self.data[secondClass])
                                support = len(transactions)
                            else:
                                # (+11)
                                transactions = set(self.data[secondClass])-set(self.data[firstClass])
                                support=currentLevelTopK[firstClass]-len(transactions)
                                # tmp=set(self.data[firstClass])
                                # diffSet = tmp - set(self.data[secondClass])
                                # transactions = tmp-diffSet

                            if support >= self.min_count:

                                #recalculate the new absolute minSup value
                                self.min_count=self.heap.insert(support)

                                items = prefixA + [itemA, itemB]

                                key = ",".join(items)

                                # Correction 3/1/2024
                                # transactions = [ele for ele in set(self.data[firstClass]) if ele not in diffSet]
                                # 4x faster the below than the above!
                                # if self.sparseData:
                                #     transactions=list(transactions)
                                # else:
                                #     transactions = list(set(self.data[firstClass]))
                                #     for each in set(diffSet):
                                #         transactions.remove(each)

                                self.data[key] = list(transactions) #add the frequent itemset to vertical database because it would help finding the superSet candidates.
                                itemset[key] = support
                                
                            # 10/12/2024 Malliaridis (+7) obsolete and non working. loses itemsets.
                            # elif self.fastMode:
                                # break #ignores all the other candidates (from current k1 to len(listOFKeys))
                                #loss of FIs but to about 40% quicker

                    k1 += 1

                k+=1

            # New idea...
            # nextLevelTopK = dict(sorted(nextLevelTopK.items(), key = lambda itemset:(itemset[1], itemset[0]), reverse=True)[:self.topK])
            # self.finalTopK = {**self.finalTopK,**nextLevelTopK}
            # self.finalTopK = dict(sorted(self.finalTopK.items(), key= lambda itemset:(itemset[1], itemset[0]), reverse = True))
            # self.finalTopK = self.getTopKFI(self.finalTopK)
            # currentLevelTopK = {**dict(nextLevelTopK)}

            # if(len(nextLevelTopK) == 0): # new itemset with support grater than minSup not found. Stop iteration
            #     self.maxLevel=level
            #     level=0
            # else:
            #     level += 1
            #     nextLevelTopK.clear()



            itemset = sorted(itemset.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

            topKCount = int(0)
            for k,v in itemset:
                if v not in topKList.values():
                    topKCount += 1
                if topKCount<=self.topK:
                    topKList[k] = v

            # merge two dictionaries into a new one using dictionary unpacking
            topKList = {**initialTopK,**topKList} 
            # self.Merge(initialTopK, topKList)

            topKList = dict(sorted(topKList.items(), key= lambda kv:(kv[1], kv[0]), reverse = True))
            topKList = self.getTopKFI(topKList)
            #Deleted by Malliaridis 5/12/2024 unnecessary for mining time improvement
            #topKList = dict(sorted(topKList.items(), key= lambda kv:(kv[1], kv[0]), reverse = True))
            # minKey = min(topKList, key=topKList.get)
            # smallestK = topKList[minKey] # for correcting smallest K

            if(len(itemset) == 0):
                itemCount = 0
            else:
                itemCount += 1

            currentLevelTopK.clear()
            itemset = dict(itemset)

            # Correction 3/12/2024
            # copy the dictionary
            currentLevelTopK = {**itemset}
            # currentLevelTopK = copy.deepcopy(itemset)

            itemset.clear()
            
        return self.min_count, topKList

    def writeFIM(self, outputFile=None):
        if (outputFile):
            # Write the dictionary to a file in pretty JSON format
            with open(outputFile, "w") as file:
                json.dump(self.finalTopK, file, indent=4)

    def mine(self):

        start = t.time()#Start Time.

        initialTopK = self.firstTopKList()

        # self.min_count, self.finalTopK = self.getFromTopK(initialTopK)
        self.getFromTopK(initialTopK)
        self.minSup=self.min_count/self.num_of_transactions

        end = t.time()#end Time
        self.execution_time=end-start

        print(f"\nTotal Execution Time: {self.execution_time} Seconds")
        print(f"FIM found:{len(self.finalTopK)}")
        print(f"Absolute minSup:{self.min_count}")
        print(f"Relative minSup:{self.minSup}")

class FixedSizeHeap:
    def __init__(self, size=10):
        self.size = size
        self.heapList = []  # Initialize an empty list
    
    def initialFill(self, initialList):
        self.heapList=initialList[:self.size]

    def insert(self, value):
        # Insert the new value
        self.heapList.append(value)
        # Sort the list in descending order
        self.heapList.sort(reverse=True)
        # Maintain the fixed size
        if len(self.heapList) > self.size:
            self.heapList.pop()  # Remove the smallest element (last in the list)
        
        return self.getMinSup()
    
    def getMinSup(self):
        if self.heapList:
            return self.heapList[-1]  # Return the last element (smallest value)
        return None  # If the heap is empty
    
    def __str__(self):
        return "\n".join(map(str, self.heapList))