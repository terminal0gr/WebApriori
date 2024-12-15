#import libraries
import time as t
import sys
import json

class qh_TopK_FIM:

    def __init__(self, dataset_file, topK, delimiter=' ', sparseData=True, bitSetMode=False):
        self.dataset_file = dataset_file
        self.minSup = None  # The relative minimum support
        self.min_count = None  # The absolute minimum support 
        self.delimiter = delimiter 
        self.num_of_transactions = None 
        self.execution_time = None # Overall time of mining
        self.topK = topK #User defined Tok-K threshold
        self.sparseData=sparseData
        self.bitSetMode=bitSetMode
        self.data = None # stores original data in its vertical representation (Key is the 1-item while value is a list of all the transactions containing that item)
        self.finalTopK = None #for showing final results
        self.maxLevel=0 # The max length of itemsets grater than minSup
        self.heap=FixedSizeHeap(topK) #Tok-K absolute support values heap initialization

    def readDatasetFile(self):

        # Dataset traversed once only!
        with open(self.dataset_file, encoding='utf-8-sig') as f:
            #TODO Documentation
            #TODO Documentation
            #TODO Documentation

            # Vertical dataset representation
            vR={}
            iSet=set()
            itemIndex=0
            transIndex=0
            itemDict=dict()
            itemDictReversed=dict()
            for line in f:
                transIndex+=1
                for item in line.strip().split(sep=self.delimiter):
                    if item not in iSet:
                        itemIndex+=1
                        itemDict[itemIndex]=item
                        itemDictReversed[item]=itemIndex
                        vR[(itemIndex,)]=list()
                        iSet.add(item)
                    vR[(itemDictReversed[item],)].append(transIndex)
            self.num_of_transactions=transIndex

        topKItemSetsList = sorted(((key, len(value)) for key, value in vR.items()), key=lambda x: x[1], reverse=True)

        item1TopKList, self.min_count = self.InitialTopKFIList(topKItemSetsList)

        # Initializes the quick Heap with brute passing a list of support values
        self.heap.initialFill(list(item1TopKList.values()))

        vR = {key: vR[key] for key in item1TopKList if key in vR}

        if self.bitSetMode:
            vBitSet=dict()
            # for key, value in vR.items()[:self.topK-1]:
            for key, value in vR.items():
                vBitSet[key] = _bitPacker(vR[key], transIndex)
            self.data=vBitSet
        else:
            self.data = vR
        
        return item1TopKList

    def InitialTopKFIList(self, topKItemSetsList):
        ### It works only for the first 1-item itemSets!!!

        # The procedure returns the dictionary of the first topK 1-Item ItemSets form the set of itemsets with their support in descending order
        # The count of ItemSets may differ if there are itemsets with the same minimum support which are also included
        # e.g. it may return 102 instead 100 if there are 3 itemsets with the same minSup.
        
        # This mechanism guarantees that only the Top-K itemsets so far will be returned 
        # plus the itemsets that have equal support as the current minSup.
        topKDict=dict()
        mS=-1
        for index, (key, value) in enumerate(topKItemSetsList):
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

    def mineNextLevelsDiffSet(self, initialTopK):
        # Implemented without recursion for faster implementation 
        # and less memory consumption

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

                    prefixA=classA[:-1]
                    prefixB=classB[:-1]
                    # prefixA = classA.split(",")
                    # prefixB = classB.split(",")

                    itemA = classA[-1]
                    itemB = classB[-1]
                    # itemA = prefixA.pop(level-1)
                    # itemB = prefixB.pop(level-1)

                    if prefixA == prefixB:

                        # if self.sparseData:
                            # transactions=self.data[classA] & self.data[classB]
                            # support=int.bit_count(transactions)
                            # transactions=set(self.data[classA]) & set(self.data[classB])
                            # support = len(transactions)
                        # else:
                        # (+11)
                        if level==1: #In level 1 we have tidSets
                            transactions = set(self.data[classA])-set(self.data[classB])
                        else: #In next levels we have diffSets (see paper 'Fast Vertical mining using Diffsets' page 7)
                            transactions = set(self.data[classB])-set(self.data[classA])
                        support=currentLevelTopK[classA]-len(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            key=prefixA + (itemA, itemB)
                            # items = [itemA, itemB]
                            # key = prefixA + items
                            # key = ",".join(key)

                            # self.data[key] = transactions
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
    
    def mineNextLevelsDiffSetBitSet(self, initialTopK):
        # Implemented without recursion for faster implementation 
        # and less memory consumption

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

                    prefixA=classA[:-1]
                    prefixB=classB[:-1]
                    # prefixA = classA.split(",")
                    # prefixB = classB.split(",")

                    itemA = classA[-1]
                    itemB = classB[-1]
                    # itemA = prefixA.pop(level-1)
                    # itemB = prefixB.pop(level-1)

                    if prefixA == prefixB:

                        # if self.sparseData:
                            # transactions=self.data[classA] & self.data[classB]
                            # support=int.bit_count(transactions)
                            # transactions=set(self.data[classA]) & set(self.data[classB])
                            # support = len(transactions)
                        # else:
                        # (+11)
                        if level==1: #In level 1 we have tidSets
                            transactions = self.data[classA]-self.data[classB]
                        else: #In next levels we have diffSets (see paper 'Fast Vertical mining using Diffsets' page 7)
                            transactions = self.data[classB]-self.data[classA]
                        support=currentLevelTopK[classA]-int.bit_count(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            key=prefixA + (itemA, itemB)

                            self.data[key] = transactions #add the frequent itemset to vertical database because it would help finding the superSet candidates.
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


    def mineNextLevelsIntersection(self, initialTopK):
        # Implemented without recursion for faster implementation 
        # and less memory consumption

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

                    prefixA=classA[:-1]
                    prefixB=classB[:-1]

                    itemA = classA[-1]
                    itemB = classB[-1]

                    if prefixA == prefixB:

                        # if self.sparseData:
                        # transactions=self.data[classA] & self.data[classB]
                        # support=int.bit_count(transactions)
                        transactions=set(self.data[classA]) & set(self.data[classB])
                        support = len(transactions)
                        # else:
                        #     # (+11)
                        #     if level==1: #In level 1 we have tidSets
                        #         transactions = set(self.data[classA])-set(self.data[classB])
                        #     else: #In next levels we have diffSets (see paper 'Fast Vertical mining using Diffsets' page 7)
                        #         transactions = set(self.data[classB])-set(self.data[classA])
                        #     support=currentLevelTopK[classA]-len(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            key=prefixA + (itemA, itemB)

                            # self.data[key] = transactions
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

    def mineNextLevelsIntersectionBitSet(self, initialTopK):
        # Implemented without recursion for faster implementation 
        # and less memory consumption

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

                    prefixA=classA[:-1]
                    prefixB=classB[:-1]

                    itemA = classA[-1]
                    itemB = classB[-1]

                    if prefixA == prefixB:

                        # if self.sparseData:
                        transactions=self.data[classA] & self.data[classB]
                        support=int.bit_count(transactions)
                            # transactions=set(self.data[classA]) & set(self.data[classB])
                            # support = len(transactions)
                        # else:
                        #     # (+11)
                        #     if level==1: #In level 1 we have tidSets
                        #         transactions = set(self.data[classA])-set(self.data[classB])
                        #     else: #In next levels we have diffSets (see paper 'Fast Vertical mining using Diffsets' page 7)
                        #         transactions = set(self.data[classB])-set(self.data[classA])
                        #     support=currentLevelTopK[classA]-len(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            key=prefixA + (itemA, itemB)

                            #add the frequent itemset to vertical database because it would help finding the superSet candidates.
                            self.data[key] = transactions #bitSet implementation (a big integer number)
                            # self.data[key] = list(transactions)  #list of integers implementation
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

        initialTopK = self.readDatasetFile() 

        endRead = t.time()

        # initialTopK = self.firstTopKList()
        if self.sparseData and self.bitSetMode:
            self.finalTopK, self.min_count = self.mineNextLevelsIntersectionBitSet(initialTopK)
        elif self.sparseData and not self.bitSetMode:
            self.finalTopK, self.min_count = self.mineNextLevelsIntersection(initialTopK)
        elif not self.sparseData and self.bitSetMode:
            self.finalTopK, self.min_count = self.mineNextLevelsDiffSetBitSet(initialTopK)
        elif not self.sparseData and not self.bitSetMode:
            self.finalTopK, self.min_count = self.mineNextLevelsDiffSet(initialTopK)
        self.minSup=self.min_count/self.num_of_transactions

        end = t.time() #end Time
        self.execution_time=end-start

        print(f"Read Dataset Time: {(endRead-start):.3f} Seconds")
        print(f"Total Execution Time: {self.execution_time:.3f} Seconds")
        print(f"FIM found:{len(self.finalTopK)}")
        print(f"Absolute minSup:{self.min_count}")
        print(f"Relative minSup:{self.minSup}")

    def writeFIM(self, outputFile=None): #outputs the frequent itemsets in json format
        print("TODO assemble FIM for output.")
        # if (outputFile):
        #     # Write the dictionary to a file in pretty JSON format
        #     with open(outputFile, "w") as file:
        #         json.dump(self.finalTopK, file, indent=4)

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
    
def _bitPacker(data, maxIndex):
    """

    It takes the data and maxIndex as input and generates integer as output value.

    :param data: it takes data as input.
    :type data: int or float
    :param maxIndex: It converts the data into bits By taking the maxIndex value as condition.
    :type maxIndex: int
    """
    packed_bits = 0
    for i in data:
        packed_bits |= 1 << (maxIndex - i)

    return packed_bits