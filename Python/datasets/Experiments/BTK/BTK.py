import sys
import time as t
import json
from functools import partial
from collections import defaultdict
import psutil
import os

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
            sI = defaultdict(int)
            dB = dict()
            Tid=0
            b1=t.time() # start of reading
            for line in f:
                Tid+=1
                dB[Tid]=[]
                for item in line.strip().split(sep=self.delimiter):
                    sI[tuple(item)] += 1
                    dB[Tid].append(tuple(item))
            # The # of transactions in dataset
            self.num_of_transactions=Tid
        sI = sorted(sI.items(), key=lambda x: x[1], reverse=True)

        # Construct-TB-Tree Step 2
        valid_elements = [item[0] for item in sI]
        valid_set = set(valid_elements)  # For fast membership checks
        # Sort and filter D1 values
        dB = {
            key: sorted(
                [item for item in value if item in valid_set],  # Filter out invalid items
                key=valid_elements.index  # Sort based on the order in valid_elements
            )
            for key, value in dB.items()
        }

        # Construct-TB-Tree Step 3,4
        self.start=0
        self.finish=0
        self.TB_Tree=dict()
        # self.TB_Tree[self.start]=['root',0,0]

        self.buildTree(dB)

        # Initialize an empty dictionary for d2
        self.BL = {}

        # Populate d2 using the data from d1
        for key, value in self.TB_Tree.items():
            BLItem = value[0]  # Extract the first element as the key for d2
            if BLItem not in self.BL:
                self.BL[BLItem] = []  # Initialize the list for this key if not already present
            self.BL[BLItem].append([value[1], key, value[2]])  # Append the required values

        # Sort d2 by the order of keys in d3
        self.BL={key:self.BL[key] for key in sorted(self.BL, key=lambda x: next(val2 for val1, val2 in sI if val1 == x), reverse=True)}
        # d2 = {key: d2[key] for key in sorted(d2, key=lambda x: d3[x])}

        # Print the resulting BL List
        print(self.BL)

        self.tabK=TabK(self.topK)

        # BTK Steps 5-10
        for item_1, support in sI:
            if support>self.tabK.threshold:
                self.tabK.insert(support,item_1)
        
        self.Candidate_gen(sI)

        print("Done!!!")

    def Candidate_gen(self,Ci):
        nextLevelC=[]
        i=0
        j=1
        while i<len(Ci):
            j=i+1
            while j<len(Ci):
                if Ci[i][1]>=self.tabK.threshold and Ci[j][1]>=self.tabK.threshold:
                    px_i=Ci[i][0][:-1]
                    px_j=Ci[j][0][:-1]
                    if px_i==px_j:
                        p=px_i + tuple(Ci[i][0][-1]) + tuple(Ci[j][0][-1])

                        pBL, count= self.intersection(self.BL[tuple(Ci[i][0][-1])], self.BL[tuple(Ci[j][0][-1])], self.tabK.threshold)
                        if pBL:
                            self.BL[p]=pBL
                            nextLevelC.append((p, count))
                j+=1
            i+=1
        
        print(nextLevelC)
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

        return R, Rcount

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

    # The main mining procedure
    def mine(self):

        self.start = t.time() #Start Time.

        self.readDatasetFile() 

        endRead = t.time()

        end = t.time() #end Time
        self.execution_time=end-self.start

        print(f"Read Dataset Time: {(endRead-self.start):.3f} Seconds")
        if self.execution_time>self.commitTimeout:
            print(f"Total Execution Time: {self.commitTimeout:.3f}+++ Seconds")
        else:
            print(f"Total Execution Time: {self.execution_time:.3f} Seconds")
        print(f"FIM found:{len(self.finalTopK)}")
        print(f"Absolute minSup:{self.min_count}")
        print(f"Relative minSup:{self.minSup}")
        print(f"Max Memory:{self.maxMemoryUSS}")       

    def writeFIM(self, outputFile=None): #outputs the frequent itemsets in json format
        if (outputFile):
            # Convert tuple keys to strings since JSON does not support tuple keys
            # data = {", ".join(map(str, key)): value for key, value in self.finalTopK.items()}
            data = {", ".join(self.itemDict[item] for item in key): value for key, value in self.finalTopK.items()}
            with open(outputFile, "w") as file:
                json.dump(data, file, indent=4)
