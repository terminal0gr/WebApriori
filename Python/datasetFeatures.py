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
    sFreqOfBoolCol = 0 #Range [0...1]


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
            for myCol in df.columns:
                freq=df[myCol].nunique()/df.shape[0] #df.shape[0]->#rows
                freqplus+=freq
            datasetFeaturesInst.AvgOfDistinctValuesPerCol=freqplus/df.shape[1] #df.shape[1]->#Columns

            #transform the 2-dimensional dataframe to 1-dimensional dataframe e.g. (100,7)->(700) rows
            df_1d = df.stack()
            df_1d = df_1d.reset_index(drop=True)
            #nunique counts the unique values of a dataframe column
            datasetFeaturesInst.AvgOfDistinctValuesOverAll=df_1d.nunique()/(df.shape[0]*df.shape[1])

            freq=0
            for i in range(df.shape[0]):
                freq+=df.loc[i].nunique()/df.shape[1] #df.shape[0]->#rows
            datasetFeaturesInst.AvgOfDistinctValuesPerRow=freq/df.shape[0] #df.shape[1]->#Columns

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
