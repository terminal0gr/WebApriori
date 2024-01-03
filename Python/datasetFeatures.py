"""
datasetFeatures.py - create the features of a given dataset or dataset sample
Owner: Malliaridis Konstantinos PHd candidate
"""

import os
import pandas as pd
import numpy as np
import mysql.connector

class datasetFeatures:
    """Creates the features of a given dataset or dataset sample that can be used 
    in Machine learning experiments

    """
    _name=""
    AvgOfDistinctValuesPerCol = 0 #Range [0...1]
    AvgOfDistinctValuesOverAll = 0 #Range [0...1]
    AvgOfDistinctValuesPerRow = 0 #Range [0...1]
    FreqoFTop1FreqValue = 0 #Range [0...1]
    FreqoFTop2FreqValue = 0 #Range [0...1]
    FreqoFTop3FreqValue = 0 #Range [0...1]
    NumberOfColumns = 0 #Range [1...Infinite]
    FreqOfNumberCol = 0 #Range [0...1]
    FreqOfDateCol = 0 #Range [0...1]    
    FreqOfStringCol = 0 #Range [0...1]
    FreqOfBoolCol = 0 #Range [0...1]
    MinItemLen = 9999 #Range [0...infinite]
    MaxItemLen = 0 #Range [0...infinite]
    AvgItemLen = 0 #Range [0...infinite]
    Freq1CharColumns = 0 #Range [0...1]
    Freq2ValuesItemColumns = 0 #Range [0...1]
    HasHeader=None  
    datasetType=None

    def _datasetFeatures_x(self, filepath, delimiter, hasHeader, nrows=100, datasetType=None):
        # Creates the features of the dataset in order to determine datasetType via ML
        try:
            if hasHeader:
                df = pd.read_csv(filepath, sep=delimiter, nrows=nrows, header=0)
            else:
                df = pd.read_csv(filepath, sep=delimiter, nrows=nrows, header=None)

            class datasetFeaturesInst(datasetFeatures):
                _name=os.path.basename(filepath)

            freqplus=0
            numericColumns=0
            datetimeColumns=0
            twoValuesItemColumn=0
            for myCol in df.columns:
                uniqueValues=df[myCol].nunique()
                freq=uniqueValues/df.shape[0] #df.shape[0]->#rows
                freqplus+=freq
                if uniqueValues==2:
                    twoValuesItemColumn+=1
                
                try:
                    # At first check if you can recognise the column as number
                    df[myCol] = pd.to_numeric(df[myCol])
                    numericColumns+=1
                except ValueError:
                    try:
                        # If not then try to chack if it is a number but with comma as delimiter e.g. like greek regional settings
                        df[myCol] = pd.to_numeric(df[myCol].str.replace(',', '.'), errors='raise')
                        numericColumns+=1  
                    except ValueError:
                        try:
                            # If not a number the try to check if it is a date.
                            # to_datetime ensures that it will find that a column is datetime even if it has 
                            # other format than the expected (expected format yyy-mm-dd)
                            df[myCol] = pd.to_datetime(df[myCol])
                            datetimeColumns+=1
                        except ValueError:
                            # Ok it is not a datetime Column. So what!!!
                            datetimeColumns+=0

            datasetFeaturesInst.AvgOfDistinctValuesPerCol=freqplus/df.shape[1] #df.shape[1]->#Columns

            #From numeric columns we want to substract the columns that have only items 0 or 1 because we consider them to be boolean columns
            #(df.isin([0, 1]).all()).sum() --> count the columns that have as values 0 or 1
            datasetFeaturesInst.FreqOfNumberCol=(numericColumns-(df.isin([0, 1]).all()).sum())/df.shape[1]

            datasetFeaturesInst.FreqOfDateCol=datetimeColumns/df.shape[1]

            datasetFeaturesInst.Freq2ValuesItemColumns=twoValuesItemColumn/df.shape[1]

            #transform the 2-dimensional dataframe to 1-dimensional dataframe e.g. (100,7)->(700) rows
            df_1d = df.stack()
            df_1d = df_1d.reset_index(drop=True)
            #nunique counts the unique values of a dataframe column
            datasetFeaturesInst.AvgOfDistinctValuesOverAll=df_1d.nunique()/(df.shape[0]*df.shape[1])
            #Freq of the most frequent value
            most_frequent_item=df_1d.value_counts()[:3]
            i=0
            for si in most_frequent_item[:3]:
                i+=1
                if i==1:
                    datasetFeaturesInst.FreqoFTop1FreqValue=si/(df.shape[0]*df.shape[1])
                elif i==2:
                    datasetFeaturesInst.FreqoFTop2FreqValue=si/(df.shape[0]*df.shape[1])
                elif i==3:
                    datasetFeaturesInst.FreqoFTop3FreqValue=si/(df.shape[0]*df.shape[1])
        
            freq=0
            for i in range(df.shape[0]):
                freq+=df.loc[i].nunique()/df.shape[1] #df.shape[0]->#rows
            datasetFeaturesInst.AvgOfDistinctValuesPerRow=freq/df.shape[0] #df.shape[1]->#Columns

            datasetFeaturesInst.NumberOfColumns=df.shape[1]

            #len(df.select_dtypes(include='bool').columns) --> count the columns that have as Values True/False
            #(df.isin([0, 1]).all()).sum() --> count the columns that have as values 0 or 1
            datasetFeaturesInst.FreqOfBoolCol = (len(df.select_dtypes(include='bool').columns)+(df.isin([0, 1]).all()).sum())/df.shape[1]

            #All the other columns are of String/Object type 
            datasetFeaturesInst.FreqOfStringCol = 1-datasetFeaturesInst.FreqOfNumberCol-datasetFeaturesInst.FreqOfBoolCol-datasetFeaturesInst.FreqOfDateCol

            datasetFeaturesInst.MinItemLen = (df.applymap(lambda x: len(str(x)) if x is not None else 0).min()).min()
            datasetFeaturesInst.MaxItemLen = (df.applymap(lambda x: len(str(x)) if x is not None else 0).max()).max()
            datasetFeaturesInst.AvgItemLen = (df.applymap(lambda x: len(str(x)) if x is not None else 0).mean()).mean()

            # Count columns with only 1-character items
            datasetFeaturesInst.Freq1CharColumns = (df.applymap(lambda x: len(str(x)) == 1 if x is not None else False).all()).sum()/df.shape[1]

            datasetFeaturesInst.HasHeader=hasHeader

            datasetFeaturesInst.datasetType=datasetType

            self._WriteToDatabase(datasetFeaturesInst)

        except Exception as e:
            vbcrlf = '\n'
            print(f"Could not open/read or find dataset file!!!.{vbcrlf}Unexpected error: {e}{vbcrlf}")
            return None
        
    def _WriteToDatabase(self, dFI):
        
        # Replace these with your MySQL server and database information
        host = "localhost"
        user = "aprioriUser"
        password = "aprioripwd"
        database = "aprioriBase"

        # Create a connection to the MySQL server
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )

            if connection.is_connected():
                strsql="INSERT INTO `datasetfeatures` (`name`, `AvgOfDistinctValuesPerCol`, `AvgOfDistinctValuesOverAll`, `AvgOfDistinctValuesPerRow`, `FreqoFTop1FreqValue`, `FreqoFTop2FreqValue`, `FreqoFTop3FreqValue`, `NumberOfColumns`, `FreqOfNumberCol`, `FreqOfDateCol`, `FreqOfStringCol`, `FreqOfBoolCol`, `MinItemLen`, `MaxItemLen`, `AvgItemLen`, `Freq1CharColumns`, `Freq2ValuesItemColumns`, `datasetType`) \
                        VALUES ('" + dFI._name + "', \
                                '" + dFI.AvgOfDistinctValuesPerCol + "', \
                                '" + dFI.AvgOfDistinctValuesOverAll + "', \
                                '" + dFI.AvgOfDistinctValuesPerRow + "', \
                                '" + dFI.FreqoFTop1FreqValue + "', \
                                '" + dFI.FreqoFTop1FreqValue + "', \
                                '" + dFI.FreqoFTop3FreqValue + "', \
                                '" + dFI.NumberOfColumns + "', \
                                '" + dFI.FreqOfNumberCol + "', \
                                '" + dFI.FreqOfDateCol + "', \
                                '" + dFI.FreqOfStringCol + "', \
                                '" + dFI.FreqOfBoolCol + "', \
                                '" + dFI.MinItemLen + "', \
                                '" + dFI.MaxItemLen + "', \
                                '" + dFI.AvgItemLen + "', \
                                '" + dFI.Freq1CharColumns + "', \
                                '" + dFI.Freq2ValuesItemColumns + "', \
                                '" + dFI.HasHeader + "', \
                                '" + dFI.datasetType + "')"  
                cursor = connection.cursor()
                cursor.execute(strsql)                                    

        except mysql.connector.Error as e:
            print(f"Error: {e}")

