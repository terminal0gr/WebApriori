#implementation of the Apriori algorithm (Apriori engine)

import sys
import os
import csv
import json
from collections import namedtuple
from itertools import combinations
from time import time
import pandas as pd
import numpy as np
import datasetAttrAutoDetectMetadata as Metadata
import Global
# global variables section
max_rules=1000
max_items=999

__Version__ = '02.00.00 28/03/2024'
__Developer__ = 'Malliaridis konstantinos'
__DeveloperEmail__= 'terminal_gr@yahoo.com'
__University__= 'International Hellenic University'

################################################################################
# Data structures.
################################################################################
class itemsetManager(object):

    def __init__(self, itemsets):
        """
        Initialization

        Arguments:
            itemsets -- A itemset iterable object
                            (example [['A', 'B', 'C'], ['B', 'C']]).
        """
        self.__num_itemset = 0
        self.__items = []
        self.__itemset_index_map = {}

        for itemset in itemsets:
            self.add_itemset(itemset)

    def add_itemset(self, itemset):
        """
        Add a itemset.

        Arguments:
            itemset -- A itemset as an iterable object (['A', 'B', 'C']).
        """
        for index,item in enumerate(itemset):
            
            #Malliaridis 15/8/2024.
            if hasHeader and datasetType==4 and 'header' in jsonData:
                item=str(jsonData['header'][index]) + '=' + str(item.strip())
            else:
                item=str(item.strip())

            if item not in self.__itemset_index_map:
                self.__items.append(item)
                self.__itemset_index_map[item] = set()
            self.__itemset_index_map[item].add(self.__num_itemset)
        self.__num_itemset += 1

    def calc_count(self, items):
        """
        Returns the number of items.
        Arguments:
            items -- Items as an iterable object (['A', 'B', 'C']).
        """
        # Empty items is supported by all itemsets.
        if not items:
            return self.__num_itemset
        # Empty itemsets supports no items.
        if not self.num_itemset:
            return 0
        # Create the itemset index intersection.
        sum_indexes = None
        for item in items:
            indexes = self.__itemset_index_map.get(item)
            if indexes is None:
                # No support for any set that contains a not existing item.
                return 0
            if sum_indexes is None:
                # Assign the indexes on the first time.
                sum_indexes = indexes
            else:
                # Calculate the intersection on not the first time.
                sum_indexes = sum_indexes.intersection(indexes)
        # Calculate and return the support.
        return len(sum_indexes)  
    
    def initial_candidates(self):
        """
        Returns the initial candidates.
        """
        return [frozenset([item]) for item in self.items]

    @property
    def num_itemset(self):
        """
        Returns the count of itemsets.
        """
        return self.__num_itemset

    @property
    def items(self):
        """
        Returns the items list that the itemset is consisted of.
        """
        return sorted(self.__items)

    @staticmethod
    def create(itemsets):
        """
        Create the itemsetManager with an itemset instance.
        If the given instance is a itemsetManager then it returns itself.
        """
        if isinstance(itemsets, itemsetManager):
            return itemsets
        return itemsetManager(itemsets)

FrequentItemset = namedtuple('FrequentItemset', ('items', 'support', 'count'))
# Association_rule = namedtuple('Association_rule', FrequentItemset._fields + ('rule_statistics',))
ruleStatistic = namedtuple('ruleStatistic', ('itemset', 'support', 'count', 'LHS', 'RHS', 'confidence', 'lift', 'conviction', 'leverage', 'LHS_count', 'LHS_support', 'RHS_count', 'RHS_support'))

################################################################################
# Inner core functions.
################################################################################
def extract_next_candidates(prev_candidates, length):
    """
    Returns the association rules candidates as a list.

    Arguments:
        prev_candidates -- Previous candidates as a list.
        length -- The lengths of the next candidates.
    """

    # Solve the items.
    item_set = set()
    for candidate in prev_candidates:
        for item in candidate:
            item_set.add(item)
    items = sorted(item_set)

    # Create the temporary candidates. These will be filtered below.
    tmp_next_candidates = (frozenset(x) for x in combinations(items, length))

    # Return all the candidates if the length of the next candidates is 2
    # because their subsets are the same as items.
    if length < 3:
        return list(tmp_next_candidates)

    # Filter candidates that all of their subsets are
    # in the previous candidates.
    next_candidates = [
        candidate for candidate in tmp_next_candidates
        if all(
            True if frozenset(x) in prev_candidates else False
            for x in combinations(candidate, length - 1))
    ]
    return next_candidates

def generate_frequent_itemsets(itemset_manager, min_support, **kwargs):
    """
    Returns a generator of support records with given itemsets.

    Arguments:
        itemset_manager -- itemsets as a itemsetManager instance.
        min_support -- A minimum support (float).

    Keyword arguments:
        max_length -- The maximum length of association_rules (integer).
    """
    # Parse arguments.
    max_length = kwargs.get('max_length')
    
    # Process.
    candidates = itemset_manager.initial_candidates()
    length = 1
    while candidates:
        association_rules = set()
        for association_rule_candidate in candidates:
            count = itemset_manager.calc_count(association_rule_candidate)
            support = float(count/itemset_manager.num_itemset)
            if support < min_support:
                continue
                
            candidate_set = frozenset(association_rule_candidate)
            association_rules.add(candidate_set)
            
            yield FrequentItemset(candidate_set, support, count)
        length += 1
        if max_length and length > max_length:
            break
        candidates = extract_next_candidates(association_rules, length)

def gen_rule_statistics(itemset_manager, itemset, **kwargs):
    """
    Returns a generator of rule statistics as ruleStatistic instances.

    Arguments:
        itemset_manager -- itemsets as a itemsetManager instance.
        itemset -- An itemset as a Supportitemset instance.
    """
 
    min_confidence = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)

    items = itemset.items
    # Check if any item from the itemset exists in excludedItems with the value of 3(excluded)
    if excludedItems is not None:
        if any(item in excludedItems and excludedItems[item] == 3 for item in items):
            return #if so exclude this itemset

    sorted_items = sorted(items)
    for base_length in range(1,len(items)):
        for combination_set in combinations(sorted_items, base_length):
            LHS = frozenset(combination_set)
            # Check if any item from LHS exists in excludedItems with the value of 2(Only in RHS)
            if excludedItems is not None:
                if any(item in excludedItems and excludedItems[item] == 2 for item in LHS):
                    continue #if so exclude this itemset

            RHS = frozenset(items.difference(LHS))
            # Check if any item from RHS exists in excludedItems with the value of 1(Only in LHS)
            if excludedItems is not None:
                if any(item in excludedItems and excludedItems[item] == 1 for item in RHS):
                    continue #if so exclude this itemset

            LHS_count = itemset_manager.calc_count(LHS)
            RHS_count = itemset_manager.calc_count(RHS)
            LHS_support = float(LHS_count / itemset_manager.num_itemset)
            RHS_support = float(RHS_count / itemset_manager.num_itemset)                   
            confidence = (itemset.support / LHS_support)
            lift = confidence / RHS_support
            leverage = itemset.support - (LHS_support * RHS_support)
            if confidence!=1:
                conviction = (1 - RHS_support) / (1 - confidence)
            else:
                conviction = 999.999
 
            if confidence < min_confidence:
                continue
            if lift < min_lift:
                continue

            yield ruleStatistic(sorted_items, itemset.support, itemset.count,
                                    frozenset(LHS), 
                                    frozenset(RHS), 
                                    confidence, lift, conviction, leverage, 
                                    LHS_count, LHS_support, RHS_count, RHS_support
                                )
        
#####################################        
#Special purpose functions        
#####################################
def transform_association_rules(A_R,RedundantType=0):
    rules=[]

    for item in [x[y] for x in A_R for y in range(0, len(x))]:
    # We don't have the initial list sorted because matchRule happens in A_R not in the created list (rules.append(rule))
    #  the next line is kept only for learning purposes
    # for item in sorted([x[y] for x in A_R for y in range(0, len(x))],key=lambda l: len(l[3]),reverse=True):

        # Interchange the antecedent and consequence case. The rule with smaller confidence is removed (support and lift are equal in this case)
        # Case 00000001
        if RedundantType & 1 == 1:
            matchRule = [x[y] for x in A_R for y in range(0, len(x)) if x[y][3]==item[4] and x[y][4]==item[3] and x[y][5]>=item[5]]
            if len(matchRule)>0:
                # Redundant do not add it to interesting association rules
                continue

        # Redundant Rules with Fixed Consequence
        # Case 00000010
        if RedundantType & 2 == 2:
            # If LHS length > 1
            if len(item[3])>1:
                # Find all the LHS length-1 sub itemsets 
                ssets = (set(x) for x in combinations(item[3], len(item[3])-1) )
                i=0
                # Count how many are the LHS length-1 sub itemsets participating to the A_R
                for c in ssets:
                    matchRule = [x[y] for x in A_R for y in range(0, len(x)) if x[y][3]==c and x[y][4]==item[4]]
                    if len(matchRule)>0:
                        i+=1
                # If LHS length-1 sub itemsets count is equal to LHS length then rule is redundant
                if i==len(item[3]):
                    # Redundant do not add it to interesting association rules
                    continue

        # Redundant Rules with Fixed Antecedent
        # Case 00000100
        if RedundantType & 4 == 4:
            # If RHS length > 1
            if len(item[4])>1:
                # Find all the RHS length-1 sub itemsets 
                ssets = (set(x) for x in combinations(item[4], len(item[4])-1) )
                i=0
                # Count how many are the RHS length-1 sub itemsets participating to the A_R
                for c in ssets:
                    matchRule = [x[y] for x in A_R for y in range(0, len(x)) if x[y][4]==c and x[y][3]==item[3]]
                    if len(matchRule)>0:
                        i+=1   
                # If RHS length-1 sub itemsets count is equal to LHS length then rule is redundant
                if i==len(item[4]):
                    # Redundant do not add it to interesting association rules
                    continue

        # non redundant. Add it to the final collection
        a = item[3]
        LHS = [x for x in a]
        a = item[4]
        RHS = [x for x in a]
        rule=[]
        # [0]:sorted_items, [1]:itemset.support, [2]:itemset.count, [3]:frozenset(LHS), [4]:frozenset(RHS), [5]:confidence, [6]:lift, [7]:conviction, [8]:leverage, [9]:LHS_count, [10]:LHS_support, [11]:RHS_count, [12]:RHS_support
        rule.extend((LHS, RHS, item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[1], item[2], item[0]))
        rules.append(rule)

    return rules
        
################################################################################
# Main Apriori engine.
################################################################################
def webApriori(itemsets, **kwargs):
    """
    Executes Apriori algorithm and returns an association rules generator.

    Arguments:
        itemsets -- A itemset iterable object
                        (eg. [['A', 'B'], ['B', 'C']]).

    Keyword arguments:
        min_support -- The minimum support of association_rules (float).
        min_confidence -- The minimum confidence of association_rules (float).
        min_lift -- The minimum lift of association_rules (float).
        max_length -- The maximum length of the association_rule (integer).
    """
    # Parse the arguments.
    min_support = kwargs.get('min_support', 0.1)
    min_confidence = kwargs.get('min_confidence', 0.2)
    min_lift = kwargs.get('min_lift', 1.5)
    max_length = kwargs.get('max_length', 4)
    
    rules_counter=0
    global max_rules

    # Check arguments.
    if min_support <= 0:
        raise ValueError('minimum support can''t be negative number!!!')
    if min_confidence <= 0:
        raise ValueError('minimum confidence can''t be negative number!!!')    
    if min_lift <= 0:
        raise ValueError('minimum lift can''t be negative number!!!') 
    if max_length < 2:
        raise ValueError('Rules max length can''t be negative number!!!') 

    # Calculate supports.
    itemset_manager = itemsetManager.create(itemsets)
    frequent_itemsets = generate_frequent_itemsets(itemset_manager, min_support, max_length=max_length)
    
    # Calculate rule stats.
    idx=0
    for frequent_itemset in frequent_itemsets:
        print(f"{idx}\t{frequent_itemset.items}\t{frequent_itemset.support}")
        idx+=1
        rule_statistics = list(gen_rule_statistics(itemset_manager, frequent_itemset, min_confidence=min_confidence, min_lift=min_lift))
        
        if not rule_statistics:
            continue  

        rules_counter+=len(rule_statistics)
        if rules_counter>=max_rules:
            print('@' + '{:04d}'.format(max_rules))
            break
        
        yield rule_statistics
            

  
'''
Dataset types:
1--> Market Basket list. There is no header. The number of columns is undefined (Default). 
2--> Order/Invoice detail. Header line is mandatory. Number of columns is fixed, 
     Group Value Column and Item Value must be declared in .metadatafile
3--> Sparse item Dataset. Header line is mandatory. Number of columns is fixed. 
     The absent value is mandatory to be declared in .metadatafile. If absent item is nothing then '' or 'nan' must be declared.
4--> Columns with multiple nominal values. Header line is optional. 
     Number of columns is fixed.
'''
###################################################################
# preprocessing section
###################################################################
def prepare_records():
    global max_items
    global groupItem
    global valueItem
    global absentValue

    try:

        if public==0:
            filepath=os.path.join('datasets', identity, datasetName)
        else:
            filepath=os.path.join('public', datasetName)

        if 'participatingItems' in jsonData:
            if len(jsonData['participatingItems'])>max_items:
                print('Max column limit exceeded (' + str(max_items) + '). Only the first ' + str(max_items) + ' of the ' + str(len(jsonData['participatingItems'])) + ' columns will be processed.')
                jsonData['participatingItems']=jsonData['participatingItems'][0:max_items+1]

        #Read the dataset from file
        dataset=Global.readDataset(filepath, sep=datasetSep, encoding='utf-8-sig', hasHeader=jsonData['hasHeader'])
        if not isinstance(dataset, pd.DataFrame):
            print(f"An error occurred: Could not read dataset! {e}")     
            sys.exit

        if int(datasetType)==1:
                    
            # #use only the columns that the user has chosen
            # if len(args)>0:
            #     dataset = dataset[list(args)]

            #pandas to list
            records=dataset.values.tolist()

            #remove nan elements from this 2-dimensional list'
            records = [[y for y in x if str(y) != 'nan'] for x in records]

            return(records)
                
        elif datasetType==2:

            if groupItem is None:
                # Grouping Column not set!
                # Set the first column as the grouping one
                groupItem=dataset.columns[0]

            if valueItem is None:
                # Value item Column not set!
                # Set the second column
                valueItem=dataset.columns[1]

            dataset = dataset[[groupItem, valueItem]]
            
            datasetSorted=dataset.sort_values(by=groupItem)

            TempInv=''
            records=[]
            setrec=set()
            for index, row in datasetSorted.iterrows():
                if TempInv!=row[groupItem]:
                    if len(setrec)>1:
                        records.append(sorted(setrec))
                    setrec=set()
                    setrec.add(str(row[valueItem]).strip())
                    TempInv=row[groupItem]
                else:
                    setrec.add(str(row[valueItem]).strip())
                    

            if len(setrec)>1:
                records.append(sorted(setrec))
                
            return(records)
                    
        elif datasetType==3:
            
            if 'participatingItems' in jsonData:
                if len(jsonData['participatingItems'])>0 and jsonData['participatingItems']!='[]':
                    dataset = dataset[jsonData['participatingItems']]
            
            #put the name of product in item#
            for arg in dataset.columns:
                dataset[arg]=[str(arg) if str(x)!=absentValue else absentValue for x in dataset[arg]]
            
            #pandas to list
            records=dataset.values.tolist()
            #remove nan elements from this 2-dimensional list in order to be transformed as a dataset type 1-MBL'
            records = [[y for y in x if str(y) !=absentValue] for x in records]
            return(records)
                                
        elif datasetType==4:
                
            if 'participatingItems' in jsonData:
                if len(jsonData['participatingItems'])>0 and jsonData['participatingItems']!='[]':
                    dataset = dataset[jsonData['participatingItems']]
                    for arg in jsonData['participatingItems']:
                        dataset[arg] = arg + '=' + dataset[arg].astype(str)
            elif hasHeader==True:
                if 'header' in jsonData:
                    if len(jsonData['header'])>0 and jsonData['header']!='[]':
                        dataset = dataset[jsonData['header']]
                        for arg in jsonData['header']:
                            dataset[arg] = arg + '=' + dataset[arg].astype(str)
            
            records=dataset.values.tolist()
            return(records)
                
        else:
            print("An error occurred: Unknown or unable to process the dataset. Its dataset type is 0 which means it can't be used for association rules mining as it can't produce intresting frequent itemsets.")
            sys.exit()

    except Exception as e:
        print(f"An error occurred: {e}")     
        sys.exit()       
     


##################################################################################
# output operations
##################################################################################

def output_association_rules(association_results, sort_index, descending=True, fileName=None, public=0, **kwargs):
    try:
         
        association_results.sort(reverse=descending, key=lambda x: x[sort_index])

        records = kwargs.get('records')
        recordTime = kwargs.get('recordTime')
        rulesCount = kwargs.get('rulesCount')
        assocTime = kwargs.get('assocTime')
        
        if fileName:

            filepath=os.path.join('output', identity)
            if not os.path.exists(filepath):
                os.makedirs(filepath)

            ext='.json'

            if public==0: #Private Dataset'
                file = open(os.path.join('output', identity, os.path.splitext(fileName)[0] + ext),'w')
            elif public==1: #Public Dataset
                publicFilePath=os.path.join('output', identity, 'p')
                if not os.path.exists(publicFilePath):
                    os.makedirs(publicFilePath)
                file = open(os.path.join('output', identity, 'p', os.path.splitext(fileName)[0] + ext),'w')
                
            Hlist = ['LHS', 'RHS', 'Confidence', 'Lift', 'Conviction', 'Leverage', 'LHS_Count', 'LHS_Support', 'RHS_Count', 'RHS_Support', 'Support', 'Count', 'FrequentItemset'] 
            dictRules = {}
            
            dictRules['min_support'] = min_support
            dictRules['min_confidence'] = min_confidence
            dictRules['min_lift'] = min_lift
            dictRules['max_length'] = max_length
            dictRules['ssort'] = ssort
            dictRules['datasetName'] = datasetName
            dictRules['redundantRemoveType'] = redundantRemoveType

            dictRules['Records'] = records
            dictRules['RecordsCreationTime'] = '{0:.3f}'.format(recordTime)
            dictRules['RulesCount'] = len(association_results)
            dictRules['RulesCreationTime'] = '{0:.3f}'.format(assocTime)
            
            dictRules['rules'] = []

            for rule in association_results:
                dictRules['rules'].append(dict(zip(Hlist, rule)))
                
            json.dump(dictRules, file, indent=4)
            print(json.dumps(dictRules, indent=4)) 
            file.close()     

        else:
            print("An error occurred: Dataset filepath not given!")
    
    except Exception as e:
        print(f"An error occurred: {e}")     
        sys.exit()       

def retrieveParticipatingItems(records=None):
    global excludedItems

    try:

        filepath=os.path.join('output', identity)
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        ext='.epi'

        if public==0: #Private Dataset'
            filepath = os.path.join('output', identity, os.path.splitext(datasetName)[0] + ext)
        elif public==1: #Public Dataset
            filepath=os.path.join('output', identity, 'p')
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filepath = os.path.join('output', identity, 'p', os.path.splitext(datasetName)[0] + ext)

        excludedItems=Global.readJSONFromFile(filepath)

        if records is None: #We want only to read excluded Items if any not to save them
            return  

        # Initialize the dictionary
        uniqueItems = {}

        # Iterate through the list and populate the dictionary
        for sublist in records:
            for index, item in enumerate(sublist):

                if hasHeader and datasetType==4 and 'header' in jsonData:
                    uniqueItem=str(jsonData['header'][index]) + '=' + str(item.strip())
                else:    
                    uniqueItem=str(item.strip())

                if uniqueItem not in uniqueItems:
                     
                    # Initialize it as a participating item
                    uniqueItems[uniqueItem] = 0

                    if excludedItems!=None:
                        if uniqueItem in excludedItems:
                            uniqueItems[uniqueItem] = excludedItems[uniqueItem]
        
                if len(uniqueItems)>max_items:
                    break

        
        if not hasHeader or datasetType in [1,2]:
            # Sorting the dictionary by keys
            uniqueItems = {key: uniqueItems[key] for key in sorted(uniqueItems)}

        print(json.dumps(uniqueItems, indent=4)) 

    except Exception as e:
        print(f"An error occurred: {e}")     
        sys.exit()              


###########
###########
###########
#Main Task#
###########
###########
###########

'''
Call arguments          
1) Identity   2) datasetName   3) public   4) callType
'''


#identity
identity=None
if len(sys.argv)>1:
    try:
        identity=str(sys.argv[1])
    except:
        print("An error occurred: Could not retrieve identity of the user!")
        sys.exit()
else:        
    print("An error occurred: User identity not given!")
    sys.exit()

if len(sys.argv)>2:
    if len(sys.argv[2])>0:
        datasetName=sys.argv[2]	
    else:
        print("An error occurred: Dataset name not given!")
        sys.exit()
else:        
    print("An error occurred: Dataset name not given!")
    sys.exit()

#0=private, 1=public
public=0
if len(sys.argv)>3:
	try:
		public=int(sys.argv[3])
	except:
		public=0 # Default is 0 private Dataset.

#0=Association rules, 1=Retrieve participating items
callType=0
if len(sys.argv)>4:
	try:
		callType=int(sys.argv[4])
	except:
		callType=0 # Default is 0 - Association rules mining.

arg1=None #In case of callType=1 it may be groupItem of datasetType 2-INV or absentValue of datasetType 3-SI'
if len(sys.argv)>5:
	try:
		arg1=sys.argv[5]
	except:
		arg1=None 

arg2=None #In case of callType=1 it may be valueItem of datasetType 2-INV'
if len(sys.argv)>6:
	try:
		arg2=sys.argv[6]
	except:
		arg2=None 

#Main Program
try:

    #Read dataset's metadatafile to retrieve its attributes. If not exists then it will AutoML create it.
    metadataInst=Metadata.Metadata()
    jsonData=metadataInst.readMetadataFile(identity, datasetName, public)
    if not {'delimiter', 'datasetType', 'hasHeader'}.issubset(jsonData):
        jsonData=metadataInst.createMetadataFile(identity, datasetName, public)
    if jsonData['datasetType']==3 and not 'absentValue' in jsonData:
        jsonData=metadataInst.createMetadataFile(identity, datasetName, public)
    
    if not 'delimiter' in jsonData:
        print("An error occurred: Could not retrieve the delimiter of the dataset!")
        sys.exit()  

    if not 'datasetType' in jsonData:
        print("An error occurred: Could not retrieve the dataset type of the dataset!") 
        sys.exit()    

    if not 'hasHeader' in jsonData:
        print("An error occurred: Could not retrieve the dataset has header or not!") 
        sys.exit() 
    elif jsonData['hasHeader'] and not 'header' in jsonData:
        print("An error occurred: Could not retrieve the dataset's header!") 
        sys.exit() 

    groupItem = None
    valueItem = None
    if jsonData['datasetType']==2:
        if callType==0: #AR Mining
            if 'groupItem' in jsonData:
                groupItem=jsonData['groupItem']
            if 'valueItem' in jsonData:
                valueItem=jsonData['valueItem']
        elif callType==1: #retrieveParticipatingItems
            if arg1 is not None:
                groupItem=arg1
            elif 'groupItem' in jsonData:
                groupItem=jsonData['groupItem']
            if arg2 is not None:
                valueItem=arg2
            elif 'valueItem' in jsonData:
                valueItem=jsonData['valueItem']

    if jsonData['datasetType']==3:
        if callType==0: #AR Mining
            if 'absentValue' in jsonData:
                absentValue=jsonData['absentValue']
            else:    
                print("An error occurred: Could not retrieve the absent value of 3-SI dataset!")
                sys.exit()  
        elif callType==1: #retrieveParticipatingItems
            if arg1 is not None:
                absentValue=arg1
            elif 'absentValue' in jsonData:
                absentValue=jsonData['absentValue']
            else:    
                print("An error occurred: Could not retrieve the absent value of 3-SI dataset!")
                sys.exit()   

    datasetSep=jsonData['delimiter']
    if datasetSep=='{TAB}':
        datasetSep='\t'

    datasetType=int(jsonData['datasetType'])
    hasHeader=bool(jsonData['hasHeader'])

    min_support=0.01
    if 'min_support' in jsonData:
        min_support=jsonData['min_support']

    min_confidence=0.2
    if 'min_confidence' in jsonData:
        min_confidence=jsonData['min_confidence']

    min_lift=1.5
    if 'min_lift' in jsonData:
        min_lift=jsonData['min_lift']

    max_length=4
    if 'max_length' in jsonData:
        max_length=jsonData['max_length']

    #sort_order
    #0 by LHS, 1 by RHS, 2 by confidence, 3 by lift, 4 by conviction, 5 by LHS support, 6 by RHS support, 7 by rule support 
    #negatives meaning descending
    ssort=-3
    if 'ssort' in jsonData:
        ssort=jsonData['ssort']

    '''
    bitwise 0 non redundant removal
    bitwise 1 Interchange the antecedent/LHS and consequence/RHS case 
    bitwise 2 Redundant Rules with Fixed Consequence/RHS
    bitwise 4 Redundant Rules with Fixed Antecedent/LHS
    #output to to both console and file if datasetName is given
    '''
    redundantRemoveType=0 
    if 'redundantRemoveType' in jsonData:
        redundantRemoveType=jsonData['redundantRemoveType']

    ssort=-3
    if 'ssort' in jsonData:
        ssort=jsonData['ssort']

    participatingItems=[]
    if 'participatingItems' in jsonData:
        participatingItems=jsonData['participatingItems'] 

    #Time starts here
    # recordTime: The time of reading and transforming adequally the dataset for use in ARM
    #################
    recordTime=time()
    #################  

    records=prepare_records()
        
    if records:
        
        # Retrieve the current participating Item List in JSON format.
        excludedItems={}
        if callType==1:
            retrieveParticipatingItems(records)
            sys.exit()
        else:
            retrieveParticipatingItems()

        recordTime=time()-recordTime

        descending=False
        if ssort<0:
            descending=True

        # assocTime: The time of creating the frequent itemsets and ARs plus the time for the adquate transformation for the results.
        #################
        assocTime=time()
        ################# 

        if callType==0: # Apriori Algorithm

            association_results = list(webApriori(records, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift, max_length=max_length))
            association_results = transform_association_rules(association_results,redundantRemoveType)
            
        if callType==2: # FPGrowth Algorithm
            # Convert transactions to one-hot encoded DataFrame
            from mlxtend.preprocessing import TransactionEncoder
            from mlxtend.frequent_patterns import fpgrowth, association_rules

            te = TransactionEncoder()
            te_ary = te.fit(records).transform(records)
            df = pd.DataFrame(te_ary, columns=te.columns_)

            # Find frequent Itemsets
            frequent_itemsets = fpgrowth(df, min_support=min_support, use_colnames=True)
            # print(frequent_itemsets)

            # Find Association Rules
            ARs = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)

            #Delete the column
            ARs = ARs.drop('zhangs_metric', axis=1) 
            #Rename the columns to fit with the need of the frontend
            ARs=ARs.set_axis(['LHS', 'RHS', 'LHS_Support', 'RHS_Support', 'Support', 'Confidence', 'Lift', 'Leverage', 'Conviction'], axis=1) 
            #Compute LHS_Count, RHS_Count, Count from support, because are not contained if mlxtend code.
            ARs['LHS_Count']=(ARs['LHS_Support']*len(records)).round().astype(int)
            ARs['RHS_Count']=(ARs['RHS_Support']*len(records)).round().astype(int)
            ARs['Count']=(ARs['Support']*len(records)).round().astype(int)
            #Rearrange the columns to fit with the need of the frontend
            ARs = ARs[['LHS', 'RHS', 'Confidence', 'Lift', 'Conviction', 'Leverage', 'LHS_Count', 'LHS_Support', 'RHS_Count', 'RHS_Support', 'Support', 'Count']]
            ARs['LHS']=ARs['LHS'].apply(list)
            ARs['RHS']=ARs['RHS'].apply(list)
            association_results=ARs.values.tolist()

        ##########################
        assocTime=time()-assocTime
        ##########################

        # print(association_results)
        output_association_rules(association_results, sort_index=abs(ssort), descending=descending, fileName=datasetName, public=public, records=len(records), recordTime=recordTime, rulesCount=len(association_results), assocTime=assocTime)


    else:
        print("An error occurred: Could not retrieve records capable for frequent itemsets or Association Rules Mining")
    
except Exception as e:
    print(f"An error occurred: {e}")     
    sys.exit()       


    
     