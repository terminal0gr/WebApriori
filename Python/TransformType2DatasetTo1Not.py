
import numpy as np 
import pandas as pd 
import os

#Declaration Section###############
filename='2_L-0023.csv' 
groupColumn='OrderId'
itemColumn='Description'
separator=";"
filepath=""  # Leave it blank if the file resides in the same directory. # os.path.join('public', filename)
###################################

# import to a dataFrame
dataset = pd.read_csv(filepath, sep=separator, encoding='utf-8')

# isolate only the groupColumn and itemColumn
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
with open(os.path.join('public', '1' + filename[1:]), 'w', encoding='utf-8-sig') as f:
    # Iterate over each sublist in the data
    for sublist in records:
        # Join the elements of the sublist with a semicolon
        line = ';'.join(sublist)
        # Write the line to the file
        f.write(line + '\n')    



# Convert to DataFrame
# df = pd.DataFrame(records)
# filepath=os.path.join('public', '1' + filename[1:])
# df.to_csv(filepath, index=False, sep=separator)
# Display the DataFrame
# print(df)



