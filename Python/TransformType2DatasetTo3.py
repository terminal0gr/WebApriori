
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os


ff='2_L-0006_SRV2_2016.csv' 

filepath=os.path.join('features', 'all', ff)

df = pd.read_csv(filepath, sep=";", encoding='utf-8')

df["Stfartro_Id"]=df["Stfartro_Id"].str.replace('.', '') # 43.700,00 --> 43700,00
df["Stfartro_Id"]=df["Stfartro_Id"].str.replace(',', '.')      # 43700,00  --> 43700.00

# Create a pivot table to transform the DataFrame
transformed_df = pd.pivot_table(df.groupby(['Stfartro_Id', 'Κωδικός Είδους']).size().reset_index(),
                                index='Stfartro_Id',
                                columns='Κωδικός Είδους',
                                fill_value='0',
                                aggfunc=lambda x: 1 if len(x) > 0 else 0)

# Reset index and rename columns
transformed_df = transformed_df.reset_index().rename_axis(columns={'Κωδικός Είδους': 'index'})

# Get rid of tuple column ('Stfartro_Id', '')
transformed_df=transformed_df.drop(columns=[('Stfartro_Id', '')])

filepath=os.path.join('features', 'all', '3' + ff[1:])
transformed_df.to_csv(filepath, index=False, sep=" ")

