import os
import csvMy as csv
import datasetFeatures as df
from scipy.io import arff
import pandas as pd

directory_path=os.path.join('features','all')

# Get a list of all entries in the directory
entries = os.listdir(directory_path)

files_with_paths = [os.path.join(directory_path, entry) for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
# Filter only files
files = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]

# Print the list of files
for file in files:
    filepath=os.path.join(directory_path,file)

    s100=''

    # if df.is_arff_file(filepath):

    #     #loads arff datafile into numpy structured array
    #     df1, meta = df.loadarfftoDataframe(filepath)
        
    #     # Save the first 100 rows of the DataFrame to a CSV format string with a header
    #     s100=df1.head(100).to_csv(path_or_buf=None, sep=';', index=False)

    # else:
    #     with open(filepath, encoding='utf8') as f:
    #         for x in range(100):
    #             s100+=f.readline()

    try:
        #loads arff datafile into numpy structured array
        df1, meta = df.loadarfftoDataframe(filepath)
        if df1 is not None:       
            # Save the first 100 rows of the DataFrame to a CSV format string with a header
            s100=df1.head(100).to_csv(path_or_buf=None, sep=';', index=False)
        else:
            with open(filepath, encoding='utf8') as f:
                for x in range(100):
                    s100+=f.readline()
    except Exception as e:
        with open(filepath, encoding='utf8') as f:
            for x in range(100):
                s100+=f.readline()

    dialect = csv.Sniffer().sniff(s100)  # Check what kind of csv/tsv file we have.

    hasHeader, header =csv.Sniffer().has_header(s100)
    df.datasetFeatures()._datasetFeatures_x(filepath,dialect.delimiter,hasHeader,datasetType=file[0])
