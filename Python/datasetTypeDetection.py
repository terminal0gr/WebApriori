"""
datasetTypeDetection.py - create the features of a given dataset or dataset sample
and auto detects its type in case is 0,2,3,4 type. 
Owner: Malliaridis Konstantinos PHd candidate
"""

import os
from scipy.io import arff
import pandas as pd
from joblib import load

class datasetFeatures:
    """Creates the features of a given dataset or dataset sample that can be used 
    in Machine learning experiments

    """
    _name=""
    AvgOfDistinctValuesPerCol = 0.0 #Range [0...1]
    AvgOfDistinctValuesOverAll = 0.0 #Range [0...1]
    AvgOfDistinctValuesPerRow = 0.0 #Range [0...1]
    FreqoFTop1FreqValue = 0.0 #Range [0...1]
    FreqoFTop2FreqValue = 0.0 #Range [0...1]
    FreqoFTop3FreqValue = 0.0 #Range [0...1]
    NumberOfColumns = 0 #Range [1...Infinite]
    FreqOfIntegerCol = 0.0 #Range [0...1]
    FreqOfNumberCol = 0.0 #Range [0...1]
    FreqOfDateCol = 0.0 #Range [0...1]    
    FreqOfStringCol = 0.0 #Range [0...1]
    FreqOfBoolCol = 0.0 #Range [0...1]
    MinItemLen = 9999 #Range [0...infinite]
    MaxItemLen = 0 #Range [0...infinite]
    AvgItemLen = 0.0 #Range [0...infinite]
    Freq1CharColumns = 0.0 #Range [0...1]
    Freq2ValuesItemColumns = 0.0 #Range [0...1]
    HasHeader=True  
    datasetType='0'
    delimiter=';'
    Header=[]
    type2Words=0 #Range [0...infinite]

    def _datasetFeatures_a(self, filepath, delimiter, hasHeader, nrows=500):
        # Creates the features of the dataset in order to determine datasetType via ML
        try:

            #The possible missing values that can exists in datasets and pandas cannot manipulate by default
            extra_missing_values_light = ["n/a", "na"] #Useful only in 3 type recordset which may use "-", "?", "#" as absent value of an item
            extra_missing_values_normal = ["n/a", "na", "-", "?", "#"] #all the other dataset types (0,2,4)

            headerV1=None
            if hasHeader:
                headerV1=0

            try: #Try with extra_missing_values_normal
                df, meta = loadarfftoDataframe(filepath,False)
                if df is None:       
                    df = pd.read_csv(filepath, sep=delimiter, nrows=nrows, encoding='utf-8', na_values = extra_missing_values_normal, header=headerV1)
            except Exception as e:
                df = pd.read_csv(filepath, sep=delimiter, nrows=nrows, encoding='utf-8', na_values = extra_missing_values_normal, header=headerV1)

            hasMissingValues=False
            for myCol in df.columns:
                #Remove the rows from current column that have missing values
                dfcol = df[myCol].dropna()
                if dfcol.shape[0]==0: #rows "The column {dfcol.name} of {os.path.basename(filepath)} is full of missing values 
                    hasMissingValues=True
                elif dfcol.shape[0]>0 and dfcol.shape[0]<(df[myCol].shape[0]*0.2): #The column {dfcol.name} of the dataset {os.path.basename(filepath)} is full (estimated more than 80%) of missing values and can't be analysed. The procedure ends with error.
                    hasMissingValues=True 
            
            if hasMissingValues: #Try with extra_missing_values_light
                try:
                    df, meta = loadarfftoDataframe(filepath)
                    if df is None:       
                        df = pd.read_csv(filepath, sep=delimiter, nrows=nrows, encoding='utf-8', na_values = extra_missing_values_light, header=headerV1)
                except Exception as e:
                    df = pd.read_csv(filepath, sep=delimiter, nrows=nrows, encoding='utf-8', na_values = extra_missing_values_light, header=headerV1)

                for myCol in df.columns:
                    #Remove the rows from current column that have missing values
                    dfcol = df[myCol].dropna()
                    if dfcol.shape[0]==0: #rows
                        print(f"The column {dfcol.name} of {os.path.basename(filepath)} is full of missing values and can't be analysed. The procedure ends with error.")
                        return None 
                    if dfcol.shape[0]>0 and dfcol.shape[0]<(df[myCol].shape[0]*0.2):
                        print(f"The column {dfcol.name} of the dataset {os.path.basename(filepath)} is full (estimated more than 80%) of missing values and can't be analysed. The procedure ends with error.")
                        return None 

            class datasetFeaturesInst(datasetFeatures):
                _name=os.path.basename(filepath)

            datasetFeaturesInst.delimiter=delimiter

            if hasHeader:
                datasetFeaturesInst.Header=df.columns.tolist()

                #datasetFeaturesInst.type2Words += sum(1 for item in datasetFeaturesInst.Header if 'invoice' in str.upper(item))
                # Specific list of strings to count
                specific_strings = ['INVOICE', 'ORDER', 'QUA', 'QUANTITY', 'QTY', 'PRODUCT', 'ITEM', 'CUSTOMER', 'ΕΙΔ', 'ΤΙΜΟΛ', 'ΠΑΡΑΣ', 'ΠΑΡΑΓ', 'ΠΟΣΟΤ', 'ΠΕΛΑΤ', 'PRODUKT']
                datasetFeaturesInst.type2Words= sum(1 for item in datasetFeaturesInst.Header if any(s in str.upper(item) for s in specific_strings))


            freqplus=0
            boolColumns=0
            numericColumns=0
            integerColumns=0
            datetimeColumns=0
            twoValuesItemColumn=0
            for myCol in df.columns:

                #Remove the rows from current column that have missing values
                dfcol = df[myCol].dropna()
                if dfcol.shape[0]==0: #rows
                    print(f"The column {dfcol.name} of {os.path.basename(filepath)} is full of missing values and can't be analysed. The procedure ends with error.")
                    return None 
                if dfcol.shape[0]>0 and dfcol.shape[0]<(df[myCol].shape[0]*0.2):
                    print(f"The column {dfcol.name} of the dataset {os.path.basename(filepath)} is full (estimated more than 80%) of missing values and can't be analysed. The procedure ends with error.")
                    return None 

                uniqueValues=dfcol.nunique()
                freq=uniqueValues/df.shape[0] #df.shape[0]->#rows
                freqplus+=freq
                if uniqueValues<=2:
                    twoValuesItemColumn+=1

                #detect bool column values (missing values have been eliminated in this stage...)
                if (dfcol.isin([0, 1]).all() or 
                    dfcol.isin(['t', 'f']).all() or
                    dfcol.isin(['T', 'F']).all() or
                    dfcol.isin(['y', 'n']).all() or
                    dfcol.isin(['Y', 'N']).all() or
                    dfcol.isin(['YES', 'NO']).all() or
                    dfcol.isin(['yes', 'no']).all() or
                    dfcol.isin(['Yes', 'No']).all() or                    
                    dfcol.isin(['true', 'false']).all() or
                    dfcol.isin(['TRUE', 'FALSE']).all() or
                    dfcol.isin(['True', 'False']).all() or                    
                    dfcol.isin([True, False]).all()
                   ):
                        boolColumns+=1
                        continue
                
                try:
                    # At first check if you can recognise the column as number
                    tempColumn = pd.to_numeric(dfcol, errors='raise')
                    dfint=dfcol.astype('int64') 
                    if dfint.sum()==dfcol.sum():
                        integerColumns+=1
                        continue
                    else:  
                        numericColumns+=1
                        continue

                except ValueError:
                    try:
                        # If not then try to check if it is a number but with comma as delimiter e.g. like greek regional settings
                        dfc=dfcol.str.replace('.', '') # 43.700,00 --> 43700,00
                        dfc=dfc.str.replace(',', '.')      # 43700,00  --> 43700.00
                        dfc=pd.to_numeric(dfc, errors='raise') #check if can be pasred as number
                        dfint=dfc.astype('int64') 
                        if dfint.sum()==dfc.sum():
                            integerColumns+=1
                            continue
                        else:  
                            numericColumns+=1
                            continue
                          
                    except ValueError:
                        try:
                            # If not a number the try to check if it is a date.
                            # to_datetime ensures that it will find that a column is datetime even if it has 
                            # other format than the expected (expected format yyy-mm-dd)
                            tempColumn = pd.to_datetime(dfcol, errors='raise', format='mixed')
                            datetimeColumns+=1
                            continue
                        except ValueError:
                            # Ok it is not a datetime Column. So what!!!
                            datetimeColumns+=0
                            continue

            datasetFeaturesInst.AvgOfDistinctValuesPerCol=freqplus/df.shape[1] #df.shape[1]->#Columns

            datasetFeaturesInst.FreqOfIntegerCol=integerColumns/df.shape[1]
            
            datasetFeaturesInst.FreqOfNumberCol=numericColumns/df.shape[1]

            datasetFeaturesInst.FreqOfDateCol=datetimeColumns/df.shape[1]

            datasetFeaturesInst.Freq2ValuesItemColumns=twoValuesItemColumn/df.shape[1]

            #transform the 2-dimensional dataframe to 1-dimensional dataframe e.g. (100,7)->(700) rows
            df_1d = df.stack()
            df_1d = df_1d.reset_index(drop=True)
            #nunique counts the unique values of a dataframe column
            datasetFeaturesInst.AvgOfDistinctValuesOverAll=df_1d.nunique()/(df.shape[0]*df.shape[1])
            #value_
            most_frequent_item=df_1d.value_counts().iloc[:3]
            i=0
            for si in most_frequent_item.iloc[:3]:
                i+=1
                if i==1:
                    datasetFeaturesInst.FreqoFTop1FreqValue=si/(df.shape[0]*df.shape[1])
                elif i==2:
                    datasetFeaturesInst.FreqoFTop2FreqValue=si/(df.shape[0]*df.shape[1])
                elif i==3:
                    datasetFeaturesInst.FreqoFTop3FreqValue=si/(df.shape[0]*df.shape[1])
        
            freq=0
            for i in range(df.shape[0]):
                freq+=df.iloc[i].nunique()/df.shape[1] #df.shape[0]->#rows
            datasetFeaturesInst.AvgOfDistinctValuesPerRow=freq/df.shape[0] #df.shape[1]->#Columns

            datasetFeaturesInst.NumberOfColumns=df.shape[1]

            datasetFeaturesInst.FreqOfBoolCol = boolColumns/df.shape[1]

            #All the other columns are of String/Object type 
            datasetFeaturesInst.FreqOfStringCol = round(1-datasetFeaturesInst.FreqOfIntegerCol-datasetFeaturesInst.FreqOfNumberCol-datasetFeaturesInst.FreqOfBoolCol-datasetFeaturesInst.FreqOfDateCol,6)

            datasetFeaturesInst.MinItemLen = (df.map(lambda x: len(str(x)) if x is not None else 0).min()).min()
            datasetFeaturesInst.MaxItemLen = (df.map(lambda x: len(str(x)) if x is not None else 0).max()).max()
            datasetFeaturesInst.AvgItemLen = (df.map(lambda x: len(str(x)) if x is not None else 0).mean()).mean()

            # Count columns with only 1-character items
            datasetFeaturesInst.Freq1CharColumns = (df.map(lambda x: len(str(x)) == 1 if x is not None else False).all()).sum()/df.shape[1]

            datasetFeaturesInst.HasHeader=hasHeader

            return(datasetFeaturesInst)

        except Exception as e:
            vbcrlf = '\n'
            print(f"Error!!!.{vbcrlf}Unexpected error: {e}{vbcrlf}")
            return None
        
    def AutoDetectType(self, dFI):

        #_name, datasetType omitted intetionally. _name irrelevant, datasetType > Y (predicted datasetType)
        data = {
                'AvgOfDistinctValuesPerCol': [dFI.AvgOfDistinctValuesPerCol],
                'AvgOfDistinctValuesOverAll': [dFI.AvgOfDistinctValuesOverAll],
                'AvgOfDistinctValuesPerRow': [dFI.AvgOfDistinctValuesPerRow],
                'FreqoFTop1FreqValue': [dFI.FreqoFTop1FreqValue],
                'FreqoFTop2FreqValue': [dFI.FreqoFTop2FreqValue],  
                'FreqoFTop3FreqValue': [dFI.FreqoFTop3FreqValue],
                'NumberOfColumns': [dFI.NumberOfColumns],
                'FreqOfIntegerCol': [dFI.FreqOfIntegerCol],
                'FreqOfNumberCol': [dFI.FreqOfNumberCol],
                'FreqOfDateCol': [dFI.FreqOfDateCol],
                'FreqOfStringCol': [dFI.FreqOfStringCol],
                'FreqOfBoolCol': [dFI.FreqOfBoolCol],
                'MinItemLen': [dFI.MinItemLen.item()],  
                'MaxItemLen': [dFI.MaxItemLen.item()],
                'AvgItemLen': [dFI.AvgItemLen],
                'Freq1CharColumns': [dFI.Freq1CharColumns],
                'Freq2ValuesItemColumns': [dFI.Freq2ValuesItemColumns],
                'hasHeader': [dFI.HasHeader],       
                'type2Words': [dFI.type2Words]
        }                                                              
        X_trained = pd.DataFrame(data)

        #Load the trained model
        filepath=os.path.join('features','TrainedModel.joblib')
        rf_model = load(filepath)

        y_pred = rf_model.predict(X_trained)

        return(y_pred[0])

#Detect if a file is in arff format
def is_arff_file(file_path):
    try:
        with open(file=file_path, mode='r', encoding='utf-8') as file:
            # Read the first few lines to check for ARFF attributes
            #first_lines = [file.readline().strip() for _ in range(15)]
            first_lines = [file.readline() for _ in range(15)]

            # Check if it contains ARFF-specific keywords in the header
            if any(line.lower().startswith('@relation') or line.lower().startswith('@attribute') for line in first_lines):
                return True
            else:
                return False
    except Exception as e:
        print(f"Error: {e}")
        return False

#Detect if a file is in arff format
def loadarfftoDataframe(file_path, showErrors=True):
    try:
        data, meta = arff.loadarff(file_path)
        # Convert the structured array to a Pandas DataFrame
        df1 = pd.DataFrame(data)

        # Decode categorical attributes to strings
        for column in df1.columns:
            if df1[column].dtype == 'object':
                df1[column] = df1[column].str.decode('utf-8')

        return df1, meta

    except arff.ParseArffError as e:
        
        if showErrors:
            print(f"Error: {e} in filepath: {file_path}")
        
        return None, None
    