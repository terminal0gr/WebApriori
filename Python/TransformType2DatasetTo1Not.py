
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os

#Declaration Section###############
ff='2_L-0023.csv' 
groupColumn='OrderId'
itemColumn='Description'
separator=";"
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

# Open the file for writing
with open(os.path.join('public', '1' + ff[1:]), 'w', encoding='utf-8-sig') as f:
    # Iterate over each sublist in the data
    for sublist in records:
        # Join the elements of the sublist with a semicolon
        line = ';'.join(sublist)
        # Write the line to the file
        f.write(line + '\n')    



# Convert to DataFrame
# df = pd.DataFrame(records)
# filepath=os.path.join('public', '1' + ff[1:])
# df.to_csv(filepath, index=False, sep=separator)
# Display the DataFrame
# print(df)



