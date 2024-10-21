import os
import csvMy as csv
import pandas as pd

##################################
#Declaration Section
##################################
##################################

directory_path=os.path.join('ARM')

# Get a list of all entries in the directory
entries = os.listdir(directory_path)

files_with_paths = [os.path.join(directory_path, entry) for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
# Filter only files
files = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]

# Print the list of files
for file in files:
    filepath=os.path.join(directory_path,file)

    

    records=self.prepare_records()

    s1=''

    try:
        #loads arff datafile into numpy structured array
        df1, meta = df.loadarfftoDataframe(filepath)
        if df1 is not None:       
            # Save the first recsNo rows of the DataFrame to a CSV format string with a header
            s1=df1.head(recsNo).to_csv(path_or_buf=None, sep=';', index=False)
        else:
            with open(filepath, encoding='utf-8-sig') as f:
                for x in range(recsNo):
                    s1+=f.readline()
    except Exception as e:
        with open(filepath, encoding='utf-8-sig') as f:
            for x in range(recsNo):
                s1+=f.readline()

    dialect = csv.Sniffer().sniff(s1)  # Check what kind of csv/tsv file we have.

    hasHeader, header =csv.Sniffer().has_header(s1)

    df.datasetFeatures()._datasetFeatures_x(filepath,dialect.delimiter,hasHeader,datasetType=file[0],trainDataset=trainData)
