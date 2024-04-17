import sys
import os
import json
import csvMy as csv
import datasetTypeDetection as df

class Metadata():

    def createMetadataFile(self, identity, datasetName, datasetType=-1, public=0):

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
                    if DFI==None:
                        print(f"Failed to detect dataset attributes for dataset '{datasetName}'.")
                        sys.exit()
                    if DFI.datasetType==-1:
                        datasetAttributes['datasetType']=int(df.datasetFeatures().AutoDetectType(DFI))
                    else:
                        datasetAttributes['datasetType']=int(DFI.datasetType)
            else: 
                datasetAttributes['datasetType']=int(datasetType)

        if public==0:
            filepath=os.path.join('output', str(identity))
        else:
            filepath=os.path.join('output', str(identity), 'p')	

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
            return datasetAttributes

    def readMetadataFile(self, identity, datasetName, public=0):
        
        if public==0:
            filepath=os.path.join('output', str(identity))
        else:
            filepath=os.path.join('output', str(identity), 'p')	
        
        #Firstly I check if the folder exists. If not, then create it and auto detect dataset attributes.
        if not os.path.exists(filepath):
            self.createMetadataFile(identity,datasetName,-1,public)

        filepath=os.path.join(filepath, datasetName)
        filepath=os.path.splitext(filepath)[0] + '.metadata'
        #Secondly I check if the dataset's metadata file exists. If not, then try create it and auto detect dataset attributes.
        if not os.path.exists(filepath): 
            self.createMetadataFile(identity,datasetName,-1,public) 

        #finally, if not then 
        if not os.path.exists(filepath): 
            print("Failed to retrieve dataset attributes!!!")
            sys.exit() 

        # Open the JSON file in read mode
        with open(filepath, 'r') as file:
            # Load the JSON data from the file
            json_data = json.load(file)

        # Now you can work with the JSON data as a Python dictionary or list
        return json_data
