import csv
import time as t
from math import ceil
from bitarray import bitarray
import json
import os
import psutil
import sys


class BMCTreeNode:
    """
    The node in the BMC tree.

    Note: To get more information about the fields, refer to the supporting paper.

    Attributes: 
        item (int): The item (really the index of item) which is registered in this node.
        count (int): The number of transactions reached to this node.
        bitmap_code (bitarray): The bitmap representation of itemset registered from root to this node.
            children (dict): The list of children of this node.
            This dictionary maps each child item to child node for speeding up
            accessing to the child node by its item.
            child.item ==> child
    """

    def __init__(self, item, count, bitmap_code):
        self.item = item
        self.count = count
        self.bitmap_code = bitmap_code
        self.children = dict()

    def get_child_registering_item(self, item):
        """
        Return the child which registers the specified item.
        If does not exist such child, then return None.

        Args:
            item (int): The item (really the index of item).

        Returns:
            The BMCTreeNode that is child of this node and registers item.
        """
        return self.children.get(item)

    def add_child(self, child):
        self.children[child.item] = child

    def __repr__(self):
        return f'{self.item}:{self.count}->{self.bitmap_code}'


class FrequentItemsetTreeNode:
    def __init__(self):
        self.item = None
        self.count = 0
        self.children = []
        self.NegNodeSet = []

    def __repr__(self):
        return f'{self.item}'


def clean_BMC_tree(root):
    """
    Delete two fields item and children from the root and all of its descendants.

    Args:
        root (BMCTreeNode): The root of sub-tree
    """
    for item, child in root.children.items():
        clean_BMC_tree(child)
    del root.item
    del root.children


class HTKnegFIN:
    def __init__(self, dataset_file, topK, output_file, delimiter=' ', memorySave=True, commitTimeout=0):
        self.dataset_file = dataset_file
        self.output_file = output_file
        self.delimiter = delimiter
        self.num_of_transactions = None
        self.F1 = None
        self.item_to_NodeSet = None
        self.memorySave = memorySave 

        # HTKnegFIN 22/1/2025 new properties
        self.num_of_candidate_FI = 0
        self.min_count = 1  # The absolute minimum support initially set to 1 - the lowest value
        self.topK = topK #User defined Top-K threshold
        self.finalTopK=dict() #Dictinary with the FI mined
        self.maxMemoryUSS = 0 # Keep the maximum memory used'
        self.execution_time = 0 # The overall execution time
        self.startTime = 0 #The time of mining beggining
        self.commitTimeout=commitTimeout
        self.heap=QuickHeap(topK) #Tok-K absolute support values heap initialization

    #Sub borrowed of the HTK-Miner 22/1/2025
    def getTopKFI(self, topKItemSets):
        # The procedure returns the dictionary of topK ItemSets from a given set of itemsets with their support in descending order
        # The count of ItemSets may differ if there are itemsets with the same minimum support which are also included
        # e.g. it may return 102 instead 100 if there are 3 itemsets with the same minSup.
        
        # The dictionary gets sorted by itemset's support in descending order 
        topKItemSets = dict(sorted(topKItemSets.items(), key= lambda itemset:(itemset[1], itemset[0]), reverse = True))

        # This mechanism guarantees that only the Top-K itemsets so far will be returned 
        # plus the itemsets that have equal support as the current minSup.
        topKDict=dict()
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
        if mS==-1: # The itemsets found are less than the topK threshold. The currenrt minSup is 1.
            minSup=1
        else:
            minSup=mS

        # quick heap synchronization
        self.heap.initialFill(supList)

        return topKDict, minSup

    def __find_F1(self):
        """
        Scanning DB to find F1, the set of frequent items.
        """
        item_name_to_count = {}  # Holds the count of each item
        with open(self.dataset_file, encoding='utf-8-sig') as file_input:
            self.reader = csv.reader(file_input, delimiter=self.delimiter)
            self.num_of_transactions = 0
            for transaction in self.reader:
                self.num_of_transactions += 1
                for item_name in transaction:
                    item_count = item_name_to_count.setdefault(item_name, 0)
                    item_name_to_count[item_name] = item_count + 1

        process = psutil.Process(os.getpid())
        memoryUSS = process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS

        item_name_to_count.pop('', None)  # Removing the empty item_name if exists.
        self.itemCount=len(item_name_to_count)

        # return the absolute TopK itemsets so far and the current min_count 
        # HTKnegFIN 22/1/2025
        # self.min_count = ceil(self.num_of_transactions * self.minSup)
        self.F1, self.min_count = self.getTopKFI(item_name_to_count)

        # Removing infrequent items and making F1
        # HTKnegFIN 22/1/2025
        # self.F1 = [{'name': item_name, 'count': item_count} for (item_name, item_count) in item_name_to_count.items() if
        #             self.min_count <= item_count]
        self.F1 = [{'name': item_name, 'count': item_count} for (item_name, item_count) in self.F1.items()]
        
        # Sorting F1 in ascending order of items' count
        # HTKnegFIN 22/1/2025
        # self.F1.sort(key=lambda item: item['count'])
        # Sorting F1 in descending order of items' count because we want to exam first most frequent the 1-itemsets.
        # the opposite of what the original algorithm do
        self.F1=sorted(self.F1, key=lambda x: (-x['count'], x['name']))

        self.F1 = tuple(self.F1)  # Converting to a tuple to speed up

    def __generate_NodeSets_of_1_itemsets(self):
        """
        Generate the BMCtree.
        During generation, insert each node to the appropriate NodeSet.
        """

        # Assigning a unique index to each item.
        # From this point forward, we use the item index to refer the item
        item_name_to_item_index = {item['name']: item_index for (item_index, item) in enumerate(self.F1)}
        # Holds the NegNodeSet of each item
        self.item_to_NodeSet = {item_index: [] for item_index in item_name_to_item_index.values()}
        # Creating and initializing the root of BMCTree
        bmc_tree_root = BMCTreeNode(item=None, count=None, bitmap_code=bitarray([False] * len(self.F1)))

        with open(self.dataset_file, encoding='utf-8-sig') as fInput:
            reader = csv.reader(fInput, delimiter=self.delimiter)
            for transaction in reader:
                # Removing infrequent items from transaction,
                # and converting frequent items in it to the corresponding indices
                transaction = [item_name_to_item_index[item_name] for item_name in transaction if
                               item_name in item_name_to_item_index]
                # Sorting the transaction in descending order of items' index
                # Please note that items' index have a direct relation with items' count

                transaction.sort(reverse=True)

                # Inserting transaction to the BMCTree
                cur_root = bmc_tree_root
                for item in transaction:
                    N = cur_root.get_child_registering_item(item)
                    if N is None:
                        bitmap_code = cur_root.bitmap_code.copy()
                        bitmap_code[item] = True
                        N = BMCTreeNode(item=item, count=0, bitmap_code=bitmap_code)
                        cur_root.add_child(N)
                        self.item_to_NodeSet[item].append(N)

                    N.count += 1
                    cur_root = N

        # After creation of the NodeSets of 1-itemset, some fields of BMCTreeNode will be unusable.
        # So, in memory save mode, two fields item and children are deleted.
        if self.memorySave:
            clean_BMC_tree(bmc_tree_root)

    def __create_root_of_frequent_itemset_tree(self):
        """"
         Create the root of frequent itemset tree and
         level 1 of frequent itemset tree and.
         This tree is not explicitly built.
         It represents the search space which is traversed in depth-first order.
        """
        root = FrequentItemsetTreeNode()

        for item in range(len(self.F1)):
            child = FrequentItemsetTreeNode()
            child.item = item
            child.count = self.F1[item]['count']
            child.NegNodeSet = self.item_to_NodeSet[item]
            root.children.append(child)
        return root

    def __create_itemsets(self, N, itemset_buffer, N_itemset_length, FIS_parent_buffer, FIS_parent_length):
        """
        Write the itemset represented by 'N',
         and all combination that can be made using this itemset and all subsets of FIS_parent,
         to the output file.
        Args:
            Similar to '__construct_frequent_itemset_tree'
        Returns:
            Write the discovered frequent itemset into the output file.
        """

        self.num_of_candidate_FI += 1

        # Get the real name (string name) of items
        itemset_string = [self.F1[itemset_buffer[i]]['name'] for i in range(N_itemset_length)]
        self.finalTopK[','.join(itemset_string)] = N.count

        # === Write all combination that can be made using this itemset and all subsets of FIS_parent
        if FIS_parent_length > 0:
            # Generate all subsets of the node list except the empty set
            max = 1 << FIS_parent_length
            for i in range(1, max):
                # Get the real name of items

                itemset_string = [self.F1[itemset_buffer[i]]['name'] for i in range(N_itemset_length)]
                # We create a new subset
                # Check if the j bit is set to 1. #isSet = i & (1 << j)
                subsetString = [self.F1[FIS_parent_buffer[j]]['name'] for j in range(FIS_parent_length) if
                                (i & (1 << j)) > 0 and i!=j]
                
                  # Concatenate the itemset with the subset
                itemset_string.extend(subsetString)
                self.finalTopK[','.join(itemset_string)] = N.count

                self.num_of_candidate_FI += 1

    def __construct_frequent_itemset_tree(self, N, itemset_buffer, N_itemset_length, N_right_siblings,
                                          FIS_parent_buffer,
                                          FIS_parent_length):
        """
         This is a recursive method which is traverse the search space in depth-first order.
         It implicitly builds the itemset tree.
        Args:
            N (:obj:'FrequentItemsetTreeNode'): The current visited node in the implicit itemset tree.
            itemset_buffer (:obj:`list` of int): The buffer for storing the itemset represented by node 'N'.
                Each member of it represents an item index.
            N_itemset_length (int): Cardinality of the itemset represented by N.
                The itemset represented by N is denoted by  'N_itemset_length[0:N_itemset_length]'
            N_right_siblings (:obj:`list` of :obj:'FrequentItemsetTreeNode'):
                The sibling nodes of 'N'
            FIS_parent_buffer (:obj:`list` of int):
                The buffer for storing FIS, a set of equivalent items of the parent of 'N'.
                For more information, refer to the supporting paper.
            FIS_parent_length (): # Cardinality of FIS.

        Returns:
            Write the discovered frequent itemset into the output file.
        """
        for sibling in N_right_siblings:
            child = FrequentItemsetTreeNode()
            sum_of_NegNodeSets_counts = 0
            if N_itemset_length == 1:  # means at level 1
                for ni in N.NegNodeSet:
                    if not ni.bitmap_code[sibling.item]:
                        child.NegNodeSet.append(ni)
                        sum_of_NegNodeSets_counts += ni.count
            else:
                for nj in sibling.NegNodeSet:
                    if nj.bitmap_code[N.item]:
                        child.NegNodeSet.append(nj)
                        sum_of_NegNodeSets_counts += nj.count

            child.count = N.count - sum_of_NegNodeSets_counts
            
            if self.min_count <= child.count:

                # New command HTKnegFIN 22/1/2025
                self.min_count=self.heap.insert(child.count)

                if N.count == child.count:
                    FIS_parent_buffer[FIS_parent_length] = sibling.item
                    FIS_parent_length += 1
                else:
                    child.item = sibling.item
                    N.children.append(child)

        # Create itemset(s)
        # Altered original commands HTKnegFIN 22/1/2025
        # self.__create_itemsets(N, itemset_buffer, N_itemset_length, FIS_parent_buffer, FIS_parent_length)
        # number_of_children = len(N.children)
        # for childIndex in range(number_of_children):
        #     child = N.children[0]
        #     itemset_buffer[N_itemset_length] = child.item
        #     del N.children[0] # We delete this node since it is not used anymore.
        #     self.__construct_frequent_itemset_tree(child, itemset_buffer, N_itemset_length + 1, N.children,
        #                                            FIS_parent_buffer, FIS_parent_length)
        #With HTKnegFIN ones 22/1/2025
        if self.min_count <= N.count:
            
            t1=t.time()   
            if self.commitTimeout>0 and (t1-self.startTime)>self.commitTimeout:
                print(f"Total Execution (before __create_itemsets) Time exceeds: {self.commitTimeout}+++ Seconds!!!")
                sys.exit()

            self.__create_itemsets(N, itemset_buffer, N_itemset_length, FIS_parent_buffer, FIS_parent_length)

            number_of_children = len(N.children)
            for childIndex in range(number_of_children):
                child = N.children[0]
                itemset_buffer[N_itemset_length] = child.item
                del N.children[0] # We delete this node since it is not used anymore.
                self.__construct_frequent_itemset_tree(child, itemset_buffer, N_itemset_length + 1, N.children,
                                                    FIS_parent_buffer, FIS_parent_length)

    def writeFIM(self, outputFile=None):
        if (outputFile):
            # Write the dictionary to a file in pretty JSON format
            with open(outputFile, "w") as file:
                json.dump(self.finalTopK, file, indent=4)


    def runAlgorithm(self):

        self.startTime = t.time()
        self.__find_F1()
        process = psutil.Process(os.getpid())
        memoryUSS = process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS        

        self.__generate_NodeSets_of_1_itemsets()
        process = psutil.Process(os.getpid())
        memoryUSS = process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS        

        root = self.__create_root_of_frequent_itemset_tree()
        process = psutil.Process(os.getpid())
        memoryUSS = process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS   

        # The following buffer is used for storing frequent itemsets discovered in a depth.
        itemset_buffer = [None] * len(self.F1)
        # Cardinality of itemset.
        #The current itemset is represented by 'itemset_buffer[0:itemset_length]'.
        itemset_length = 0  # Set the itemset of root to empty

        # The following buffer is used for storing FIS, a set of equivalent items of the parent.
        # For more information, refer to the supporting paper.
        FIS_parent_buffer = [None] * len(self.F1) 
        FIS_parent_length = 0
        num_of_children = len(root.children)
        for childIndex in range(num_of_children):
            child = root.children[0]
            itemset_buffer[itemset_length] = child.item
            del root.children[0] # We delete this node since it is not used anymore.
            # Call this recursive method to traverse the search space in a depth-first order.
            self.__construct_frequent_itemset_tree(child, itemset_buffer, itemset_length + 1, root.children,
                                                   FIS_parent_buffer, FIS_parent_length)

        process = psutil.Process(os.getpid())
        memoryUSS = process.memory_full_info().uss
        if self.maxMemoryUSS<memoryUSS:
            self.maxMemoryUSS=memoryUSS        

        self.finalTopK, self.min_count = self.getTopKFI(self.finalTopK)     

        self.execution_time = t.time()-self.startTime # Total execution time of algorithm.


    # Print statistics about the latest execution of the algorithm to
    # standard output
    def printStats(self):
        if self.commitTimeout>0 and self.execution_time>self.commitTimeout:
            print(f"Total Execution Time exceeds: {self.commitTimeout}+++ Seconds!!!")
        else:
            print(f"Total Execution Time: {self.execution_time:.3f} Seconds")
        print(f"FIM found :{len(self.finalTopK)}")
        print(f'Candidate FIM found: {self.num_of_candidate_FI}')
        print(f"Rank count:{self.heap.rankCount()}")
        print(f"Absolute minSup:{self.min_count}")
        print(f"Relative minSup:{self.min_count/self.num_of_transactions}")
        print(f"Max Memory:{self.maxMemoryUSS}")      
        # Useful stats
        print(f"Transactions:{self.num_of_transactions}")   
        print(f"Items:{self.itemCount}")  
        print("HTKnegFIN Done!")

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
        if self.heapList[low] >= value:
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
        heapLen=len(self.heapList)
        if heapLen > self.size:
            self.heapList.pop()  # Remove the smallest element (last in the list)
            return self.heapList[-1] # Return the last element (smallest value)            
        else: # The heap is not full
            return 1 # heap items less than the heap's size. In that case minSup is 1
        
    def rankCount(self):
        return len(set(self.heapList))

    def __str__(self):
        return "\n".join(map(str, self.heapList))