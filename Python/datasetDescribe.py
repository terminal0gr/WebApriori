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

#print(dataset.describe(include='all'))

#datasetDescription['Shape']=f"Rows:{dataset.shape[0]}, Columns:{dataset.shape[1]}"
#datasetDescription['Describe']=dataset.describe(include='all').to_dict(orient='dict')
datasetDescription['Head']=dataset.head(10).to_dict(orient='records')
print(json.dumps(datasetDescription))




