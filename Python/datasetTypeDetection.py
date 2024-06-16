"""
datasetTypeDetection.py - create the features of a given dataset or dataset sample
and auto detects its type in case is 0,2,3,4 type. 
Owner: Malliaridis Konstantinos PHd candidate
"""

import os
import pandas as pd
from joblib import load
import Global

missingValuesThreshold=0.2
nRows=500

class datasetFeatures:
    """Creates the features of a given dataset or dataset sample that can be used 
    in Machine learning experiments

    """
    _name=""
    AvgOfDistinctValuesPerCol = 0.0 #Range [0...1]
    AvgOfDistinctValuesOverAll = 0.0 #Range [0...1]
    AvgOfDistinctValuesPerRow = 0.0 #Range [0...1]
    Top1Value = None
    FreqOfTop1FreqValue = 0.0 #Range [0...1]
    FreqOfTop2FreqValue = 0.0 #Range [0...1]
    FreqOfTop3FreqValue = 0.0 #Range [0...1]
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
    delimiter=';'
    Header=[]
    type2Words=0 #Range [0...infinite]

    #This is not an attribute directly at least.
    datasetType=-1

    def _datasetFeatures_a(self, filepath, delimiter, hasHeader, nRows=nRows):
        # Creates the features of the dataset in order to determine datasetType via ML
        try:

            #The possible missing values that can exists in datasets and pandas cannot manipulate by default
            # extra_missing_values_light = ["n/a", "na"] #Useful only in 3 type recordset which may use "-", "?", "#" or None as absent value of an item
            # extra_missing_values_normal = ["n/a", "na", "-", "?", "#"] #all the other dataset types (0,2,4)

            headerV1=None
            if hasHeader:
                headerV1=0

            # try: #Try with extra_missing_values_normal
            #     df, meta = Global.loadarfftoDataframe(filepath,False)
            #     if df is None:       
            #         df = pd.read_csv(filepath, sep=delimiter, nrows=nRows, encoding='utf-8-sig', na_values = extra_missing_values_normal, header=headerV1)
            # except Exception as e:
            #     df = pd.read_csv(filepath, sep=delimiter, nrows=nRows, encoding='utf-8-sig', na_values = extra_missing_values_normal, header=headerV1)
            try: #Try with extra_missing_values_normal
                df, meta = Global.loadarfftoDataframe(filepath,False)
                if df is None:       
                    df = pd.read_csv(filepath, sep=delimiter, nrows=nRows, encoding='utf-8-sig', header=headerV1)
            except Exception as e:
                df = pd.read_csv(filepath, sep=delimiter, nrows=nRows, encoding='utf-8-sig', header=headerV1)
            
            class datasetFeaturesInst(datasetFeatures):
                _name=os.path.basename(filepath)

            # We want to find and keep the most frequent value because with df=df.fillna(0) later the value may change to 0 for ever!!!
            # Concatenate all columns into a single Series in ordeer to avoid iterating in all columns of the dataframe...
            all_values = pd.concat([df[col] for col in df.columns])

            # Find the most frequent value in the entire DataFrame
            datasetFeaturesInst.Top1Value = all_values.value_counts(dropna=False).idxmax()
            
            # Check if the Most frequent value is one of the P\possible strings that could represent the absent value in 3-SI dataset type
            if datasetFeaturesInst.Top1Value in ["n/a", "na", "-", "?", "#", False, "no", "No", "0"]:
                # If the most frequent value is more than 50% of all the values of the dataset then 
                # It is the absent value and the
                # dataset is 100% of type 3-SI. Additionally change NaN values to 0 For smoothness in the procedures below because is 3-SI we don't want absent value to be treated as missing value
                # Declare 3-SI type to dataset here without performing ML prediction afterwards.
                if all_values.value_counts(dropna=False).max()>= df.shape[1]*df.shape[0]*0.5:
                    datasetFeaturesInst.datasetType=3
                    df=df.fillna(0)   

            #DatasetType 3 special case.
            #Initially check if NaN value is the most frequent in the dataset.
            #If that happens then DatasetType is Most likely datasetType:3 and NaN Value is the absent value.
            #For smoothness in the procedures below, I change Nan value with 0.
            # countNaNValues=0
            # for myCol in df.columns:
            #     # if pd.isna(df[myCol].value_counts(dropna=False).idxmax()):
            #         countNaNValues+=df[myCol].value_counts(dropna=False).max()
            #If NaN values are more than 50% of all the values of the dataset then change them to 0
            #And declare 3-SI to dataset Type without performing ML prediction
            # if countNaNValues>= df.shape[1]*df.shape[0]*0.5:
            #     datasetFeaturesInst.datasetType=3
            #     df=df.fillna(0)   

            columnsCount=df.shape[1]
            columnsWithUnacceptedMissingValues=0

            for myCol in df.columns:
                #Remove the rows from current column that have missing values
                dfCol = df[myCol].dropna()
                if dfCol.shape[0]<(df[myCol].shape[0]*missingValuesThreshold): #The column {dfcol.name} of the dataset {os.path.basename(filepath)} is full (estimated more than 80%) of missing values and can't be analysed. The procedure ends with error.
                    columnsWithUnacceptedMissingValues+=1
                    print(f"The column {dfCol.name} of the dataset {os.path.basename(filepath)} is full (estimated more than 80%) of missing values and it will be omitted")

            if columnsWithUnacceptedMissingValues>columnsCount*missingValuesThreshold: 
                print(f"{columnsWithUnacceptedMissingValues} columns {columnsCount} of the dataset {os.path.basename(filepath)} has missing values more than 80% and the dataset and can't be analyzed. The procedure ends with error.")
                return None

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
                # if dfcol.shape[0]==0: #rows
                #     print(f"The column {dfcol.name} of {os.path.basename(filepath)} is full of missing values and can't be analysed. The procedure ends with error.")
                #     return None 
                # if dfcol.shape[0]>0 and dfcol.shape[0]<(df[myCol].shape[0]*0.2):
                #     print(f"The column {dfcol.name} of the dataset {os.path.basename(filepath)} is full (estimated more than 80%) of missing values and can't be analysed. The procedure ends with error.")
                #     return None 

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
                    datasetFeaturesInst.FreqOfTop1FreqValue=si/(df.shape[0]*df.shape[1])
                elif i==2:
                    datasetFeaturesInst.FreqOfTop2FreqValue=si/(df.shape[0]*df.shape[1])
                elif i==3:
                    datasetFeaturesInst.FreqOfTop3FreqValue=si/(df.shape[0]*df.shape[1])
        
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

        #_name, datasetType. Top1Value omitted intetionally. _name irrelevant, datasetType > Y (predicted datasetType)
        data = {
                'AvgOfDistinctValuesPerCol': [dFI.AvgOfDistinctValuesPerCol],
                'AvgOfDistinctValuesOverAll': [dFI.AvgOfDistinctValuesOverAll],
                'AvgOfDistinctValuesPerRow': [dFI.AvgOfDistinctValuesPerRow],
                'FreqOfTop1FreqValue': [dFI.FreqOfTop1FreqValue],
                'FreqOfTop2FreqValue': [dFI.FreqOfTop2FreqValue],  
                'FreqOfTop3FreqValue': [dFI.FreqOfTop3FreqValue],
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
        X_Pred = pd.DataFrame(data)

        #Load the trained model
        filepath=os.path.join('features','TrainedModel.joblib')
        rf_model = load(filepath)

        y_pred = rf_model.predict(X_Pred)

        return(y_pred[0])
