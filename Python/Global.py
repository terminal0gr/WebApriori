import os
from scipy.io import arff
import pandas as pd
import numpy as np
import mysql.connector

#Detect if a file is in arff format
def is_arff_file(file_path, Show_Errors=False):
    try:
        with open(file=file_path, mode='r', encoding='utf-8-sig') as file:
            # Read the first few lines to check for ARFF attributes
            #first_lines = [file.readline().strip() for _ in range(15)]
            first_lines = [file.readline() for _ in range(15)]

            # Check if it contains ARFF-specific keywords in the header
            if any(line.lower().startswith('@relation') or line.lower().startswith('@attribute') for line in first_lines):
                return True
            else:
                return False
    except Exception as e:
        if Show_Errors:
            print(f"Error: {e}")
        return False

def loadarfftoDataframe(file_path, encoding='utf-8-sig'):
    try:
        data, meta = arff.loadarff(file_path)
        # Convert the structured array to a Pandas DataFrame
        dataframe1 = pd.DataFrame(data)

        # Decode categorical attributes to strings
        for column in dataframe1.columns:
            if dataframe1[column].dtype == 'object':
                dataframe1[column] = dataframe1[column].str.decode(encoding)

        return dataframe1

    except arff.ParseArffError as e:
        return None
    
def readDataset(filepath, sep=';', encoding='utf-8-sig', hasHeader=True):
    dataset=None
    try:
        if is_arff_file(filepath):
            dataset=loadarfftoDataframe(filepath, encoding)
        if not isinstance(dataset, pd.DataFrame):
            if hasHeader:
                dataset = pd.read_csv(filepath, sep=sep, encoding=encoding)
            else:
                dataset = pd.read_csv(filepath, sep=sep, encoding=encoding, header=None)
    
    except Exception as e:
        print(f"An error occurred: {e}")     
    finally:
        return dataset       
