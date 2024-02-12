
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os


ff='2_L-0012_2023.csv'

filepath=os.path.join('features', 'all', ff)

df = pd.read_csv(filepath, sep=";", encoding='utf-8')

#dfp=df.pivot(index='Stfartro_Id', columns='Κωδικός Είδους', values='Εξαγωγές')

df["Stfartro_Id"]=df["Stfartro_Id"].str.replace('.', '') # 43.700,00 --> 43700,00
df["Stfartro_Id"]=df["Stfartro_Id"].str.replace(',', '.')      # 43700,00  --> 43700.00

# Create a pivot table to transform the DataFrame
transformed_df = pd.pivot_table(df.groupby(['Stfartro_Id', 'Κωδικός Είδους']).size().reset_index(),
                                index='Stfartro_Id',
                                columns='Κωδικός Είδους',
                                fill_value='0',
                                aggfunc='sum')

# Reset index and rename columns
transformed_df = transformed_df.reset_index().rename_axis(columns={'Κωδικός Είδους': 'index'})

# Get rid of tuple column ('Stfartro_Id', '')
transformed_df=transformed_df.drop(columns=[('Stfartro_Id', '')])


#transformed_df=transformed_df.drop(index=1)
#transformed_df["Stfartro_Id"]=transformed_df["Stfartro_Id"].astype("float").astype("int64")

filepath=os.path.join('features', 'all', '3' + ff[1:])
transformed_df.to_csv(filepath, index=False)

