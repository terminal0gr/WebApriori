import os
import csvMy as csv
#import csv

#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '4', 'titanic02.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '4', 'titanic02WithoutHeader.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '3', 'a2100.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '3', 'a2.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '3', 'grocery_timestamp.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '3', 'supermarket.txt')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '2', 'invoice.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '2', 'OrderDetails.csv')
#filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '1', 'groceries.csv')
filepath=os.path.join('datasets', '79d1727987f200802593e3599119c966', '1', 'dataset.csv')


with open(filepath, encoding='utf8') as f:
    s10=''
    for x in range(100):
        s10+=f.readline()
    f.seek(0) # Go to start
    has_header = csv.Sniffer().has_header(s10)
    print(has_header)
    dialect = csv.Sniffer().sniff(s10)  # Check what kind of csv/tsv file we have.
    print(repr(dialect.delimiter))

with open(filepath, encoding='utf8') as csvfile:
    csv_test_bytes = csvfile.read(1024)  # Grab a sample of the CSV for format detection.
    csvfile.seek(0)  # Rewind
    has_header = csv.Sniffer().has_header(csv_test_bytes)  # Check to see if there's a header in the file.
    print(has_header)
    dialect = csv.Sniffer().sniff(csv_test_bytes)  # Check what kind of csv/tsv file we have.
    print(repr(dialect.delimiter))
    #inputreader = csv.reader(csvfile, dialect)
    #if has_header:
    #    next(inputreader) # Skip the header if we have one.
    #for row in inputreader:
    #    print(row)