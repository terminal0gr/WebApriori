
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os

#Declaration Section###############
ff='2dairy_dataset.csv' 
groupByItemColumn='Date'
itemColumn='Product Name'
separator=","
absentValue='N'
value='Y'
filepath=os.path.join('public', ff)
###################################

df = pd.read_csv(filepath, sep=separator, encoding='utf-8')

# Create a pivot table to transform the DataFrame
transformed_df = pd.pivot_table(df.groupby([groupByItemColumn, itemColumn]).size().reset_index(),
                                index=groupByItemColumn,
                                columns=itemColumn,
                                fill_value=absentValue,
                                aggfunc=lambda x: value if len(x) > 0 else absentValue)

# Reset index and rename columns
transformed_df = transformed_df.reset_index().rename_axis(columns={itemColumn: 'index'})

# Get rid of tuple column (groupByItemColumn, '')
transformed_df=transformed_df.drop(columns=[(groupByItemColumn, '')])

filepath=os.path.join('public', '3' + ff[1:])
transformed_df.to_csv(filepath, index=False, sep=separator)

