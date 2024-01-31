
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os

filepath=os.path.join('features', 'all', '4breast-cancer-dataset.csv')

# the reading of the dataset which is in CSV format
#df = pd.read_csv(filepath)

#print(df.head())

missing_values = ["n/a", "na", "--", "?", "#"]
df = pd.read_csv(filepath, na_values = missing_values)

print(df['Year'].isnull().sum())

#column_values = df['Year'].isnull().tolist()  # Replace 'Column1' with the actual column name
#print(column_values)
#print(df['Year'])