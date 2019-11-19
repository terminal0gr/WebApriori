#implementation of the Apriori algorithm

import sys
import csv
import os
import json
from collections import namedtuple
from itertools import combinations
from time import time
import pandas as pd
import numpy as np

# global variables section
max_rules=9999
max_items=999

# Meta informations.
__Version__ = '01.00.00 02/10/2019'
__Modificator__ = 'Malliaridis konstantinos'
__Modificator_email__= 'terminal_gr@yahoo.com'

# general purpose functions
######################
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

################################################################################
# Data structures.
################################################################################
class TransactionManager(object):
    """
    Transaction managers.
    """

    def __init__(self, transactions):
        """
        Initialize.

        Arguments:
            transactions -- A transaction iterable object
                            (eg. [['A', 'B'], ['B', 'C']]).
        """
        self.__num_transaction = 0
        self.__items = []
        self.__transaction_index_map = {}

        for transaction in transactions:
            self.add_transaction(transaction)

    def add_transaction(self, transaction):
        """
        Add a transaction.

        Arguments:
            transaction -- A transaction as an iterable object (eg. ['A', 'B']).
        """
        for item in transaction:
            if item not in self.__transaction_index_map:
                self.__items.append(item)
                self.__transaction_index_map[item] = set()
            self.__transaction_index_map[item].add(self.__num_transaction)
        self.__num_transaction += 1

    def calc_count(self, items):
        """
        Returns the number of items.
        Arguments:
            items -- Items as an iterable object (eg. ['A', 'B']).
        """
        # Empty items is supported by all transactions.
        if not items:
            return self.__num_transaction
        # Empty transactions supports no items.
        if not self.num_transaction:
            return 0
        # Create the transaction index intersection.
        sum_indexes = None
        for item in items:
            indexes = self.__transaction_index_map.get(item)
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
    def num_transaction(self):
        """
        Returns the number of transactions.
        """
        return self.__num_transaction

    @property
    def items(self):
        """
        Returns the item list that the transaction is consisted of.
        """
        return sorted(self.__items)

    @staticmethod
    def create(transactions):
        """
        Create the TransactionManager with a transaction instance.
        If the given instance is a TransactionManager, this returns itself.
        """
        if isinstance(transactions, TransactionManager):
            return transactions
        return TransactionManager(transactions)


# Ignore name errors because these names are namedtuples.
SupportRecord = namedtuple( # pylint: disable=C0103
    'SupportRecord', ('items', 'support', 'count'))
RelationRecord = namedtuple( # pylint: disable=C0103
    'RelationRecord', SupportRecord._fields + ('ordered_statistics',))
OrderedStatistic = namedtuple( # pylint: disable=C0103
    'OrderedStatistic', ('LHS', 'RHS', 'confidence', 'lift', 'conviction', 'levarage', 'LHS_count', 'LHS_support', 'RHS_count', 'RHS_support'))


################################################################################
# Inner functions.
################################################################################
def create_next_candidates(prev_candidates, length):
    """
    Returns the apriori candidates as a list.

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


def gen_support_records(transaction_manager, min_support, **kwargs):
    """
    Returns a generator of support records with given transactions.

    Arguments:
        transaction_manager -- Transactions as a TransactionManager instance.
        min_support -- A minimum support (float).

    Keyword arguments:
        max_length -- The maximum length of relations (integer).
    """
    # Parse arguments.
    max_length = kwargs.get('max_length')

    # For testing.
    _create_next_candidates = kwargs.get(
        '_create_next_candidates', create_next_candidates)
    
    # Process.
    candidates = transaction_manager.initial_candidates()
    length = 1
    while candidates:
        relations = set()
        for relation_candidate in candidates:
            count = transaction_manager.calc_count(relation_candidate)
            support = float(count/transaction_manager.num_transaction)
            if support < min_support:
                continue
                
            candidate_set = frozenset(relation_candidate)
            relations.add(candidate_set)
            
            yield SupportRecord(candidate_set, support, count)
        length += 1
        if max_length and length > max_length:
            break
        candidates = _create_next_candidates(relations, length)


def gen_ordered_statistics(transaction_manager, record):
    """
    Returns a generator of ordered statistics as OrderedStatistic instances.

    Arguments:
        transaction_manager -- Transactions as a TransactionManager instance.
        record -- A support record as a SupportRecord instance.
    """
    items = record.items
    for combination_set in combinations(sorted(items), len(items) - 1):
        LHS = frozenset(combination_set)
        RHS = frozenset(items.difference(LHS))
        LHS_count = transaction_manager.calc_count(LHS)
        RHS_count = transaction_manager.calc_count(RHS)
        LHS_support = float(LHS_count / transaction_manager.num_transaction)
        RHS_support = float(RHS_count / transaction_manager.num_transaction)                   
        confidence = (record.support / LHS_support)
        lift = confidence / RHS_support
        levarage = record.support - (LHS_support * RHS_support)
        if confidence!=1:
            conviction = (1 - RHS_support) / (1 - confidence)
        else:
            conviction = 100
            
        yield OrderedStatistic(
            frozenset(LHS), frozenset(RHS), confidence, lift, conviction, levarage, LHS_count, LHS_support, RHS_count, RHS_support)


def filter_ordered_statistics(ordered_statistics, **kwargs):
    """
    Filter OrderedStatistic objects.

    Arguments:
        ordered_statistics -- A OrderedStatistic iterable object.

    Keyword arguments:
        min_confidence -- The minimum confidence of relations (float).
        min_lift -- The minimum lift of relations (float).
    """
    
    min_confidence = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)

    for ordered_statistic in ordered_statistics:
        if ordered_statistic.confidence < min_confidence:
            continue
        if ordered_statistic.lift < min_lift:
            continue
            
        yield ordered_statistic

        
#####################################        
#Special purpose functions        
#####################################
def transform_association_rules(A_R):
    rules=[]
    for item in A_R:
        #rule=[]
        for k in range(0, len(item[3])):
            a = item[3][k][0]
            LHS = [x for x in a]
            a = item[3][k][1]
            RHS = [x for x in a]
            rule=[]
            rule.extend((LHS, RHS, item[3][k][2], item[3][k][3], item[3][k][4], item[3][k][5], item[3][k][6], item[3][k][7], item[3][k][8], item[3][k][9], item[1], item[2]))
            rules.append(rule)
    return rules
        
 
    
################################################################################
# API function.
################################################################################
def apriori(transactions, **kwargs):
    """
    Executes Apriori algorithm and returns a RelationRecord generator.

    Arguments:
        transactions -- A transaction iterable object
                        (eg. [['A', 'B'], ['B', 'C']]).

    Keyword arguments:
        min_support -- The minimum support of relations (float).
        min_confidence -- The minimum confidence of relations (float).
        min_lift -- The minimum lift of relations (float).
        max_length -- The maximum length of the relation (integer).
    """
    # Parse the arguments.
    min_support = kwargs.get('min_support', 0.1)
    min_confidence = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)
    max_length = kwargs.get('max_length', None)
    
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
        
    # For testing.
    _gen_support_records = kwargs.get(
        '_gen_support_records', gen_support_records)
    _gen_ordered_statistics = kwargs.get(
        '_gen_ordered_statistics', gen_ordered_statistics)
    _filter_ordered_statistics = kwargs.get(
        '_filter_ordered_statistics', filter_ordered_statistics)

    # Calculate supports.
    transaction_manager = TransactionManager.create(transactions)
    support_records = _gen_support_records(
        transaction_manager, min_support, max_length=max_length)
    
    # Calculate ordered stats.
    for support_record in support_records:
        
        ordered_statistics = list(
            _filter_ordered_statistics(
                _gen_ordered_statistics(transaction_manager, support_record),
                min_confidence=min_confidence,
                min_lift=min_lift,
            )            
        )
        
        if not ordered_statistics:
            continue
           
        rules_counter+=1
        if rules_counter>=max_rules:
            print('Maximum itemsets count limit reached!!!(' + str(max_rules) + ') No more rules can be found')
            break
        
        yield RelationRecord(
            support_record.items, support_record.support, support_record.count, ordered_statistics)
            

  
'''
Dataset types:
1--> Market Basket list. No header is expected, The number of columns is undefined (Default). 
     If header, then participant columns must be declared in args starting from arg[1:], 
     In arg[0] the absent of item string must be declared. If absent item is nothing then assign '' or 'nan' 
2--> Order/Invoice detail. Header line is mandatory. Number of columns is fixed, 
     arg[0] primary key column and arg[1] items column are required in *args
3--> Sparce item Dataset. Header line is mandatory. Number of columns is fixed. 
     Items columns are mandatory to be declared in args[1:].
     In arg[0] the absent of item string must be declared!!! If absent item is nothing then assign '' or 'nan' 
4--> Columns with multiple nomimal values. Header line is optional. 
     Number of columns is fixed, optional items columns are expected in case header line exists.
'''
###################################################################
# preprocessing section
###################################################################
def prepare_records(datasetName, datasetSep, datasetType, *args):

    global max_items
    filepath='datasets\\' + identity + '\\' + str(datasetType) + '\\' + datasetName
    
    if len(args)>max_items:
        print('Max column limit exceeded (' + str(max_items) + '). Only the first ' + str(max_items) + ' columns will be processed.')
        args=args[0:max_items+1]
    
    if datasetType==1:
        if len(args)==0:
            try:
                with open(filepath, mode='r') as f:
                    reader = csv.reader(f, delimiter=datasetSep)
                    return list(reader)
            except:
                print('Could not open or find dataset file!!!')
                return None

        else:
            try:
                dataset = pd.read_csv(filepath, sep=datasetSep)
            except:
                return None
                
            #use only added columns
            if len(args)>1:
                dataset = dataset[list(args[1:])]
            #pandas to list
            records=dataset.values.tolist()
            #remove nan elements from this 2-dimensional list'
            records = [[y for y in x if str(y) != args[0]] for x in records]
            return(records)
            
    elif datasetType==2:
        try:
            dataset = pd.read_csv(filepath, sep=datasetSep)
        except:
            return None

        groupCol = args[0]
        itemsCol = args[1]

        dataset = dataset[[groupCol, itemsCol]]
        
        dataset.sort_values(by=groupCol)

        TempInv=''
        records=[]
        setrec=set()
        for index, row in dataset.iterrows():
            if TempInv!=row[groupCol]:
                if len(setrec)>1:
                    records.append(sorted(setrec))
                setrec=set()
                setrec.add(str(row[itemsCol]).strip())
                TempInv=row[groupCol]
            else:
                setrec.add(str(row[itemsCol]).strip())
                

        if len(setrec)>1:
            records.append(sorted(setrec))
            
        return(records)
                
    elif datasetType==3:
    
        try:
            dataset = pd.read_csv(filepath, sep=datasetSep)
        except:
            return None
        
        dataset = dataset[list(args[1:])]
        
        #put the name of product in item#
        for arg in args[1:]:
            dataset[arg]=[str(arg) if str(x)!=args[0] else args[0] for x in dataset[arg]]
        
        #pandas to list
        records=dataset.values.tolist()
        #remove nan elements from this 2-dimensional list'
        records = [[y for y in x if str(y) != args[0]] for x in records]
        return(records)
                            
    elif datasetType==4:
        if len(args)>0:
        
            try:
                dataset = pd.read_csv(filepath, sep=datasetSep)
            except:
                return None
                
            dataset = dataset[list(args)]
            
            for arg in args:
                dataset[arg] = arg + '=' + dataset[arg].astype(str)
            
            records=dataset.values.tolist()
            return(records)
            
        else:
            with open(filepath, mode='r') as f:
                try:
                    reader = csv.reader(f, delimiter=datasetSep)
                except:
                    return None
                    
                return list(reader)            
            
    else:
        print("Unknown dataset type")


##################################################################################
# output operations
##################################################################################

def output_association_rules(association_results, sort_index, descending=True, fileName=None, outputType=1, **kwargs):
    association_results.sort(reverse=descending, key=lambda x: x[sort_index])

    records = kwargs.get('records')
    recordTime = kwargs.get('recordTime')
    rulesCount = kwargs.get('rulesCount')
    assocTime = kwargs.get('assocTime')
    
    if fileName:
        if not os.path.exists('output\\' + identity + '\\' + str(datasetType)):
            os.makedirs('output\\' + identity + '\\' + str(datasetType))
        
        if outputType==1:
            ext='.txt'
        elif outputType==2:
            ext='.json'
        else:
            ext=''
            
        file = open('output\\' + identity + '\\' + str(datasetType) + '\\' + os.path.splitext(fileName)[0] + ext,'w') 
        
    if outputType==1:        
    
        Sline='Input Parameters\n'

        #dictRules['datasetArgs'] = datasetArgs
        
        if min_support:
            Sline+='Minimum Support   :' + '{0:.3f}'.format(min_support)
        if min_confidence:
            Sline+='     Minimum confidence:' + '{0:.3f}'.format(min_confidence)  
        Sline+='\n'
        if min_lift:
            Sline+='Minimum Lift      :' + '{0:.3f}'.format(min_lift)
        if max_length:
            Sline+='     Maximum rule items:' + '{:05d}'.format(max_length)      
        Sline+='\n'
         
        if ssort:
            Sline+='Sort by '
            #sort_order
#0 by LHS, 1 by RHS, 2 by confidence, 3 by lift, 4 by conviction, 5 by LHS support, 6 by RHS support, 7 by rule support 
#negatives meaning descending
            if ssort==0:
                Sline+='LHS (body) '
            elif abs(ssort)==1:
                Sline+='RHS (head) '           
            elif abs(ssort)==2:
                Sline+='confidence '
            elif abs(ssort)==3:
                Sline+='lift '            
            elif abs(ssort)==4:
                Sline+='conviction '    
            elif abs(ssort)==5:
                Sline+='LHS support '            
            elif abs(ssort)==6:
                Sline+='RHS support '  
            elif abs(ssort)==7:
                Sline+='Rule support '  
            else:
                Sline+='Unknown ' 

            if ssort>0:
                Sline+='acsending\n'
            else:
                Sline+='descending\n'
        
        if datasetName:
            Sline+='Dataset file name :' + datasetName + '\n' 
        if datasetSep:
            Sline+='Dataset separator : ' + datasetSep + '\n' 
        if datasetType:
            Sline+='Dataset Type      :' + str(datasetType) + '\n' 
        Sline+=    'Output Type       :Plain text\n'
        if datasetArgs:
            Sline+='Dataset parameters: ' + datasetArgs + '\n' 
            
        Sline+='-----------------------------------------------------\n\n' 
        if records:
            Sline+='Records           :' + '{:06d}'.format(records)
        if recordTime:
            Sline+='   Transformation time:' + '{0:.3f}'.format(recordTime)
        Sline+='\n'
        if rulesCount:
            Sline+='Association Rules :' + '{:06d}'.format(len(association_results))
        if assocTime:
            Sline+='          Time elapsed:' + '{0:.3f}'.format(assocTime)
        Sline+='\n'
        Sline+='-----------------------------------------------------\n'
 
        if fileName:
            file.write(Sline)
        print(Sline)
        
        Vr=0
        for item in association_results:
            Vr+=1 

            #Rules numbering
            str1 = right("     " + str(Vr),4) + ") {"

            #LHS
            a = item[0]
            LHS = [x for x in a]
            for l in range(0, len(LHS)):
                str1 += LHS[l] + ", "
            if len(str1)>0:
                str1 = left(str1,len(str1)-2)

            str1 += "}([" + str(item[6]) + "]" + '{0:.3f}'.format(item[7]) + ") ==> {"

            #RHS
            a = item[1]
            RHS = [x for x in a]
            for l in range(0, len(RHS)):
                str1 += RHS[l] + ", "
            if len(str1)>0:
                str1 = left(str1,len(str1)-2)

            str1 += "}([" + str(item[8]) + "]" + '{0:.3f}'.format(item[9]) + ")"

            #output to filename
            if fileName:
                file.write(str1 + '\n')
                file.write("        Count:" + '{:05d}'.format(item[11]) +
                      "  Supp:" + '{0:.3f}'.format(item[10]) + 
                      "  Conf:" + '{0:.3f}'.format(item[2]) + 
                      "  Lift:" + '{0:.3f}'.format(item[3]) +
                      "  Conv:" + '{0:.3f}'.format(item[4]) +
                      "  Levr:" + '{0:.3f}'.format(item[5]) + '\n')
            #output to console          
            print(str1)    
            print("        Count:" + '{:05d}'.format(item[11]) +
                  "  Supp:" + '{0:.3f}'.format(item[10]) + 
                  "  Conf:" + '{0:.3f}'.format(item[2]) + 
                  "  Lift:" + '{0:.3f}'.format(item[3]) +
                  "  Conv:" + '{0:.3f}'.format(item[4]) +
                  "  Levr:" + '{0:.3f}'.format(item[5]))               
 
    elif outputType==2:
        Hlist = ['LHS', 'RHS', 'Confidence', 'Lift', 'Conviction', 'Leverage', 'LHS_Count', 'LHS_Support', 'RHS_Count', 'RHS_Support', 'Support', 'Count'] 
        dictRules = {}
        
        dictRules['min_support'] = min_support
        dictRules['min_confidence'] = min_confidence
        dictRules['min_lift'] = min_lift
        dictRules['max_length'] = max_length
        dictRules['ssort'] = ssort
        dictRules['datasetName'] = datasetName
        dictRules['datasetSep'] = datasetSep
        dictRules['datasetType'] = datasetType
        dictRules['outputType'] = outputType
        dictRules['datasetArgs'] = datasetArgs
        
        dictRules['Records'] = records
        dictRules['RecordsCreationTime'] = '{0:.3f}'.format(recordTime)
        dictRules['RulesCount'] = len(association_results)
        dictRules['RulesCreationTime'] = '{0:.3f}'.format(assocTime)
        
        dictRules['rules'] = []
        for arule in association_results:
            dictRules['rules'].append(dict(zip(Hlist, arule)))
            
        if fileName:
            json.dump(dictRules, file, indent=4)
        print(json.dumps(dictRules, indent=4)) 

    else:
        print("Unknown output type")
 
    if fileName:
        file.close()     

 

#Main Task

'''
Dataset types:
1--> Market Basket list. No header is expected, The number of columns is undefined (Default). 
     If header, then participant columns must be declared in args starting from arg[1:], 
     In arg[0] the absent of item string must be declared. If absent item is nothing then assign '' or 'nan' 
2--> Order/Invoice detail. Header line is mandatory. Number of columns is fixed, 
     arg[0] primary key column and arg[1] items column are required in *args
3--> Sparce item Dataset. Header line is mandatory. Number of columns is fixed. 
     Items columns are mandatory to be declared in args[1:].
     In arg[0] the absent of item string must be declared!!! If absent item is nothing then assign '' or 'nan' 
4--> Columns with multiple nomimal values. Header line is optional. 
     Number of columns is fixed, optional items columns are expected in case header line exists.
'''

#1--> Market Basket list. No header is expected, The number of columns is undefined (Default)
# sys.argv=['Main02.py', '79d1727987f200802593e3599119c966', 0.01, 0.2, 1.5, 4, -3, "dataset.csv", ',', '1', '2']
# sys.argv=['Main02.py', '79d1727987f200802593e3599119c966', 0.01, 0.2, 1.5, 4, -3, "dataset.csv", ',', '1', '2']
# sys.argv=['Main02.py', '79d1727987f200802593e3599119c966', 0.01, 0.2, 1.5, 4, -3, 'store_data.csv', ',', '1', '1']
# sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.2, 1.5, 4, -3, "groceries.csv", ",", "1", '2']

#1--> Market Basket list. There is a header, so the participant columns must be declared in args
# sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.2, 1.5, 4, -3, "groceries - groceries.csv", ",", "1", '2', 'nan', "Item 1","Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10", "Item 11", "Item 12", "Item 13", "Item 14", "Item 15", "Item 16", "Item 17", "Item 18", "Item 19", "Item 20", "Item 21", "Item 22", "Item 23", "Item 24", "Item 25", "Item 26", "Item 27", "Item 28", "Item 29", "Item 30", "Item 31", "Item 32"]

#sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.2, 1.5, 4, -3, "OrderDetails.csv", ";", "2", '1', "InvoiceNo", "Description"]
# sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.02, 1.0, 4, -3, "invoice.csv", ";", "2", '1', "IDInvoice", "ProduitID"]

#sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.02, 1.5, 4, -3, "grocery_timestamp.csv", ",", "3", '2', "0", "air fresheners candles", "asian foods", "baby accessories", "baby bath body care", "baby food formula", "bakery desserts", "baking ingredients", "baking supplies decor", "beauty", "beers coolers", "body lotions soap", "bread", "breakfast bakery", "breakfast bars pastries", "bulk dried fruits vegetables", "bulk grains rice dried goods", "buns rolls", "butter", "candy chocolate", "canned fruit applesauce", "canned jarred vegetables", "canned meals beans", "canned meat seafood", "cat food care", "cereal", "chips pretzels", "cleaning products", "cocoa drink mixes", "coffee", "cold flu allergy", "condiments", "cookies cakes", "crackers", "cream", "deodorants", "diapers wipes", "digestion", "dish detergents", "dog food care", "doughs gelatins bake mixes", "dry pasta", "eggs", "energy granola bars", "energy sports drinks", "eye ear care", "facial care", "feminine care", "first aid", "food storage", "fresh dips tapenades", "fresh fruits", "fresh herbs", "fresh pasta", "fresh vegetables", "frozen appetizers sides", "frozen breads doughs", "frozen breakfast", "frozen dessert", "frozen juice", "frozen meals", "frozen meat seafood", "frozen pizza", "frozen produce", "frozen vegan vegetarian", "fruit vegetable snacks", "grains rice dried goods", "granola", "hair care", "honeys syrups nectars", "hot cereal pancake mixes", "hot dogs bacon sausage", "ice cream ice", "ice cream toppings", "indian foods", "instant foods", "juice nectars", "kitchen supplies", "kosher foods", "latino foods", "laundry", "lunch meat", "marinades meat preparation", "meat counter", "milk", "mint gum", "missing", "more household", "muscles joints pain relief", "nuts seeds dried fruit", "oils vinegars", "oral hygiene", "other", "other creams cheeses", "packaged cheese", "packaged meat", "packaged poultry", "packaged produce", "packaged seafood", "packaged vegetables fruits", "paper goods", "pasta sauce", "pickled goods olives", "plates bowls cups flatware", "popcorn jerky", "poultry counter", "prepared meals", "prepared soups salads", "preserved dips spreads", "protein meal replacements", "red wines", "refrigerated", "refrigerated pudding desserts", "salad dressing toppings", "seafood counter", "shave needs", "skin care", "soap", "soft drinks", "soup broth bouillon", "soy lactosefree", "specialty cheeses", "specialty wines champagnes", "spices seasonings", "spirits", "spreads", "tea", "tofu meat alternatives", "tortillas flat bread", "trail mix snack mix", "trash bags liners", "vitamins supplements", "water seltzer sparkling water", "white wines", "yogurt"]
# sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.02, 1.5, 4, -3, "supermarket.txt", ",", "3", '1', "?", 'department1','department2','department3','department4','department5','department6','department7','department8','department9','grocery misc','department11','baby needs','bread and cake','baking needs','coupons','juice-sat-cord-ms','tea','biscuits','canned fish-meat','canned fruit','canned vegetables','breakfast food','cigs-tobacco pkts','cigarette cartons','cleaners-polishers','coffee','sauces-gravy-pkle','confectionary','puddings-deserts','dishcloths-scour','deod-disinfectant','frozen foods','razor blades','fuels-garden aids','spices','jams-spreads','insecticides','pet foods','laundry needs','party snack foods','tissues-paper prd','wrapping','dried vegetables','pkt-canned soup','soft drinks','health food other','beverages hot','health&beauty misc','deodorants-soap','mens toiletries','medicines','haircare','dental needs','lotions-creams','sanitary pads','cough-cold-pain','department57','meat misc','cheese','chickens','milk-cream','cold-meats','deli gourmet','margarine','salads','small goods','dairy foods','fruit drinks','delicatessen misc','department70','beef','hogget','lamb','pet food','pork','poultry','veal','gourmet meat','department79','department80','department81','produce misc','fruit','plants','potatoes','vegetables','flowers','department88','department89','variety misc','brushware','electrical','haberdashery','kitchen','manchester','pantyhose','plasticware','department98','stationary','department100','department101','department102','prepared meals','preserving needs','condiments','cooking oils','department107','department108','department109','department110','department111','department112','department113','department114','health food bulk','department116','department117','department118','department119','department120','bake off products','department122','department123','department124','department125','department126','department127','department128','department129','department130','small goods2','offal','mutton','trim pork','trim lamb','imported cheese','department137','department138','department139','department140','department141','department142','department143','department144','department145','department146','department147','department148','department149','department150','department151','department152','department153','department154','department155','department156','department157','department158','department159','department160','department161','department162','department163','department164','department165','department166','department167','department168','department169','department170','department171','department172','department173','department174','department175','department176','department177','department178','department179','casks white wine','casks red wine','750ml white nz','750ml red nz','750ml white imp','750ml red imp','sparkling nz','sparkling imp','brew kits/accesry','department189','port and sherry','ctrled label wine','department192','department193','department194','department195','department196','department197','department198','department199','non host support','department201','department202','department203','department204','department205','department206','department207','department208','department209','department210','department211','department212','department213','department214','department215','department216']
# sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.02, 1.5, 4, -3, "supermarket.txt", ",", "3", '1', "?", 'department1','department2','department3','department4','department5','department6','department7','department8','department9','grocery misc']

# sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.2, 1.5, 4, -3, "titanic02WithoutHeader.csv", ",", "4", '2']
# sys.argv=["Main02.py", '79d1727987f200802593e3599119c966', 0.01, 0.2, 1.5, 3, -3, "titanic02.csv", ",", "4", '2', "class", "age", "sex", "survived"]

#identity
identity=None
if len(sys.argv)>1:
	try:
		identity=str(sys.argv[1])
	except:
		sys.exit()

#min_support
min_support=0.01
if len(sys.argv)>2:
	try:
		min_support=float(sys.argv[2])
	except:
		min_support=0.01

#min_confidence
min_confidence=0.2
if len(sys.argv)>3:
	try:
		min_confidence=float(sys.argv[3])
	except:
		min_confidence=0.2

#min_lift
min_lift=1.5
if len(sys.argv)>4:
	try:
		min_lift=float(sys.argv[4])
	except:
		min_lift=1.5

#max_length	
max_length=2	
if len(sys.argv)>5:
	try:
		max_length=int(sys.argv[5])
	except:
		max_length=2
		
#sort_order
#0 by LHS, 1 by RHS, 2 by confidence, 3 by lift, 4 by conviction, 5 by LHS support, 6 by RHS support, 7 by rule support 
#negatives meaning descending
ssort=-3
if len(sys.argv)>6:
	try:
		ssort=int(sys.argv[6])
	except:
		ssort=-3 # by lift descending
		
datasetName='dataset.csv'	
if len(sys.argv)>7:
    if len(sys.argv[7])>0:
        datasetName=sys.argv[7]	

#Dataset item separator
datasetSep=','
if len(sys.argv)>8:
    if len(sys.argv[8])>0:
        datasetSep=str(sys.argv[8])


datasetType=1
if len(sys.argv)>9:
	try:
		datasetType=int(sys.argv[9])
	except:
		datasetType=1 # Default is Market Basket list

'''
#1=text file, 2=json file
#output to to both console and file if datasetName is given
'''
outputType=1
if len(sys.argv)>10:
	try:
		outputType=int(sys.argv[10])
	except:
		outputType=1 # Default is 1 print text in console.

datasetArgs=''
if len(sys.argv)>11:
    if len(sys.argv[11])>0:
	    datasetArgs=str(sys.argv[11:])
	
paramFile = open('inputparams.log', 'w') 
print("Identity      :" + str(identity), file = paramFile)
print("min_support   :" + str(min_support), file = paramFile)
print("min_confidence:" + str(min_confidence), file = paramFile)
print("min_lift      :" + str(min_lift), file = paramFile)
print("max_length    :" + str(max_length), file = paramFile)
print("SortIndex     :" + str(ssort), file = paramFile)
print("Dataset Name  :" + datasetName, file = paramFile)
print("Dataset Sep   :" + str(datasetSep), file = paramFile)
print("Dataset Type  :" + str(datasetType), file = paramFile)
print("Output Type   :" + str(outputType), file = paramFile)
print("Dataset Args  :" + str(datasetArgs), file = paramFile)
paramFile.close()  

if not identity:
    print("Unknown identity")
    sys.exit()

recordTime=time()
if len(sys.argv)>11:
    records=prepare_records(datasetName, datasetSep, datasetType, *sys.argv[11:])
else:
    records=prepare_records(datasetName=datasetName, datasetSep=datasetSep, datasetType=datasetType)
    
if records:

    recordTime=time()-recordTime

    assocTime=time()
    association_results = list(apriori(records, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift, max_length=max_length))
    association_results = transform_association_rules(association_results)
    assocTime=time()-assocTime

    descending=False
    if ssort<0:
        descending=True

    output_association_rules(association_results, sort_index=abs(ssort), descending=descending, fileName=datasetName, outputType=outputType, records=len(records), recordTime=recordTime, rulesCount=len(association_results), assocTime=assocTime)

else:
    print("Couldn't retrieve detaset records")
    
    