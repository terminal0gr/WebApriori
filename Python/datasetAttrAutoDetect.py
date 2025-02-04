import sys
import json
import datasetAttrAutoDetectMetadata as Metadata

identity='79d1727987f200802593e3599119c966'

# datasetName='H-MineSample.txt'	
# datasetName='invoice.csv'	
# datasetName='titanic02.csv'	
# datasetName='4Thyroid_Diff.csv'
# datasetName='grocery_timestamp.csv'
# datasetName='0data_balita.csv'
# datasetName='T10I4D100K.dat'
# datasetName='kosarak.dat'
# datasetName="chess.dat"
# datasetName="1_L-0023.csv"
datasetName="webdocs.dat"

datasetType=1 # -1 means detect DatasetType. Else force the value from user
public=0 # 0 > private, 1 > public
force=0 # Force recreate dataset attributes

#------------------------------
#command line arguments section
#------------------------------

#identity
 #random for testing purposes 
if len(sys.argv)>1:
	try:
		identity=str(sys.argv[1])
	except:
		sys.exit()
              
if len(sys.argv)>2:
    if len(sys.argv[2])>0:
        datasetName=sys.argv[2]

# -1 means detect DatasetType. Else force the value from user
if len(sys.argv)>3:
	try:
		datasetType=int(sys.argv[3])
	except:
		datasetType=-1 
            
# 0 > private, 1 > public
if len(sys.argv)>4:
    if len(sys.argv[4])>0:
        public=int(sys.argv[4])

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

