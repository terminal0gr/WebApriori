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

            DFI=df.datasetFeatures()._datasetFeatures_a(filepath,dialect.delimiter,datasetAttributes['hasHeader'])
            if DFI==None:
                print(f"Failed to detect dataset attributes for dataset '{datasetName}'.")
                sys.exit()

            DFI_Dict = {
                "NumberOfColumns": ("Number Of Columns", int(DFI.NumberOfColumns), int(DFI.NumberOfColumns), "The total number of columns/features in the Dataset"),
                "_name": ("Name", DFI._name, DFI._name, "The name of the dataset"),
                "AvgOfDistinctValuesPerCol": ("AvgOfDistinctValuesPerCol" ,DFI.AvgOfDistinctValuesPerCol, "{:.1f}%".format(DFI.AvgOfDistinctValuesPerCol*100), "The Average of distinct values per column over the total columns"),
                "AvgOfDistinctValuesOverAll": ("AvgOfDistinctValuesOverAll", DFI.AvgOfDistinctValuesOverAll, "{:.1f}%".format(DFI.AvgOfDistinctValuesOverAll*100), "The ratio of the number of total unique values to the number of elements"),
                "AvgOfDistinctValuesPerRow": ("AvgOfDistinctValuesPerRow", DFI.AvgOfDistinctValuesPerRow, "{:.1f}%".format(DFI.AvgOfDistinctValuesPerRow*100), "The Average of distinct values per row over the total rows"),
                "FreqoFTop1FreqValue": ("Top 1 Value", DFI.FreqoFTop1FreqValue, "{:.1f}%".format(DFI.FreqoFTop1FreqValue*100), "The ratio of the number of the most frequent value to the number of elements"), 
                "FreqoFTop2FreqValue": ("Top 2 Value", DFI.FreqoFTop2FreqValue, "{:.1f}%".format(DFI.FreqoFTop2FreqValue*100), "The ratio of the number of the second most frequent value to the number of elements"), 
                "FreqoFTop3FreqValue": ("Top 3 Value", DFI.FreqoFTop3FreqValue, "{:.1f}%".format(DFI.FreqoFTop3FreqValue*100), "The ratio of the number of the third most frequent value to the number of elements"), 
                "FreqOfIntegerCol": ("Integer Columns %", DFI.FreqOfIntegerCol, "{:.1f}%".format(DFI.FreqOfIntegerCol*100), "The ratio of integer columns to the total number of columns"),
                "FreqOfNumberCol": ("Number Columns %", DFI.FreqOfNumberCol, "{:.1f}%".format(DFI.FreqOfNumberCol*100), "The ratio of float number columns to the total number of columns"),
                "FreqOfDateCol": ("Date Columns %", DFI.FreqOfDateCol, "{:.1f}%".format(DFI.FreqOfDateCol*100), "The ratio of date columns to the total number of columns"),
                "FreqOfStringCol": ("String Columns %", DFI.FreqOfStringCol, "{:.1f}%".format(DFI.FreqOfStringCol*100), "The ratio of columns with text to the total number of columns"),
                "FreqOfBoolCol": ("Boolean Columns %", DFI.FreqOfBoolCol, "{:.1f}%".format(DFI.FreqOfBoolCol*100), "The ratio of boolean columns to the total number of columns"),
                "MinItemLen": ("Min Item length", int(DFI.MinItemLen), int(DFI.MinItemLen), "The length of the smallest element in dataset"),
                "MaxItemLen": ("Max Item Length", int(DFI.MaxItemLen), int(DFI.MaxItemLen), "The length of the largest element in dataset"),
                "AvgItemLen": ("Avg Item Length", DFI.AvgItemLen, "{:.1f}".format(DFI.AvgItemLen), "The average length of the elements in dataset"),
                "Freq1CharColumns": ("1-Char Columns %", DFI.Freq1CharColumns, "{:.1f}%".format(DFI.Freq1CharColumns*100), "The columns count with exclusively 1-character elements by the total of columns"),
                "Freq2ValuesItemColumns": ("2-Value Item Columns %", DFI.Freq2ValuesItemColumns, "{:.1f}%".format(DFI.Freq2ValuesItemColumns*100), "The columns count having exclusively 2 values by the total number of columns"),
                "HasHeader": ("Has Header?", DFI.HasHeader, DFI.HasHeader, "Does the dataset have Header?"),
                "delimiter": ("delimiter", DFI.delimiter, DFI.delimiter, "The delimiter between the columns of the dataset"),
                "type2Words": ("Type 2-INV Words", int(DFI.type2Words), int(DFI.type2Words), "The number of columns containing words used in Type 2-INV datasets. For example (Invoice, Item, Customer etc)")
            }

            datasetAttributes['datasetFeatures']=DFI_Dict

            # Declare the predicted Dataset type
            if dialect.datasetType==0:
              datasetAttributes['datasetTypePredicted']=int(df.datasetFeatures().AutoDetectType(DFI))
            else:
               datasetAttributes['datasetTypePredicted']=int(dialect.datasetType)  

            if datasetType==-1:
                if dialect.datasetType==1: #Without Machine learning detection
                    datasetAttributes['datasetType']=int(dialect.datasetType)
                else:
                    if DFI.datasetType==-1:
                        datasetAttributes['datasetType']=datasetAttributes['datasetTypePredicted']
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

        if not 'datasetFeatures' in json_data:
            self.createMetadataFile(identity,datasetName,-1,public) 
            with open(filepath, 'r') as file:
                json_data = json.load(file)

        # Now you can work with the JSON data as a Python dictionary or list
        return json_data
