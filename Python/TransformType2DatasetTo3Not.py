
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os


ff='2u.data' 

filepath=os.path.join('features', 'all', ff)

df = pd.read_csv(filepath, sep="\t", encoding='utf-8')

#df["user_id"]=df["user_id"].str.replace('.', '') # 43.700,00 --> 43700,00
#df["user_id"]=df["user_id"].str.replace(',', '.')      # 43700,00  --> 43700.00

# Create a pivot table to transform the DataFrame
transformed_df = pd.pivot_table(df.groupby(['user_id', 'movie_id']).size().reset_index(),
                                index='user_id',
                                columns='movie_id',
                                fill_value='?',
                                aggfunc=lambda x: 't' if len(x) > 0 else '?')

# Reset index and rename columns
transformed_df = transformed_df.reset_index().rename_axis(columns={'movie_id': 'index'})

# Get rid of tuple column ('user_id', '')
transformed_df=transformed_df.drop(columns=[('user_id', '')])

filepath=os.path.join('features', 'all', '3' + ff[1:])
transformed_df.to_csv(filepath, index=False, sep=",")

