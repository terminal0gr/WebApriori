
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os

#Declaration Section###############
ff='2scanner_data.csv' 
groupColumn='Customer_ID'
itemColumn='SKU'
separator=","
filepath=os.path.join('public', ff)
###################################

# import to a dataFrame
dataset = pd.read_csv(filepath, sep=separator, encoding='utf-8')

# isolate only the groupColumn nad itemColumn
dataset = dataset[[groupColumn, itemColumn]]

# sort dataset by groupColumn
datasetSorted=dataset.sort_values(by=groupColumn)

TempInv=''
records=[]
setRec=set()
for index, row in datasetSorted.iterrows():
    if TempInv!=row[groupColumn]:
        if len(setRec)>1:
            records.append(sorted(setRec))
        setRec=set()
        setRec.add(str(row[itemColumn]).strip())
        TempInv=row[groupColumn]
    else:
        setRec.add(str(row[itemColumn]).strip())             
if len(setRec)>1:
    records.append(sorted(setRec))

# Convert to DataFrame
df = pd.DataFrame(records)

# Display the DataFrame
print(df)


