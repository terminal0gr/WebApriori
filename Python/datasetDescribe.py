import sys
import json
import os
import pandas as pd
import numpy as np
import datasetAttrAutoDetectMetadata as Metadata
import Global

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

rows=10
if len(sys.argv)>3:
    if len(sys.argv[3])>0:
        rows=int(sys.argv[3])

columns=15       
if len(sys.argv)>4:
    if len(sys.argv[4])>0:
        columns=int(sys.argv[4])

public=0 # 0 > private, 1 > public
if len(sys.argv)>5:
    if len(sys.argv[5])>0:
        public=int(sys.argv[5])


#------------------------------           
#end command line arguments section
#------------------------------

datasetDescription = {}

try:
     
    if public==0:
        filepath=os.path.join('datasets', str(identity), datasetName)
    else:
        filepath=os.path.join('public', datasetName)

    metadataInst=Metadata.Metadata()
    metaDataFile=metadataInst.readMetadataFile(identity,datasetName,public)

    #Read the dataset from file
    dataset=Global.readDataset(filepath, sep=metaDataFile['delimiter'], encoding='utf-8-sig', hasHeader=metaDataFile['hasHeader'], nRows=rows)
    if not isinstance(dataset, pd.DataFrame):
        print(f"An error occurred: Could not read dataset! {e}")     
        sys.exit    

    datasetDescription['features']={"Rows":  ("Dataset rows", dataset.shape[0], dataset.shape[0], "The total rows of the dataset")}

    Type1="0-Unmanaged"
    Desc1="Unmanaged Dataset Type. This type can't be used for useful Association rules or frequent itemsets."
    if metaDataFile['datasetTypePredicted']==1:
        Type1="1-MBL"
        Desc1="Market Basket List (MBL) Dataset Type. Each dataset row is a transaction. A transaction involves a variable number of items. "
    elif metaDataFile['datasetTypePredicted']==2:
        Type1="2-INV"
        Desc1="Invoice detail (INV) Dataset Type. This dataset type is a special report (usually called Detailed Sales Statement) produced by a Company Accounting or an Enterprise Resource Planning software (ERP)."   
    elif metaDataFile['datasetTypePredicted']==3:
        Type1="3-SI"
        Desc1="Sparse Item (SI) Dataset Type. It involves a header and a fixed number of columns. Each item corresponds to a column. Each row represents a transaction." 
    elif metaDataFile['datasetTypePredicted']==4:
        Type1="4-NOA"
        Desc1="Nominal Attributes (NOA) Dataset Type. It involves a fixed number of columns. Each column registers nominal/categorical values."    
    datasetDescription['features'].update({"datasetTypePredicted":  ("Dataset type Predicted", metaDataFile['datasetTypePredicted'], Type1, Desc1)})

    Type1="0-Unmanaged"
    Desc1="Unmanaged Dataset Type. This type can't be used for useful Association rules or frequent itemsets."
    if metaDataFile['datasetType']==1:
        Type1="1-MBL"
        Desc1="Market Basket List (MBL) Dataset Type. Each dataset row is a transaction. A transaction involves a variable number of items. "
    elif metaDataFile['datasetType']==2:
        Type1="2-INV"
        Desc1="Invoice detail (INV) Dataset Type. This dataset type is a special report (usually called Detailed Sales Statement) produced by a Company Accounting or an Enterprise Resource Planning software (ERP)."   
    elif metaDataFile['datasetType']==3:
        Type1="3-SI"
        Desc1="Sparse Item (SI) Dataset Type. It involves a header and a fixed number of columns. Each item corresponds to a column. Each row represents a transaction." 
    elif metaDataFile['datasetType']==4:
        Type1="4-NOA"
        Desc1="Nominal Attributes (NOA) Dataset Type. It involves a fixed number of columns. Each column registers nominal/categorical values."    
    datasetDescription['features'].update({"datasetType": ("Dataset type Declared", metaDataFile['datasetType'], Type1, Desc1)})

    datasetDescription['features'].update(metaDataFile['datasetFeatures'])

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

except Exception as e:
    print(f"An error occurred: {e}")





