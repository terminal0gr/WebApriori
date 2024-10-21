import sys
import os
import json
import csvMy as csv
#import csv
import datasetTypeDetection as df
from Inv_2_Sorter import Inv_2_Sorter
import Global
import Main01W as Apriori
import pandas as pd
import skmine

nRows=500

class Metadata():

    def createMetadataFile(self, identity, datasetName, datasetType=-1, public=0, forceDelimiter=None, forceHasHeader=None, forceArg1=None, forceArg2=None):

        if public==0:
            filepath=os.path.join('datasets', str(identity), datasetName)
        else:
            filepath=os.path.join('public', datasetName)	

        if Global.is_arff_file(filepath):
           dataset=Global.loadarfftoDataframe(filepath, encoding='utf-8-sig',nRows=nRows)
           filepathcsv=os.path.join('temp',datasetName)
           filepath=os.path.splitext(filepathcsv)[0] + '.csv'
           dataset.to_csv(filepath,index=False)

        datasetAttributes = {}

        sSample=''
        with open(filepath, encoding='utf-8-sig') as f:
            for i, line in enumerate(f):
                if i < nRows:
                    sSample+=line
                else:
                    break

        if sSample=='':
            print(f"Dataset found empty!!!")     
            sys.exit    
            
        datasetAttributes['hasHeader'], datasetAttributes['header'],dialect = csv.Sniffer().has_header(sSample, forceDelimiter, forceHasHeader)
        # dialect = csv.Sniffer().sniff(sSample)  # Check what kind of csv/tsv file we have.
        datasetAttributes['delimiter']=dialect.delimiter

        DFI=df.datasetFeatures()._datasetFeatures_a(filepath,dialect,datasetAttributes['hasHeader'],nRows=nRows)
        if DFI==None:
            print(f"Failed to detect dataset attributes for dataset '{datasetName}'.")
            sys.exit()

        DFI_Dict = {
            "NumberOfColumns": ("Number Of Columns", int(DFI.NumberOfColumns), int(DFI.NumberOfColumns), "The total number of columns/features in the Dataset"),
            "_name": ("Name", DFI._name, DFI._name, "The name of the dataset"),
            "AvgOfDistinctValuesPerCol": ("AvgOfDistinctValuesPerCol" ,DFI.AvgOfDistinctValuesPerCol, "{:.1f}%".format(DFI.AvgOfDistinctValuesPerCol*100), "The Average of distinct values per column over the total columns"),
            "AvgOfDistinctValuesOverAll": ("AvgOfDistinctValuesOverAll", DFI.AvgOfDistinctValuesOverAll, "{:.1f}%".format(DFI.AvgOfDistinctValuesOverAll*100), "The ratio of the number of total unique values to the number of elements"),
            "AvgOfDistinctValuesPerRow": ("AvgOfDistinctValuesPerRow", DFI.AvgOfDistinctValuesPerRow, "{:.1f}%".format(DFI.AvgOfDistinctValuesPerRow*100), "The Average of distinct values per row over the total rows"),
            "Top1Value": ("Most Frequent Value", str(DFI.Top1Value), str(DFI.Top1Value), "The most frequent value in the dataset"),
            "FreqOfTop1FreqValue": ("Top 1 Value %", DFI.FreqOfTop1FreqValue, "{:.1f}%".format(DFI.FreqOfTop1FreqValue*100), "The ratio Of the number of the most frequent value to the number of elements"), 
            "FreqOfTop2FreqValue": ("Top 2 Value %", DFI.FreqOfTop2FreqValue, "{:.1f}%".format(DFI.FreqOfTop2FreqValue*100), "The ratio of the number of the second most frequent value to the number of elements"), 
            "FreqOfTop3FreqValue": ("Top 3 Value %", DFI.FreqOfTop3FreqValue, "{:.1f}%".format(DFI.FreqOfTop3FreqValue*100), "The ratio of the number of the third most frequent value to the number of elements"), 
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
            "hasHeader": ("Has Header?", DFI.hasHeader, DFI.hasHeader, "Does the dataset have Header?"),
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

        if datasetAttributes['datasetType']==2:

            if forceArg1 is not None:
                datasetAttributes['groupItem']=forceArg1
            else:
                #####################            
                #GROUP ITEM DETECTION
                #####################

                #Initialization to None
                datasetAttributes['groupItem']='?'

                filepath=os.path.join('datasets')	
            
                #Firstly I check if the folder exists. If not, then create it and auto detect dataset attributes.
                if not os.path.exists(filepath):
                    print(f"Failed to detect datasets folder!!!")     
                    sys.exit    

                filepath=os.path.join('datasets', 'Inc_2_Group_Words.json')	
                #Secondly I check if the the lexicon file exists. If not
                if os.path.exists(filepath): 

                    value_dict={}

                    # Open the JSON file in read mode
                    with open(filepath, encoding='utf-8-sig') as file:
                        # Load the JSON data from the file
                        try:
                            value_dict = json.load(file)
                        except Exception as e:
                            # Handle the case where no JSON data is found or the file is empty
                            print(f"An error occurred: {e}")
                            sys.exit()

                    if value_dict:
                        # Create an instance of DictionarySorter
                        sorter = Inv_2_Sorter(datasetAttributes['header'], value_dict)
                        datasetAttributes['groupItem']=sorter.generate_best_item()

            if forceArg2 is not None:
                datasetAttributes['valueItem']=forceArg2
            else:
                #####################            
                #VALUE ITEM DETECTION
                #####################

                #Initialization to None
                datasetAttributes['valueItem']='?'

                filepath=os.path.join('datasets')	
            
                #Firstly I check if the folder exists. If not, then create it and auto detect dataset attributes.
                if not os.path.exists(filepath):
                    print(f"Failed to detect datasets folder!!!")     
                    sys.exit    

                filepath=os.path.join('datasets', 'Inc_2_Value_Words.json')	
                #Secondly I check if the the lexicon file exists. If not
                if os.path.exists(filepath): 

                    value_dict={}

                    # Open the JSON file in read mode
                    with open(filepath, encoding='utf-8-sig') as file:
                        # Load the JSON data from the file
                        try:
                            value_dict = json.load(file)
                        except Exception as e:
                            # Handle the case where no JSON data is found or the file is empty
                            print(f"An error occurred: {e}")
                            sys.exit()

                    if value_dict:
                        # Create an instance of DictionarySorter
                        sorter = Inv_2_Sorter(datasetAttributes['header'], value_dict)
                        datasetAttributes['valueItem']=sorter.generate_best_item()

        if datasetAttributes['datasetType']==3:
            if forceArg1 is not None:
               datasetAttributes['absentValue']=str(forceArg1)
            else:
               datasetAttributes['absentValue']=str(DFI.Top1Value)

        ###########################################################################
        # Append to file, four important features of the transformed final dataset n_items, avg_transaction_size, n_transactions, density=avg_transaction_size / n_items
        # 4th parameter=101 means --> transformed transaction description. n_items, avg_transaction_size, n_transactions, density=avg_transaction_size / n_items
        # wrapped in a dictionary
        WAInst=Apriori.webApriori(identity,datasetName,public,101,arg1=None,arg2=None)
        # The Attributes below are needed in WAInst.prepare_records
        WAInst.datasetSep=datasetAttributes['delimiter']
        WAInst.hasHeader=datasetAttributes['hasHeader']
        WAInst.datasetType=datasetAttributes['datasetType']
        WAInst.header=datasetAttributes['header']
        if WAInst.datasetType==2:
            if 'groupItem' in datasetAttributes:
                WAInst.groupItem=datasetAttributes['groupItem']
            if 'valueItem' in datasetAttributes:
                WAInst.valueItem=datasetAttributes['valueItem']
        if  WAInst.datasetType==3:
            if 'absentValue' in datasetAttributes:
                WAInst.absentValue=datasetAttributes['absentValue']
        records=WAInst.prepare_records()
        D=pd.Series(records)
        DFI2=skmine.datasets.utils.describe(D)

        # # Convert Series to DataFrame
        # df = D.to_frame()
        # # Write to file with ';' delimiter and UTF-8 encoding
        # df.to_csv("output_file.csv", sep=';', encoding='utf-8', index=False, header=False)
        
        # DFI2=WAInst.runWebApriori()
        key='n_items'
        if key in DFI2:
            datasetAttributes['datasetFeatures'][key]=("Items count",DFI2[key],DFI2[key],"The total number of items for ARM process")
        key='avg_transaction_size'
        if key in DFI2:
            datasetAttributes['datasetFeatures'][key]=("Avg items per transaction",DFI2[key],"{:.2f}".format(DFI2[key]),"The average number of items per transaction for ARM process")
        key='n_transactions'
        if key in DFI2:
            datasetAttributes['datasetFeatures'][key]=("transactions count",DFI2[key],DFI2[key],"The total number of transactions for ARM process")
        key='density'
        if key in DFI2:
            datasetAttributes['datasetFeatures'][key]=("transactions density",DFI2[key],"{:.1f}%".format(DFI2[key]*100.),"The density of transactions for ARM process")
        ###########################################################################

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
            return "ERROR!!! Failed to retrieve dataset attributes!!!"

        # Open the JSON file in read mode
        with open(filepath, 'r') as file:
            # Load the JSON data from the file
            json_data = json.load(file)

        mustReinitialize=False
        if not 'datasetFeatures'  in json_data or not 'datasetType' in json_data:
            mustReinitialize=True

        # If the dataset type is Inv-2 and groupItem or valueItem cannot be detected recreate metadataFile
        if json_data['datasetType']==2 and (not 'groupItem'  in json_data or not 'valueItem' in json_data):
            mustReinitialize=True

        if mustReinitialize:
            json_data=self.createMetadataFile(identity,datasetName,-1,public) 
        else:
            try:
                # Changes found in dataset. DatasetFeatures must be updated.
                if json_data['delimiter']!=json_data['datasetFeatures']['delimiter'][1] or json_data['hasHeader']!=json_data['datasetFeatures']['hasHeader'][1] or 'datasetTypeChanged' in json_data:
                    # Key created in PHP call and must be erased by code below because it was needed to lead to this if block.
                    json_data.pop('datasetTypeChanged', None)
                    # Calling createMetadataFile but without autodetecting delimiter and hasHeader
                    if json_data['datasetType']==2:
                        # needs groupItem, valueItem
                        json_data=self.createMetadataFile(identity,datasetName,json_data['datasetType'],public, json_data['delimiter'], json_data['hasHeader'],json_data['groupItem'],json_data['valueItem']) 
                    elif json_data['datasetType']==3:
                        # needs absentValue
                        json_data=self.createMetadataFile(identity,datasetName,json_data['datasetType'],public, json_data['delimiter'], json_data['hasHeader'],json_data['absentValue'])
                    else:                                                          
                        json_data=self.createMetadataFile(identity,datasetName,json_data['datasetType'],public, json_data['delimiter'], json_data['hasHeader']) 
            except Exception as e:
                json_data=self.createMetadataFile(identity,datasetName,-1,public) 

        # Now you can work with the JSON data as a Python dictionary or list
        return json_data


