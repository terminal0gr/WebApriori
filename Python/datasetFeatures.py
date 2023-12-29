"""
datasetFeatures.py - create the features of a given dataset or dataset sample
Owner: Malliaridis Konstantinos PHd candidate
"""

import pandas as pd
import numpy as np

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


    def _datasetFeatures_x(self, filepath, delimiter, hasHeader, nrows=100):
        # Creates the features of the dataset in order to determine datasetType via ML
        try:
            if hasHeader:
                df = pd.read_csv(filepath, sep=delimiter, nrows=nrows, header=0)
            else:
                df = pd.read_csv(filepath, sep=delimiter, nrows=nrows, header=None)

            class datasetFeaturesInst(datasetFeatures):
                _name="Sniffed"

            freqplus=0
            numericColumns=0
            datetimeColumns=0
            for myCol in df.columns:
                freq=df[myCol].nunique()/df.shape[0] #df.shape[0]->#rows
                freqplus+=freq
                
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


            # for dfColumn in df.columns:

            # data1= pd.to_datetime(df['Date'])

            # print(df.info())
 
            # # display
            # print(data1.head())

            # datetime_columns = df.select_dtypes(include=['datetime', 'datetime64'])

            # Count the number of datetime columns
            # num_datetime_columns = len(datetime_columns.columns)

            datasetFeaturesInst.FreqOfDateCol = len(df.select_dtypes(include=['datetime', 'datetime64']))/df.shape[1]

            # list_of_lists = [line.split(delimiter) for line in data.split('\n')]
            # print(list_of_lists)
            # if hasHeader:

            # else:

            # # Convert the string array into a list of lists
            # list_of_lists = [line.split("\n") for line in data]
            # # Create a Pandas DataFrame
            # columns = ["Name", "Age", "Occupation"]
            # df = pd.DataFrame(list_of_lists, columns=columns)

            # pd.DataFrame=data
            # print(pd)
            # data = pd.read_csv(filepath, sep=datasetSep)
        except Exception as e:
            vbcrlf = '\n'
            print(f"Could not open/read or find dataset file!!!.{vbcrlf}Unexpected error: {e}{vbcrlf}")
            return None
