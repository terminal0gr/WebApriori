import os
import csvMy as csv
import datasetFeatures as df

directory_path=os.path.join('features','all')

# Get a list of all entries in the directory
entries = os.listdir(directory_path)

files_with_paths = [os.path.join(directory_path, entry) for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
# Filter only files
files = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]

# Print the list of files
for file in files:
    filepath=os.path.join(directory_path,file)
    with open(filepath, encoding='utf8') as f:
        s100=''

        for x in range(100):
            s100+=f.readline()

        dialect = csv.Sniffer().sniff(s100)  # Check what kind of csv/tsv file we have.

        df.datasetFeatures()._datasetFeatures_x(filepath,dialect.delimiter,csv.Sniffer().has_header(s100),datasetType=file[0])
