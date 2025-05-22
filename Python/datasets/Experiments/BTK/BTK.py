import sys
import time as t
import json
from functools import partial
from collections import defaultdict
import psutil
import os
from itertools import chain, combinations

class TabK:
    def __init__(self, max_size):
        """
        Initialize the TabK object with a fixed size.
        """
        self.max_size = max_size
        self.data = defaultdict(list)  # Dictionary to hold support as keys and itemsets as values

    def _get_sorted_keys(self):
        """
        Return the sorted keys in descending order of support.
        """
        return sorted(self.data.keys(), reverse=True)

    @property
    def threshold(self):
        """
        Return the threshold (support of the last record).
        """
        sorted_keys = self._get_sorted_keys()
        if len(sorted_keys) < self.max_size:
            return 0  # No threshold if the table is not full
        return sorted_keys[-1]

    def insert(self, support, itemset):
        """
        Insert a new itemset with its support into the TabK.
        """
        # If the support is below the current threshold, discard the itemset
        if support < self.threshold:
            return
        
        # If the support already exists, append the itemset to the existing list
        if support in self.data:
            self.data[support].append(itemset)
        else:
            # Otherwise, create a new record for this support
            self.data[support] = [itemset]

        # Sort the data by support and ensure size constraints
        self._trim_to_size()

    def _trim_to_size(self):
        """
        Trim the TabK to ensure it does not exceed the maximum size.
        """
        sorted_keys = self._get_sorted_keys()
        
        # If the size exceeds the maximum, remove the lowest support records
        while len(sorted_keys) > self.max_size:
            lowest_support = sorted_keys[-1]
            del self.data[lowest_support]
            sorted_keys = self._get_sorted_keys()

    def __repr__(self):
        """
        Provide a string representation of the TabK for easy debugging.
        """
        sorted_data = [(support, self.data[support]) for support in self._get_sorted_keys()]
        return '\n'.join(f"{support}: {', '.join(map(str, itemsets))}" for support, itemsets in sorted_data)


class BTK: 

    def __init__(self, dataset_file, topK, delimiter=' ', commitTimeout=0):

        # Construct-TB-Tree step 4
        self.start=0
        self.finish=0
        self.TB_Tree=dict()
        self.BL=dict()
        self.topK=topK
        self.sI=None
        self.dB=None
        self.finalTopK=0

        self.dataset_file = dataset_file
        self.minSup = None  # The relative minimum support
        self.min_count = 0  # The absolute minimum support 
        self.delimiter = delimiter 
        self.num_of_transactions = None 
        self.execution_time = None # Overall time of mining
        self.process=psutil.Process(os.getpid())
        self.maxMemoryUSS=0
        self.commitTimeout=commitTimeout

    def readDatasetFile(self):

        # Construct-TB-Tree Step 1
        with open(self.dataset_file, encoding='utf-8-sig') as f:
            # 1Item itemsets with their support
            self.sI = defaultdict(int)
            self.dB = dict()
            Tid=0
            for line in f:
                Tid+=1
                self.dB[Tid]=[]
                for item in line.strip().split(sep=self.delimiter):
                    self.sI[(item,)] += 1
                    self.dB[Tid].append((item,))
            # The # of transactions in dataset
            self.num_of_transactions=Tid

    def TB_Tree_Construction(self):
        self.sI = sorted(self.sI.items(), key=lambda x: x[1], reverse=True)

        # Construct-TB-Tree Step 2
        valid_elements = [item[0] for item in self.sI]
        valid_set = set(valid_elements)  # For fast membership checks
        # Sort and filter D1 values
        self.dB = {
            key: sorted(
                [item for item in value if item in valid_set],  # Filter out invalid items
                key=valid_elements.index  # Sort based on the order in valid_elements
            )
            for key, value in self.dB.items()
        }

        # Construct-TB-Tree Step 3,4
        self.start=0
        self.finish=0
        self.TB_Tree=dict()

        self.buildTree(self.dB)

    def BL_Construction(self):
        # Initialize The B-list (BL)
        self.BL = {}
        
        for key, value in self.TB_Tree.items():
            BLItem = value[0]  
            if BLItem not in self.BL:
                self.BL[BLItem] = []  # Initialize the list for this key if not already present
            self.BL[BLItem].append([value[1], key, value[2]])  # Append the required values

        # BL List is sorted in descending order of their current rank
        self.BL={key:self.BL[key] for key in sorted(self.BL, key=lambda x: next(val2 for val1, val2 in self.sI if val1 == x), reverse=True)}

    def itemset_Construction(self):
        self.tabK=TabK(self.topK)

        # BTK Steps 5-10
        tempSI=[]
        for item_1, support in self.sI:
            if support>self.tabK.threshold:
                self.tabK.insert(support,item_1)
                tempSI.append((item_1,support,))
            else:
                break

        # BTK Steps 11-13    
        self.sI=tempSI
        self.Candidate_gen(self.sI)

        # BTK Steps 14-18
        for sup, fiList in self.tabK.data.items():
            for fi in fiList:
                if fi in self.subsume:
                    # Generate all possible combinations of items in subsume
                    subsumeCombinations = chain.from_iterable(combinations(self.subsume[fi], r) for r in range(1, len(self.subsume[fi]) + 1))
                    for combination in subsumeCombinations:
                        self.tabK.insert(sup, fi + tuple(chain.from_iterable(combination)))
                    # print(f"fi={fi} == subsume {self.subsume[fi]}, sup=={sup}")
    
    def Candidate_gen(self,Ci):
        nextLevelC=[]
        i=0
        j=1
        while i<len(Ci):
            j=i+1
            while j<len(Ci):
                if Ci[i][1]>=self.tabK.threshold and Ci[j][1]>=self.tabK.threshold:
                    px_i = Ci[i][0][1:]
                    px_j = Ci[j][0][1:]
                    if px_i==px_j and not any(v1 == Ci[i][0] for v1 in self.subsume.get(Ci[j][0], [])):
                        pBL, count= self.intersection(self.BL[(Ci[i][0])], self.BL[(Ci[j][0])], self.tabK.threshold)
                        if pBL:
                            p=(Ci[i][0][0],) + (Ci[j][0][0],) + px_i
                            if Ci[j][0] in self.subsume:
                                self.subsume[p]=self.subsume.get(Ci[j][0])
                            self.BL[p]=pBL
                            self.tabK.insert(count,p)
                            nextLevelC.append((p, count))
                j+=1
            i+=1
        
        if t.time()-self.startTime>self.commitTimeout:
            print(f"Total Execution Time exceeds: {self.commitTimeout}+++ Seconds!!!")
            sys.exit()

        
        if nextLevelC:
            self.Candidate_gen(nextLevelC)

                
    def intersection(self, BLy, BLx, threshold):
        i=0
        j=0
        Rcount=0
        R=[]
        C1=self.BLItemSup(BLx)
        C2=self.BLItemSup(BLy)
        s=1 # a parameter to determine at a step, the avoided node belongs to BLx, or BLy
        while i<len(BLx) and j<len(BLy):
            if BLx[i][1]>BLy[j][1]: #start
                if BLx[i][2]<BLy[j][2]: #finish
                    s=0 # reset flag
                    if len(R)>0 and R[len(R)-1][1] == BLy[j][1]:
                        R[len(R)-1][0]+= BLx[i][0]
                    else:
                        B_info_code=[BLx[i][0],BLy[j][1],BLy[j][2]]
                        R.append(B_info_code)
                    Rcount+=BLx[i][0]
                    i+=1
                else:
                    C2=C2-s*BLy[j][0]
                    j+=1
                    s=1 # set flag
            else:
                C1=C1-BLx[i][0]
                i+=1
                s=1 # set flag 
            if (C1 < threshold or C2 < threshold):
                return [], 0
        # Malliaridis 6/1/2025 This check is vital for algorithm speed
        if Rcount>=threshold:
            return R, Rcount
        else:
            return [], 0
        

    def BLItemSup(self,BLItem):
        if BLItem:
            return sum(Bn[0] for Bn in BLItem)
        return 0

    def buildTree(self, dB):
        prefix = {}
        for value in dB.values():
            if value:  # Ensure the list is non-empty
                prefix[value[0]] = prefix.get(value[0], 0) + 1

        # Construct-TB-Tree step 5
        for pKey, pValue in prefix.items():
            self.start+=1
            currentTreeStart=self.start
            self.TB_Tree[currentTreeStart]=[pKey,pValue,0]
            prefixFiltered = {key: value[1:] for key, value in dB.items() if value[:1] == [pKey]}
            self.buildTree(prefixFiltered)
            self.finish+=1
            self.TB_Tree[currentTreeStart][2]=self.finish

    def Find_Subsume(self):
        self.subsume={}
        for i in range(1,len(self.sI)):
            for j in range(i-1,-1,-1):
                if self.sI[i][0] in self.subsume:
                    if any(val == self.sI[j][0] for val in self.subsume[self.sI[i][0]]):
                        continue
                if self.check_Subsume(self.BL[self.sI[i][0]], self.BL[self.sI[j][0]]):
                    if self.sI[i][0] not in self.subsume:
                        self.subsume[self.sI[i][0]] = []  # Initialize the list of subsumes
                    self.subsume[self.sI[i][0]].append(self.sI[j][0])  # Append the subsume
                    if self.sI[j][0] in self.subsume:
                        for item in self.subsume[self.sI[j][0]]:
                            if item not in self.subsume[self.sI[i][0]]:
                                self.subsume[self.sI[i][0]].append(item)
                        #self.subsume[self.sI[i][0]].extend(self.subsume[self.sI[j][0]])

    def check_Subsume(self,BLx,BLy):
        i=0
        j=0
        while i<len(BLx) and j<len(BLy):
            if BLx[i][1]>BLy[j][1]: #start
                if BLx[i][2]<BLy[j][2]: #finish
                    i+=1
                else:
                    j+=1
            else:
                return False # early stopping strategy when met, return False        
        if i==len(BLx):
            return True
        return False

    # The main mining procedure
    def mine(self):

        self.startTime = t.time() #Start Time.
        self.readDatasetFile() 
        endRead = t.time()
        # We keep only the max memory used between the stages.
        memoryUSS = self.process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS
        print(f"Read Dataset Time: {(endRead-self.startTime):.3f} Seconds")
            

        self.TB_Tree_Construction()
        endTBTree = t.time()
        # We keep only the max memory used between the stages.
        memoryUSS = self.process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS
        print(f"TB-Tree construction Time: {(endTBTree-endRead):.3f} Seconds")
        if (endTBTree-self.startTime)>self.commitTimeout:
            print(f"Total Execution Time exceeds: {self.commitTimeout}+++ Seconds!!!")
            return 1


        self.BL_Construction()
        endBL = t.time()
        print(f"B-List construction Time: {(endBL-endTBTree):.3f} Seconds")
        # We keep only the max memory used between the stages.
        memoryUSS = self.process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS
        if (endBL-self.startTime)>self.commitTimeout:
            print(f"Total Execution Time exceeds: {self.commitTimeout}+++ Seconds!!!")
            return 1



        self.Find_Subsume()
        endSubsume = t.time()
        print(f"Subsume construction Time: {(endSubsume-endBL):.3f} Seconds")
        # We keep only the max memory used between the stages.
        memoryUSS = self.process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS
        if (endSubsume-self.startTime)>self.commitTimeout:
            print(f"Total Execution Time exceeds: {self.commitTimeout}+++ Seconds!!!")
            return 1

        self.itemset_Construction()
        end = t.time() #end Time
        # We keep only the max memory used between the stages.
        memoryUSS = self.process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS
            

        self.execution_time=end-self.startTime

        print(f"FI mining Time: {(end-endBL):.3f} Seconds")
        if self.execution_time>self.commitTimeout:
            print(f"Total Execution Time exceeds: {self.commitTimeout}+++ Seconds!!!")
        else:
            print(f"Total Execution Time: {self.execution_time:.3f} Seconds")
        # Count the FI mined
        # Use a set to collect unique values
        unique_values = set()
        # Add each tuple in the dictionary values to the set
        for value_list in self.tabK.data.values():
            unique_values.update(value_list)  # Add all tuples in the current list to the set
        self.finalTopK=len(unique_values)
        print(f"FIM found:{self.finalTopK}")
        self.min_count=self.tabK.threshold
        print(f"Absolute minSup:{self.min_count}")
        self.minSup=self.min_count/self.num_of_transactions
        print(f"Relative minSup:{self.minSup}")
        print(f"Max Memory:{self.maxMemoryUSS}")       

    def writeFIM(self, outputFile=None): #outputs the frequent itemsets in json format
        if (outputFile):
            data = {
                ", ".join(t): key
                for key, value_list in sorted(self.tabK.data.items(), reverse=True) 
                for t in value_list
            }  
            with open(outputFile, "w") as file:
                json.dump(data, file, indent=4)
