import sys
import json
import os
import pandas as pd
import numpy as np
import datasetAttrAutoDetectMetadata as Metadata

#------------------------------
#command line arguments section
#------------------------------

#identity
identity='111111111' #random for testing purposes 
if len(sys.argv)>1:
	try:
		identity=str(sys.argv[1])
	except:
		sys.exit()
              
datasetName='something.csv'	
if len(sys.argv)>2:
    if len(sys.argv[2])>0:
        datasetName=sys.argv[2]

public=0 # 0 > private, 1 > public
if len(sys.argv)>3:
    if len(sys.argv[3])>0:
        public=int(sys.argv[3])

rows=10
if len(sys.argv)>4:
    if len(sys.argv[4])>0:
        rows=int(sys.argv[4])

columns=15       
if len(sys.argv)>5:
    if len(sys.argv[5])>0:
        columns=int(sys.argv[5])


#------------------------------           
#end command line arguments section
#------------------------------

metadataInst=Metadata.Metadata()
metaDataFile=metadataInst.readMetadataFile(identity,datasetName,public)

datasetDescription = {}

if public==0:
    filepath=os.path.join('datasets', str(identity), datasetName)
else:
    filepath=os.path.join('public', datasetName)

dataset = pd.read_csv(filepath, sep=metaDataFile['delimiter'])

datasetDescription['features']={"Rows":  ("Dataset rows", dataset.shape[0], dataset.shape[0], "The total rows of the dataset")}
metaDatafile=metadataInst.readMetadataFile(identity,datasetName,public)

datasetDescription['features'].update(metaDatafile['datasetFeatures'])

#Arbitrary take the first 15 columns for rendering purposes
if dataset.shape[1]>columns:
     dataset=dataset[dataset.columns[:columns]]

headData=dataset.head(rows).to_dict(orient='records')

# Αντικατάσταση των τιμών NaN με κενό
for item in headData:
    for key, value in item.items():
        if isinstance(value, float) and np.isnan(value):
            item[key] = 'NaN'
#my_dict_cleaned = {k: '' if isinstance(v, float) and np.isnan(v) else v for k, v in my_dict.items()}
datasetDescription['Head']=headData

print(json.dumps(datasetDescription))





