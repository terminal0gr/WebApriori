#import libraries
import time as t
import json
from concurrent.futures import ProcessPoolExecutor
from functools import partial 
import psutil
import os
import sys


class HTKMiner: 

    def __init__(self, dataset_file, topK, delimiter=' ', tidSet=True, bitSetMode=True, commitTimeout=0):
        self.dataset_file = dataset_file
        self.minSup = None  # The relative minimum support
        self.min_count = 0  # The absolute minimum support 
        self.delimiter = delimiter 
        self.num_of_transactions = 0 # The count of transactions in database
        self.itemCount = 0 # The count of items in database
        self.TransitemCount = 0 # The count of all items in every transaction
        self.topK = topK #User defined Tok-K threshold
        self.tidSet=tidSet # User specified, default True. True intersection mode, False Diffset mode
        self.bitSetMode=bitSetMode # User specified, default True. True bitSet mode, False tidSet mode
        self.data = None # stores original data in its vertical representation (Key is the 1-item while value is a list of all the transactions containing that item)
        self.finalTopK = None #for showing final results
        self.maxLevel=0 # The max length of itemsets grater than minSup
        self.heap=QuickHeap(topK) #Tok-K absolute support values heap initialization
        self.itemDict=None # map item names to simple integers for better performance
        self.execution_time = None # Overall time of mining
        self.process=psutil.Process(os.getpid())
        self.maxMemoryUSS=0
        self.commitTimeout=commitTimeout

    def readDatasetFile(self):

        # Dataset traversed once only!
        with open(self.dataset_file, encoding='utf-8-sig') as f:

            # Vertical dataset representation (temp)
            vR={}
            # Ensures the uniquity of items (temp)
            iSet=set()
            # The integer value given to each item
            itemIndex=0
            # The Tid of each transaction
            transIndex=0
            # The overall count of items in dataset
            # transitem=0 # Uncomment for stats only 
            # The next 2 dictionaries are used to implement one bidirectional dictionary
            # The idea is to map item names to their indexes and perform better in the algorithm
            self.itemDict=dict()
            itemDictReversed=dict()
            b1=t.time() # start of reading
            for line in f:
                for item in line.strip().split(sep=self.delimiter):
                    # transitem+=1 # Uncomment for stats only
                    if item not in iSet:
                        itemIndex+=1
                        self.itemDict[itemIndex]=item
                        itemDictReversed[item]=itemIndex
                        vR[(itemIndex,)]=[transIndex]
                        iSet.add(item)
                    else:
                        vR[(itemDictReversed[item],)].append(transIndex)
                transIndex+=1
            
            # statistics
            self.num_of_transactions=transIndex
            self.itemCount=itemIndex
            # self.TransitemCount=transitem # Uncomment for stats only

        item1TopK, self.min_count = self.InitialTopKFI(vR)

        # Initializes the quick Heap with brute passing its first list of support values
        self.heap.initialFill(list(item1TopK.values()))

        # Get rid off the 1-itemsets that are non frequent based on the TopK value
        vR = {key: vR[key] for key in item1TopK if key in vR}

        b3=t.time()
        print(f"Read dataset Time: {(b3-b1):.3f} Seconds")

        if self.bitSetMode:

            # Parallel processing
            with ProcessPoolExecutor() as executor:
                # Map each dictionary value to the costly operation
                partialParallelOperation = partial(parallelBitSetOp)
                # result_partial = list(executor.map(partialParallelOperation, vR.values()))
                vBitSet = {key: result for key, result in zip(vR.keys(), executor.map(partialParallelOperation, vR.values()))}

            # Single core processing
            # vBitSet=dict()
            # for key, value in vR.items():
            #     vBitSet[key] = _bitPacker(value)

            self.data=vBitSet
        else:
            self.data = vR
        
        print(f"bitset transformation Time: {(t.time()-b3):.3f} Seconds")

        return item1TopK


    def InitialTopKFI(self, vR):
        ### It works only for the first 1-item itemSets!!!

        # The procedure returns the dictionary of the first topK 1-Item ItemSets form the set of itemsets with their support in descending order
        # The count of ItemSets may differ if there are itemsets with the same minimum support which are also included
        # e.g. it may return 102 instead 100 if there are 3 itemsets with the same minSup.

        topKItemSetsList = sorted(((key, len(value)) for key, value in vR.items()), key=lambda x: x[1], reverse=True)
        
        # itemsets found so far less than TopK threshold. Return them as is and set minSup to zero
        if len(topKItemSetsList)<self.topK:
            return dict(topKItemSetsList), 0
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
            minSup=self.min_count
        else:
            minSup=mS

        return topKDict, minSup

    def getTopKFI(self, topKItemSets, level=0):
        # The procedure returns the dictionary of topK ItemSets from a given set of itemsets with their support in descending order
        # The count of ItemSets may differ if there are itemsets with the same minimum support which are also included
        # e.g. it may return 102 instead 100 if there are 3 itemsets with the same minSup.
        
        # The dictionary gets sorted by itemset's support in descending order 
        topKItemSets = dict(sorted(topKItemSets.items(), key= lambda itemset:(itemset[1], itemset[0]), reverse = True))

        # This mechanism guarantees that only the Top-K itemsets so far will be returned 
        # plus the itemsets that have equal support as the current minSup.
        topKDict=dict()
        currentLevelTopK=dict()
        supList=list()
        mS=-1
        for index, (key, value) in enumerate(topKItemSets.items()):
            if index>=self.topK-1:
                if mS==-1:
                    mS=value
                elif value!=mS:
                    break
            # The absolute topK itemsets
            topKDict[key]=value
            # the supports only list in descending order for quick heap synchronization
            supList.append(value)
            # The TopK itemsets of the current depth level.
            if len(key)==level:
                currentLevelTopK[key]=value
        if mS==-1: # The itemsets found are less than the topK threshold. The currenrt minSup is 0.
            minSup=0
        else:
            minSup=mS

        # quick heap synchronization - verification. Not necessary. 
        # It works propably and with out this line but this does not offer execution speed
        self.heap.initialFill(supList)

        return topKDict, minSup, currentLevelTopK

    def mineNextLevelDiffSet(self, initialTopK):
        # Implemented without recursion for faster implementation 
        # and less memory consumption

        # Collects the final Top-K itemsets with its support
        topKFI = {**initialTopK}
        # Represents the current level itemsets with its support
        currentLevelTopK = {**initialTopK}

        #count the items participating in itemset or alternatively the current class level
        level = 1

        while level > 0:

            # We keep only the max memory used between the stages.
            memoryUSS = self.process.memory_full_info().uss
            if self.maxMemoryUSS<memoryUSS:
                self.maxMemoryUSS=memoryUSS

            # The vertical itemset database representation for the current level ONLY!
            nextLevelData=dict()

            # Represents the next level candidate itemsets to be found with its support
            nextLevelTopK = {}

            # listOFKeys is a tuple for more efficiency in iteration with only the itemsets
            listOFKeys = tuple(currentLevelTopK.keys())

            # malliaridis 10/12/2024 (+10%)
            countKeys=len(listOFKeys)            

            # initialization of the second itemset counter
            iB = 1
            while(iB < countKeys):

                classB = listOFKeys[iB]
                # stop current iteration if classA itemset has already been above the current minSup.
                if currentLevelTopK[classB]<self.min_count:
                    break

                # initialization of the first itemset counter
                iA=0

                while (iA<iB):

                    classA = listOFKeys[iA]
                    # Gave at least 5x in chess 1000 (and not only) with intersect (7.9s vs 1.3s)
                    # Stop current iteration if any of the second itemset has already been above the current minSup.
                    if currentLevelTopK[classA]<self.min_count:
                        break

                    # Gave at least 5x in chess 1000 (and not only) with intersect (7.9s vs 1.3s)
                    # Stop current iteration if any of the second itemset has already been above the current minSup.
                    if currentLevelTopK[classB]<self.min_count:
                        break

                    # prefixA and prefixB keep the current itemset but the last item.
                    # example: if classA key is (a, b, c), prefixA keeps (a, b)
                    prefixA=classA[:-1]
                    prefixB=classB[:-1]

                    if prefixA == prefixB:

                        # (+11)
                        if level==1: #In level 1 we have tidSets
                            transactions = set(self.data[classA])-set(self.data[classB])
                        else: #In next levels we have diffSets (see paper 'Fast Vertical mining using Diffsets' page 7)
                            transactions = set(self.data[classB])-set(self.data[classA])
                        support=currentLevelTopK[classA]-len(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            #next level candidate itemset
                            # itemA = classA[-1]
                            # itemB = classB[-1]
                            key=prefixA + (classA[-1], classB[-1])

                            #add the frequent itemset to level's vertical database because it would help finding the superSet candidates.
                            nextLevelData[key] = list(transactions) #list of the transactions ion which the itemset participates
                            # self.data[key] = list(transactions) #add the frequent itemset to vertical database because it would help finding the superSet candidates.

                            # Insert itemset with its support
                            nextLevelTopK[key] = support
                            
                    iA+=1
                iB+=1

            # filtering the itemsets that are above the new current minSup threshold
            nextLevelTopK = {key: value for key, value in nextLevelTopK.items() if value >= self.min_count}

            # merge in the final topKFI the new level frequent itemsets that have support value greater than minSup threshold
            topKFI={**topKFI, **nextLevelTopK} 

            # return the absolute TopK itemsets so far
            # In currentLevelTopK, collect only the first topK items. the rest are discarded
            topKFI, self.min_count, currentLevelTopK = self.getTopKFI(topKFI,level+1)

            if not currentLevelTopK or (self.commitTimeout!=0 and t.time()-self.start>self.commitTimeout):
                level = 0 # Declares the end of procedure
            else:
                level += 1
                # We do not need to preserve the previous levels of itemset representation. Only the last one created
                # 2 orders of magnitude less memory consumption in kosarak 10000 sp bs
                self.data=nextLevelData

        return topKFI, self.min_count
    
    def mineNextLevelDiffSetBitSet(self, initialTopK):
        # Implemented without recursion for faster implementation 
        # and less memory consumption

        # Collects the final Top-K itemsets
        topKFI = {**initialTopK}
        # Represents the current level itemsets
        currentLevelTopK = {**initialTopK}

        #count the items participating in itemset or alternatively the current class level
        level = 1

        while level > 0:

            # We keep only the max memory used between the stages.
            memoryUSS = self.process.memory_full_info().uss
            if self.maxMemoryUSS<memoryUSS:
                self.maxMemoryUSS=memoryUSS

            # The vertical itemset database representation for the current level ONLY!
            nextLevelData=dict()

            # Represents the next level candidate itemsets to be found
            nextLevelTopK = {}

            # Collect only the first topK items. the rest are discarded
            # malliaridis 10/12/2024 (+10)
            listOFKeys = tuple(currentLevelTopK.keys())

            # malliaridis 10/12/2024 (+10%)
            countKeys=len(listOFKeys)

            # initialization of the second itemset counter
            iB = 1
            while(iB < countKeys):

                classB = listOFKeys[iB]
                # stop current iteration if classA itemset has already been above the current minSup.
                if currentLevelTopK[classB]<self.min_count:
                    break

                # initialization of the first itemset counter
                iA=0

                while (iA<iB):

                    classA = listOFKeys[iA]
                    # Gave at least 5x in chess 1000 (and not only) with intersect (7.9s vs 1.3s)
                    # Stop current iteration if any of the second itemset has already been above the current minSup.
                    if currentLevelTopK[classA]<self.min_count:
                        break

                    # prefixA and prefixB keep the current itemset but the last item.
                    # example: if classA key is (a, b, c), prefixA keeps (a, b)
                    prefixA=classA[:-1]
                    prefixB=classB[:-1]

                    if prefixA == prefixB:

                        # (+11)
                        if level==1: #In level 1 we have tidSets
                            # bitwise difference of 2 numbers e.g. 29 (11101) and 27 (11011) 
                            # 29 & (29 ^ 27) = 4 (00100)
                            transactions=self.data[classA]&(self.data[classA]^self.data[classB])
                            # Alternative but slower 
                            # 11101 & (~ 11011) = 4 (00100)
                            # transactions=self.data[classA]&(~self.data[classB])

                        else: #In next levels we have diffSets (see paper 'Fast Vertical mining using Diffsets' page 7)
                            transactions=self.data[classB]&(self.data[classB]^self.data[classA])
                            # Alternative but slower 
                            # transactions=self.data[classB]&(~self.data[classA])
                        support=currentLevelTopK[classA]-int.bit_count(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            #next level candidate itemset
                            # itemA = classA[-1]
                            # itemB = classB[-1]
                            key=prefixA + (classA[-1], classB[-1])

                            #add the frequent itemset to level's vertical database because it would help finding the superSet candidates.
                            nextLevelData[key] = transactions #bitSet implementation (a big integer number)

                            # Insert itemset with its support
                            nextLevelTopK[key] = support
                            
                    iA+=1
                iB+=1

            # filtering the itemsets that are abode the new current misSup thresold
            nextLevelTopK = {key: value for key, value in nextLevelTopK.items() if value >= self.min_count}

            # merge in the final topKFI the new level frequent itemsets that have support value greater than minSup threshold
            topKFI={**topKFI, **nextLevelTopK} 

            # return the absolute TopK itemsets so far
            topKFI, self.min_count, currentLevelTopK = self.getTopKFI(topKFI,level+1)

            if not currentLevelTopK or (self.commitTimeout!=0 and t.time()-self.start>self.commitTimeout):
                level = 0 # Declares the end of procedure
            else:
                level += 1
                # We do not need to preserve the previous levels of itemset representation. Only the last one created
                # 2 orders of magnitude less memory consumption in kosarak 10000 sp bs
                self.data=nextLevelData

        return topKFI, self.min_count


    def mineNextLevelIntersection(self, initialTopK):
        # Implemented without recursion for faster implementation 
        # and less memory consumption

        # Collects the final Top-K itemsets
        topKFI = {**initialTopK}
        # Represents the current level itemsets
        currentLevelTopK = {**initialTopK}

        #count the items participating in itemset or alternatively the current class level
        level = 1

        while level > 0:

            # We keep only the max memory used between the stages.
            memoryUSS = self.process.memory_full_info().uss
            if self.maxMemoryUSS<memoryUSS:
                self.maxMemoryUSS=memoryUSS

            # The vertical itemset database representation for the current level ONLY!
            nextLevelData=dict()

            # Represents the next level candidate itemsets to be found
            nextLevelTopK = {}

            # listOFKeys = tuple(currentLevelTopK.keys())[:self.topK]
            listOFKeys = tuple(currentLevelTopK.keys())

            # malliaridis 10/12/2024 (+10%)
            countKeys=len(listOFKeys)

            # initialization of the second itemset counter
            iB = 1
            while(iB < countKeys):

                classB = listOFKeys[iB]
                # stop current iteration if classA itemset has already been above the current minSup.
                if currentLevelTopK[classB]<self.min_count:
                    break

                # initialization of the first itemset counter
                iA=0

                while (iA<iB):

                    classA = listOFKeys[iA]
                    # Gave at least 5x in chess 1000 (and not only) with intersect (7.9s vs 1.3s)
                    # Stop current iteration if any of the second itemset has already been above the current minSup.
                    if currentLevelTopK[classA]<self.min_count:
                        break

                    # prefixA and prefixB keep the current itemset but the last item.
                    # example: if classA key is (a, b, c), prefixA keeps (a, b)
                    prefixA=classA[:-1]
                    prefixB=classB[:-1]

                    if prefixA == prefixB:

                        transactions=set(self.data[classA]) & set(self.data[classB])
                        support = len(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            #next level candidate itemset
                            # itemA = classA[-1]
                            # itemB = classB[-1]
                            key=prefixA + (classA[-1], classB[-1])

                            #add the frequent itemset to level's vertical database because it would help finding the superSet candidates.
                            nextLevelData[key] = list(transactions) #bitSet implementation (a big integer number)

                            # Insert itemset with its support
                            nextLevelTopK[key] = support
                            
                    iA+=1
                iB+=1
            
            # filtering the itemsets that are abode the new current misSup thresold
            nextLevelTopK = {key: value for key, value in nextLevelTopK.items() if value >= self.min_count}

            # merge in the final topKFI the new level frequent itemsets that have support value greater than minSup threshold
            topKFI={**topKFI, **nextLevelTopK} 

            # return the absolute TopK itemsets so far
            topKFI, self.min_count, currentLevelTopK = self.getTopKFI(topKFI,level+1)

            if not currentLevelTopK or (self.commitTimeout!=0 and t.time()-self.start>self.commitTimeout):

                level = 0 # Declares the end of procedure
            else:
                level += 1
                # We do not need to preserve the previous levels of itemset representation. Only the last one created
                # 2 orders of magnitude less memory consumption in kosarak 10000 sp bs
                self.data=nextLevelData

        return topKFI, self.min_count

    def mineNextLevelIntersectionBitSet(self, initialTopK):
        # Implemented without recursion for faster implementation 
        # and less memory consumption

        # Collects the final Top-K itemsets
        topKFI = {**initialTopK}
        # Represents the current level itemsets
        currentLevelTopK = {**initialTopK}

        #count the items participating in itemset or alternatively the current class level
        level = 1

        while level > 0:

            # We keep only the max memory used between the stages.
            memoryUSS = self.process.memory_full_info().uss
            if self.maxMemoryUSS<memoryUSS:
                self.maxMemoryUSS=memoryUSS

            # The vertical itemset database representation for the current level ONLY!
            nextLevelData=dict()

            # Represents the next level candidate itemsets to be found
            nextLevelTopK = {}

            #listOFKeys = list(currentLevelTopK.keys())[:self.topK]
            listOFKeys = tuple(currentLevelTopK.keys())

            # malliaridis 10/12/2024 (+10%)
            countKeys=len(listOFKeys)

            # initialization of the second itemset counter
            iB = 1
            while(iB < countKeys):

                classB = listOFKeys[iB]
                # stop current iteration if classA itemset has already been above the current minSup.
                if currentLevelTopK[classB]<self.min_count:
                    break

                # initialization of the first itemset counter
                iA=0

                while (iA<iB):

                    classA = listOFKeys[iA]
                    # Gave at least 5x in chess 1000 (and not only) with intersect (7.9s vs 1.3s)
                    # Stop current iteration if any of the second itemset has already been above the current minSup.
                    if currentLevelTopK[classA]<self.min_count:
                        break

                    # prefixA and prefixB keep the current itemset but the last item.
                    # example: if classA key is (a, b, c), prefixA keeps (a, b)
                    prefixA=classA[:-1]
                    prefixB=classB[:-1]

                    if prefixA == prefixB:

                        # bitwise intersection
                        transactions=self.data[classA] & self.data[classB]
                        # counts the bit that have 1 from the bit array of the number
                        support=int.bit_count(transactions)

                        if support >= self.min_count:

                            # recalculate the new absolute minSup value from quick heap
                            self.min_count=self.heap.insert(support)

                            #next level candidate itemset
                            # itemA = classA[-1]
                            # itemB = classB[-1]
                            key=prefixA + (classA[-1], classB[-1])

                            #+15 add the frequent itemset to level's vertical database because it would help finding the superSet candidates.
                            nextLevelData[key] = transactions #bitSet implementation (a big integer number)
                            # self.data[key] = transactions  

                            # Insert itemset with its support
                            nextLevelTopK[key] = support
                            
                    iA+=1
                iB+=1

            # filtering the itemsets that are abode the new current misSup thresold
            nextLevelTopK = {key: value for key, value in nextLevelTopK.items() if value >= self.min_count}

            # merge in the final topKFI the new level frequent itemsets that have support value greater than minSup threshold
            topKFI={**topKFI, **nextLevelTopK} 

            # return the absolute TopK itemsets so far
            topKFI, self.min_count, currentLevelTopK = self.getTopKFI(topKFI,level+1)

            if not currentLevelTopK or (self.commitTimeout!=0 and t.time()-self.start>self.commitTimeout):
                level = 0 # Declares the end of procedure
            else:
                level += 1
                # We do not need to preserve the previous levels of itemset representation. Only the last one created
                # 2 orders of magnitude less memory consumption in kosarak 10000 sp bs
                self.data=nextLevelData

        return topKFI, self.min_count


    # The main mining procedure
    def mine(self):

        self.start = t.time() #Start Time.

        initialTopK = self.readDatasetFile()  

        endRead = t.time()

        # initialTopK = self.firstTopKList()
        if self.tidSet and self.bitSetMode:
            self.finalTopK, self.min_count = self.mineNextLevelIntersectionBitSet(initialTopK)
        elif self.tidSet and not self.bitSetMode:
            self.finalTopK, self.min_count = self.mineNextLevelIntersection(initialTopK)
        elif not self.tidSet and self.bitSetMode:
            self.finalTopK, self.min_count = self.mineNextLevelDiffSetBitSet(initialTopK)
        elif not self.tidSet and not self.bitSetMode:
            self.finalTopK, self.min_count = self.mineNextLevelDiffSet(initialTopK)
        self.minSup=self.min_count/self.num_of_transactions

        end = t.time() #end Time
        self.execution_time=end-self.start

        print(f"FI Mining Time: {(end-endRead):.3f} Seconds")
        if self.execution_time>self.commitTimeout:
            print(f"Total Execution Time: {self.commitTimeout:.3f}+++ Seconds")
        else:
            print(f"Total Execution Time: {self.execution_time:.3f} Seconds")
        print(f"FIM found :{len(self.finalTopK)}")
        print(f"Rank count:{self.heap.rankCount()}")
        print(f"Absolute minSup:{self.min_count}")
        print(f"Relative minSup:{self.minSup}")
        print(f"Max Memory:{self.maxMemoryUSS}")      
        # Useful stats
        print(f"Transactions:{self.num_of_transactions}")   
        print(f"Items:{self.itemCount}")  

        # Uncomment only if self.TransitemCount has been computed in read dataset for stats
        # avg=self.TransitemCount/self.num_of_transactions 
        # print(f"Avg item size pre trans:{avg:.1f}")   
        # print(f"Dataset density:{avg/self.itemCount:.5f}") 

    def writeFIM(self, outputFile=None): #outputs the frequent itemsets in json format
        if (outputFile):
            # Convert tuple keys to strings since JSON does not support tuple keys
            # data = {", ".join(map(str, key)): value for key, value in self.finalTopK.items()}
            data = {", ".join(self.itemDict[item] for item in key): value for key, value in self.finalTopK.items()}
            with open(outputFile, "w") as file:
                json.dump(data, file, indent=4)

# implementation of the quick heap which keeps only the Top-K supports in descending order
# Quick and memory saver.
class QuickHeap:
    def __init__(self, size=10):
        self.size = size
        self.heapList = []  # Initialize an empty list
    
    def initialFill(self, initialList):
        self.heapList=initialList[:self.size]

    def insert(self, value):
        # Custom binary search to find the correct position
        high, low = 0, len(self.heapList)-1
        heapLen=low+1 #Current heap size
        if self.heapList[low] >= value:
            if self.size==low+1:
                return self.heapList[low]
            else:
                high=low+1
        else:
            while high < low:
                mid = (high + low) // 2
                if self.heapList[mid] > value:  # Reverse comparison for descending order
                    high = mid + 1
                else:
                    low = mid
        self.heapList.insert(high, value)  # Insert the item at the correct position
        # Maintain the fixed size and return the minSup
        heapLen+=1

        if heapLen > self.size:
            self.heapList.pop()  # Remove the smallest element (last in the list)
            return self.heapList[-1] # Return the last element (smallest value)            
        else: # The heap is not full
            return 0 # heap items less than the heap's size. In that case minSup is 0
        
    def rankCount(self):
        return len(set(self.heapList))

    def __str__(self):
        return "\n".join(map(str, self.heapList))
    
def _bitPacker(data):
    """
    Thank you Rage Uday Kiran (PAMI) For this code!
    :param data: it takes data as input.
    :type data: int or float
    :param maxIndex: It converts the data into bits By taking the maxIndex value as condition.
    :type maxIndex: int  

    Updated version by Malliaridis Konstantinos
    It takes a list of integers as input (data) and generates a single integer as output value (return).
    """
    packed_bits = 0
    for i in data:
        # packed_bits |= 1 << (maxIndex - i)
        # Slightly updated. for more speed (>15%). instead building the number from most significant digit we start from the left side of the number.
        # It is faster and got rid of the maxIndex presence.
        packed_bits |= 1 << i
    return packed_bits

# used in parallel computations
def parallelBitSetOp(value):
    return _bitPacker(value)
