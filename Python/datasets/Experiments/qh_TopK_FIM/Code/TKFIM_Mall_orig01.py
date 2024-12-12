#import libraries
import numpy as np
import pandas as pd
import copy
import time as t
import json

def Merge(dict1, dict2):
    #this function is responsible for merging two dictionaries
    res = {**dict1, **dict2}
    return res

class TKFIM:

    def __init__(self, dataset_file, topK, delimiter=' '):
        self.dataset_file = dataset_file
        self.minSup = None  # The relative minimum support
        self.min_count = None  # The absolute minimum support
        self.delimiter = delimiter
        self.num_of_transactions = None
        self.execution_time = None
        self.topK = topK
        #initialize variables for TKFIM algorithm
        # self.itemset = dict()
        self.data = None # for storing diffsets
        self.finalTopK = None#for showing end results
        # self.diffset = set() # is the actual diffset of an item.

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
        # This Code is changed with the above at 3/12/2024 from Malliaridis.
        # pandas dataFrame cannot manipulate in right manner transactional dataset (1-MBL type)
        # df1 = pd.read_csv(self.dataset_file, sep=self.delimiter, header=None)
        # self.num_of_transactions = df1.count(axis=0)[0]# total num of rows.
        # trx = [str(i) for i in range(1, int(df1.max().max()) + 1)]#list containing values from 0 to max value in dataframe
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
    def makePrefix(self, key):
        #this functions is responsible for generating classes i.e FBA, ABC etc
        tem_var = ""

        for i in range(0, len(key)):
            if key[i] not in tem_var:
                tem_var += key[i]
        return tem_var

    def Merge(self, dict1, dict2):
        #this function is responsible for merging two dictionaries
        res = {**dict1, **dict2}
        return res

    def GetTopKListOnly(self, firstTopKList):

        res=dict()
        mS=-1
        for index, (key, value) in enumerate(firstTopKList.items()):
            # TODO Documentation
            if index>=self.topK-1:
                if mS==-1:
                    mS=value
                elif value!=mS:    
                    break

            res[key]=value

        # res=dict(list(firstTopKList.items())[:self.topK])
        ##################################################
        # This Code is changed with the above at 3/12/2024 from Malliaridis.
        # res = {}
        # topKCount = 1
        # for k,v in firstTopKList.items():
        #     if v not in res.values():
        #         topKCount += 1
        #     if topKCount<=self.topK:
        #         res[k] = v
        #     else:
        #         break

        return res

    def firstTopKList(self):
        itemset = {} # 
        for k,v in self.data.items():
            c=len(v)
            itemset[k] = c

        # itemset = sorted(itemset.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
        # firstTopKList = {}
        # for k,v in itemset:
        #     firstTopKList[k] = v
        # Correction Malliaridis 3/12/2024
        firstTopKList = {k: v for k, v in sorted(itemset.items(), key=lambda item: item[1], reverse=True)}

        firstTopKList = self.GetTopKListOnly(firstTopKList)
        itemset.clear()

        return firstTopKList

    def getFromTopK(self, initialTopK):

        itemset = {}
        topKList = {}

        # Correction 3/12/2024
        # copy the dictionary
        givenTopK = {**initialTopK}
        # givenTopK = {}
        # givenTopK = Merge(givenTopK, initialTopK)

        # get the itemset which is the last in the dectionary
        minKey = min(givenTopK, key=givenTopK.get)
        # get the smallest support from the above itemset
        smallestK = givenTopK[minKey]
        itemCount =  int(1)

        while itemCount > 0:

            k = int(0)

            listOFKeys = list(givenTopK.keys())
            # print(f"itemset of {i}\t {listOFKeys}")
            while(k < len(listOFKeys)):
                k1 = int(k + 1)
                while (k1 < len(listOFKeys)):

                    firstClass = listOFKeys[k]
                    secondClass = listOFKeys[k1]

                    if len(firstClass) <= 2:
                        diffset = list(set(self.data[firstClass]) - set(self.data[secondClass]))
                        support = len(self.data[firstClass]) - len(diffset)
                        key = firstClass +"," + secondClass

                        # Correction 3/1/2024
                        # transactions = [ele for ele in set(self.data[firstClass]) if ele not in diffset]
                        # 4x faster the below than the above in chess.dat at least!
                        transactions = list(set(self.data[firstClass]))
                        for each in set(diffset):
                            transactions.remove(each)

                        if support >= smallestK:
                            self.data[key] = transactions #add class alongside diffset in data for upcoming classes
                            itemset[key] = support
                        else:
                            break

                    else:
                        prefixA = firstClass.split(",")
                        prefixB = secondClass.split(",")

                        # if prefixA==['52','29','40','60','62']:
                        #     print("Ok!")
                        if prefixA==['58','52','29','40','60','62']:
                            print("OK!")

                        length_of_classes = len(prefixA)-1

                        itemA = prefixA.pop(length_of_classes)
                        itemB = prefixB.pop(length_of_classes)

                        if prefixA == prefixB:

                            items = [itemA, itemB]

                            key = prefixA + items
                            key = ",".join(key)

                            diffset = list(set(self.data[firstClass]) - set(self.data[secondClass]))
                            support = len(self.data[firstClass]) - len(diffset)

                            # if support==2845:
                            #     print(key)


                            # Correction 3/1/2024
                            # transactions = [ele for ele in set(self.data[firstClass]) if ele not in diffset]
                            # 4x faster the below than the above!
                            transactions = list(set(self.data[firstClass]))
                            for each in set(diffset):
                                transactions.remove(each)


                            if support >= smallestK:
                                self.data[key] = transactions #add class alongside diffset in data for upcoming classes
                                itemset[key] = support
                            elif support < smallestK:
                                break

                    k1 += 1

                k+=1

            itemset = sorted(itemset.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

            topKCount = int(0)
            for k,v in itemset:
                if v not in topKList.values():
                    topKCount += 1
                if topKCount<=self.topK:
                    topKList[k] = v

            topKList = self.Merge(initialTopK, topKList)
            topKList = dict(sorted(topKList.items(), key= lambda kv:(kv[1], kv[0]), reverse = True))
            # print("############# Top K List After ############")
            #print(topKList)
            topKList = self.GetTopKListOnly(topKList)
            #print(topKList)
            topKList = dict(sorted(topKList.items(), key= lambda kv:(kv[1], kv[0]), reverse = True))
            #print(topKList)\
            minKey = min(topKList, key=topKList.get)
            smallestK = topKList[minKey]# for reset smallest K

            # print(f"Itemset: \t{itemset}")
            # print(len(itemset))
            if(len(itemset) == 0):
                itemCount = 0
            else:
                itemCount += 1

            # print(f"Item Count \t {itemCount}")
            givenTopK.clear()
            itemset = dict(itemset)
            givenTopK = copy.deepcopy(itemset)
            # print(itemset)
            itemset.clear()
            
        return smallestK, topKList

    def writeFIM(self, outputFile=None):
        if (outputFile):
            # Write the dictionary to a file in pretty JSON format
            with open(outputFile, "w") as file:
                json.dump(self.finalTopK, file, indent=4)

    def mine(self):

        start = t.time()#Start Time.

        initialTopK = self.firstTopKList()

        self.min_count, self.finalTopK = self.getFromTopK(initialTopK)
        self.minSup=self.min_count/self.num_of_transactions

        end = t.time()#Final Time
        self.execution_time=end - start

        # if self.

        # print(initialTopK)
        print(f"\nTotal Execution Time: {self.execution_time} Seconds")
        print(f"FIM found:{len(self.finalTopK)}")
        print(f"Absolute minSup:{self.min_count}")
        print(f"Relative minSup:{self.minSup}")
