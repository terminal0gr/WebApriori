import sys
import json
import datasetAttrAutoDetectMetadata as Metadata

#------------------------------
#command line arguments section
#------------------------------

#identity
identity='79d1727987f200802593e3599119c966' #random for testing purposes 
if len(sys.argv)>1:
	try:
		identity=str(sys.argv[1])
	except:
		sys.exit()
              
# datasetName='H-MineSample.txt'	
# datasetName='invoice.csv'	
# datasetName='titanic02.csv'	
# datasetName='4Thyroid_Diff.csv'
# datasetName='grocery_timestamp.csv'
# datasetName='0data_balita.csv'
# datasetName='T10I4D100K.csv'
datasetName='kosarak.dat'

if len(sys.argv)>2:
    if len(sys.argv[2])>0:
        datasetName=sys.argv[2]

datasetType=-1 # -1 means detect DatasetType. Else force the value from user
if len(sys.argv)>3:
	try:
		datasetType=int(sys.argv[3])
	except:
		datasetType=-1 

public=0 # 0 > private, 1 > public
if len(sys.argv)>4:
    if len(sys.argv[4])>0:
        public=int(sys.argv[4])

force=1
if len(sys.argv)>5:
    if len(sys.argv[5])>0:
        force=int(sys.argv[5])




metadataInst=Metadata.Metadata()

if force==0:
    metadatafile=metadataInst.readMetadataFile(identity,datasetName,public)
    print(json.dumps(metadatafile))
else:     
    metadatafile=metadataInst.createMetadataFile(identity,datasetName,datasetType,public)
    print(json.dumps(metadatafile))

#------------------------------           
#end command line arguments section
#------------------------------

