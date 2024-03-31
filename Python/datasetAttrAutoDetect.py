import sys
import os
import json
import csvMy as csv
import datasetTypeDetection as df

#------------------------------
#command line arguments section
#------------------------------

#identity
identity=111111111 #random for testing purposes
if len(sys.argv)>1:
	try:
		identity=str(sys.argv[1])
	except:
		sys.exit()
              
datasetName='titanic02.csv'	
if len(sys.argv)>2:
    if len(sys.argv[2])>0:
        datasetName=sys.argv[2]

datasetType=-1
if len(sys.argv)>3:
	try:
		datasetType=int(sys.argv[3])
	except:
		datasetType=-1 # -1 means detect DatasetType. Else force the value from user

public=0
if len(sys.argv)>4:
    if len(sys.argv[4])>0:
        public=sys.argv[4]

#------------------------------           
#end command line arguments section
#------------------------------


if public==0:
    filepath=os.path.join('datasets', str(identity), datasetName)
else:
    filepath=os.path.join('public', datasetName)	

datasetAttributes = {}

with open(filepath, encoding='utf8') as f:
    s100=''

    for x in range(100):
        s100+=f.readline()

    datasetAttributes['hasHeader'], datasetAttributes['header'] = csv.Sniffer().has_header(s100)
    dialect = csv.Sniffer().sniff(s100)  # Check what kind of csv/tsv file we have.
    datasetAttributes['delimiter']=dialect.delimiter

    if datasetType==-1:
        if dialect.datasetType==1: #Without Machine learning detection
            datasetAttributes['datasetType']=int(dialect.datasetType)
        else:
            DFI=df.datasetFeatures()._datasetFeatures_a(filepath,dialect.delimiter,datasetAttributes['hasHeader'])
            datasetAttributes['datasetType']=int(df.datasetFeatures().AutoDetectType(DFI))

if public==0:
    filepath=os.path.join('output', str(identity))
else:
    filepath=os.path.join('output', 'p')	

# Use os.makedirs() to create the folder (including parent directories if they don't exist)
os.makedirs(filepath, exist_ok=True)

if os.path.exists(filepath):
    filepath=os.path.join(filepath, datasetName)
else:
    print(f"Failed to create folder '{filepath}'.")
    sys.exit()

#file = open(os.path.splitext(filepath)[0] + '.metadata','w')
with open(os.path.splitext(filepath)[0] + '.metadata','w') as file:
    json.dump(datasetAttributes, file, indent=4)
    #print(json.dumps(datasetAttributes, indent=4)) 
    json_string = json.dumps(datasetAttributes)
    print(json_string)

#------------
#test section

#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '4', 'titanic02.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '4', 'titanic02WithoutHeader.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '3', 'a2100.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '3', 'a2.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '3', 'grocery_timestamp.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '3', 'supermarket.txt')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '2', 'invoice.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '2', 'OrderDetails.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '1', 'groceries.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '1', 'dataset.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '1', 'Fake05_1.csv')

# print('improved version')
# with open(filepath, encoding='utf8') as f:
#     s10=''
#     for x in range(100):
#         s10+=f.readline()
#     f.seek(0) # Go to start
#     has_header = csv.Sniffer().has_header(s10)
#     print(has_header)
#     dialect = csv.Sniffer().sniff(s10)  # Check what kind of csv/tsv file we have.
#     print(repr(dialect.delimiter))

# print('original version')
# with open(filepath, encoding='utf8') as csvfile:
#     csv_test_bytes = csvfile.read(8192)  # Grab a sample of the CSV for format detection.
#     csvfile.seek(0)  # Rewind
#     has_header = csv.Sniffer().has_header(csv_test_bytes)  # Check to see if there's a header in the file.
#     print(has_header)
#     dialect = csv.Sniffer().sniff(csv_test_bytes)  # Check what kind of csv/tsv file we have.
#     print(repr(dialect.delimiter))
    #inputreader = csv.reader(csvfile, dialect)
    #if has_header:
    #    next(inputreader) # Skip the header if we have one.
    #for row in inputreader:
    #    print(row)
#End test section
#----------------