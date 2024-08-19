import os
from scipy.io import arff
import pandas as pd
import numpy as np
from itertools import islice
import csv
import json

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

def loadarfftoDataframe(file_path, encoding='utf-8-sig', nRows=None):
    try:
        data, meta = arff.loadarff(file_path)
        # Convert the structured array to a Pandas DataFrame
        dataframe1 = pd.DataFrame.from_records(data,nRows=nRows)

        # Decode categorical attributes to strings
        for column in dataframe1.columns:
            if dataframe1[column].dtype == 'object':
                dataframe1[column] = dataframe1[column].str.decode(encoding)

        return dataframe1

    except arff.ParseArffError as e:
        return None
    
def readDataset(filepath, sep=';', encoding='utf-8-sig', hasHeader=True, nRows=None):
    dataset=None
    try:

        headerV1=None
        if hasHeader:
            headerV1=0

        if is_arff_file(filepath):
            dataset=loadarfftoDataframe(filepath, encoding)
        if not isinstance(dataset, pd.DataFrame):
            try:
                dataset = pd.read_csv(filepath, sep=sep, encoding=encoding, header=headerV1, nrows=nRows)
            except Exception:
                with open(filepath, mode='r') as file:
                    reader = csv.reader(file, delimiter=sep)
                    if nRows is None: #Read all the lines of the file
                        data = [line for line in reader]
                    else:
                        data = []
                        for i, row in enumerate(reader):
                            if i >= nRows:
                                break
                            data.append(row)

                    # Create a DataFrame from the list of lists
                    dataset = pd.DataFrame(data)                              
    
    except Exception as e:
        print(f"An error occurred: {e}")     
    finally:
        return dataset       

def countDatasetRecords(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        line_count = sum(1 for line in file)
    return line_count

def readJSONFromFile(filepath):

    if not os.path.exists(filepath): 
        return None
    else:
        try:

            # Open the JSON file in read mode
            with open(filepath, 'r') as file:
                # Load the JSON data from the file
                json_data = json.load(file)

        except Exception as e:
            return None
        
        # Now you can work with the JSON data as a Python dictionary or list
        return json_data
        