from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from time import time
import pandas as pd

# Sample transactions
transactions = [
    ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
    ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
    ['b', 'f', 'h', 'j', 'o', 'p'],
    ['b', 'c', 'k', 's', 'p'],
    ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
]

# https://chatgpt.com/share/66f005dc-9a30-800b-b3d3-60500be509ae

# transactions = [
#     ['A', 'B', 'D'],
#     ['B', 'C', 'E'],
#     ['A', 'B', 'C', 'E'],
#     ['B', 'E']
# ]

transactions = [
    ['c','d','e','f','g','i'],
    ['a','c','d','e','m'],
    ['a','b','d','e','g','k'],
    ['a','c','d','h']
]

# Convert transactions to one-hot encoded DataFrame
from mlxtend.preprocessing import TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_) 

# recordTime=time()
# frequent_itemsets = apriori(df, min_support=0.6, low_memory=True, use_colnames=True)
# print(frequent_itemsets)
# recordTime=time()-recordTime
# print(recordTime)

recordTime=time()
frequent_itemsets = fpgrowth(df, min_support=0.4, use_colnames=True)
recordTime=time()-recordTime
print(frequent_itemsets)
print(recordTime)

# recordTime=time()
# ARs = association_rules(frequent_itemsets, metric="lift", min_threshold=1.5)
# recordTime=time()-recordTime
# print(recordTime)
# print(ARs)

