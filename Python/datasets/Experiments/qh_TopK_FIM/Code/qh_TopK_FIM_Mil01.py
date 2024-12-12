#import libraries
import time as t
import json

class qh_TopK_FIM:

    def __init__(self, dataset_file, topK, delimiter=' ', sparseData=True):
        self.dataset_file = dataset_file
        self.minSup = None  # The relative minimum support
        self.min_count = None  # The absolute minimum support 
        self.delimiter = delimiter 
        self.num_of_transactions = None 
        self.execution_time = None # Overall time of mining
        self.topK = topK #User defined Tok-K threshold
        self.sparseData=sparseData
        self.data = None # stores original data in its vertical representation (Key is the 1-item while value is a list of all the transactions containing that item)
        self.finalTopK = None #for showing final results
        self.maxLevel=0 # The max length of itemsets grater than minSup
        self.heap=FixedSizeHeap(topK) #Tok-K absolute support values heap initialization

    def readDatasetFile(self):

        # Dataset it traversed once only!
        with open(self.dataset_file, encoding='utf-8-sig') as f:
            transactions = [line.strip().split(sep=self.delimiter) for line in f]

        self.num_of_transactions=len(transactions)

        # Vertical dataset representation
        d = {}
        for i, row in enumerate(transactions):
            for item in row:
                if item not in d:
                    d[item] = []  # Initialize a new list if the key is not in the dictionary
                d[item].append(i)  # Append the transaction index to the list                

        self.data=d

    # Fills the topKList with the top-K 1-item itemsets.
    # It also initializes the quick heap for first and last time.
    def firstTopKList(self):
        item1TopKList = {} 
        for key, value in self.data.items():
            item1TopKList[key] = len(value)

        item1TopKList, self.min_count = self.getTopKFI(item1TopKList)

        # Initializes the quick Heap with brute passing a list of support values
        self.heap.initialFill(list(item1TopKList.values()))

        return item1TopKList

    def getTopKFI(self, topKItemSets):
        # The procedure returns the dictionary of topK ItemSets from a given set of itemsets with their support in descending order
        # The count of ItemSets may differ if there are itemsets with the same minimum support which are also included
        # e.g. it may return 102 instead 100 if there are 3 itemsets with the same minSup.
        
        # The dictionary gets sorted by itemset's support in descending order 
        topKItemSets = dict(sorted(topKItemSets.items(), key= lambda itemset:(itemset[1], itemset[0]), reverse = True))

        # This mechanism guarantees that only the Top-K itemsets so far will be returned 
        # plus the itemsets that have equal support as the current minSup.
        topKDict=dict()
        mS=-1
        for index, (key, value) in enumerate(topKItemSets.items()):
            if index>=self.topK-1:
                if mS==-1:
                    mS=value
                elif value!=mS:
                    break
            topKDict[key]=value
        if mS==-1:
            minSup=value
        else:
            minSup=mS

        return topKDict, minSup

    def mineNextLevels(self, initialTopK):

        # Collects the final Top-K itemsets
        topKFI = {**initialTopK}
        # Represents the current level itemsets
        currentLevelTopK = {**initialTopK}
        # Represents the next level candidate itemsets to be found
        nextLevelTopK = {}

        #count the items participating in itemset or alternatively the current class level
        level = 1

        while level > 0:

            # initialization of the first itemset counter
            iA = 0

            # Collect only the first topK items. the rest are discarded
            # malliaridis 10/12/2024 (+10)
            listOFKeys = list(currentLevelTopK.keys())[:self.topK]
            # listOFKeys = list(currentLevelTopK.keys())

            while(iA < len(listOFKeys)):

                classA = listOFKeys[iA]
                # stop current iteration if classA itemset has already been above the current minSup.
                if currentLevelTopK[classA]<=self.min_count:
                    break

                # initialization of the second itemset counter
                iB=iA+1

                while (iB<len(listOFKeys)):

                    classB = listOFKeys[iB]

                    # Gave at least 5x in chess 1000 (and not only) with intersect (7.9s vs 1.3s)
                    # Stop current iteration if any of the two engaging itemsets has already been above the current minSup.
                    if currentLevelTopK[classA]<=self.min_count or currentLevelTopK[classB]<=self.min_count:
                        break

                    prefixA = classA.split(",")
                    prefixB = classB.split(",")

                    itemA = prefixA.pop(level-1)
                    itemB = prefixB.pop(level-1)

                    if prefixA == prefixB:

                        if self.sparseData:
                            transactions=set(self.data[classA]) & set(self.data[classB])
                            support = len(transactions)
                        else:
                            # (+11)
                            if level==1: #In level 1 we have tidSets
                                transactions = set(self.data[classA])-set(self.data[classB])
                            else: #In next levels we have diffSets (see paper 'Fast Vertical mining using Diffsets' page 7)
                                transactions = set(self.data[classB])-set(self.data[classA])
                            support=currentLevelTopK[classA]-len(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            items = [itemA, itemB]

                            key = prefixA + items
                            key = ",".join(key)

                            self.data[key] = list(transactions) #add the frequent itemset to vertical database because it would help finding the superSet candidates.
                            nextLevelTopK[key] = support

                    iB+=1
                iA+=1

            # sort new level itemsets by their support value in descending order
            nextLevelTopK = sorted(nextLevelTopK.items(), key = lambda itemset:(itemset[1], itemset[0]), reverse=True)

            # Add in the final TopK the new level frequent itemsets that have support value greater than minSup threshold
            for value in nextLevelTopK:
                if value[1]<self.min_count:
                    break
                topKFI[value[0]]=value[1]

            # return the absolute TopK itemsets so far
            topKFI, self.min_count = self.getTopKFI(topKFI)

            if(len(nextLevelTopK) == 0):
                level = 0
            else:
                level += 1

            currentLevelTopK=dict(nextLevelTopK)
            nextLevelTopK={}

        return topKFI, self.min_count

    # The main mining procedure
    def mine(self):

        start = t.time() #Start Time.

        initialTopK = self.firstTopKList()
        self.finalTopK, self.min_count = self.mineNextLevels(initialTopK)
        self.minSup=self.min_count/self.num_of_transactions

        end = t.time() #end Time
        self.execution_time=end-start

        print(f"\nTotal Execution Time: {self.execution_time} Seconds")
        print(f"FIM found:{len(self.finalTopK)}")
        print(f"Absolute minSup:{self.min_count}")
        print(f"Relative minSup:{self.minSup}")

    def writeFIM(self, outputFile=None): #outputs the frequent itemsets in json format
        if (outputFile):
            # Write the dictionary to a file in pretty JSON format
            with open(outputFile, "w") as file:
                json.dump(self.finalTopK, file, indent=4)

# implementation of the quick heap which keeps only the Top-K supports in descending order
# Quick and memory saver.
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