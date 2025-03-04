import os
import sys
import pandas as pd
import skmine
from skmine.datasets.utils import describe

# Add two levels up to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('ARM'), '..', '..')))

import Global

##################################
#Declaration Section
##################################
##################################

filepath=os.path.join('accidents.dat')
# filepath=os.path.join('chess.dat')
# filepath=os.path.join('connect.dat')
# filepath=os.path.join('kosarak.dat') #10 minutes
# filepath=os.path.join('mushroom.dat')
# filepath=os.path.join('pumsb.dat')
# filepath=os.path.join('pumsb_star.dat')
# filepath=os.path.join('T10I4D100K.dat')
# filepath=os.path.join('T40I10D100K.dat')
# filepath=os.path.join('retail.dat')
# ; filepath=os.path.join('T16IT20D100K.csv')


# # Get a list of all entries in the directory
# entries = os.listdir(directory_path)

# files_with_paths = [os.path.join(directory_path, entry) for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
# # Filter only files
# files = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]

dataset=Global.readDataset(filepath, sep=' ', encoding='utf-8-sig', hasHeader=False)
if not isinstance(dataset, pd.DataFrame):
    print(f"An error occurred: Could not read dataset!")    
    sys.exit()

records=dataset.values.tolist()
#remove nan elements from this list
records = [[x for x in sublist if not pd.isna(x)] for sublist in records]

D=pd.Series(records) 
F=describe(D)
print(F)

