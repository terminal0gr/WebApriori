import os
import json
import csv
import datetime
import time

def get_file_creation_date(file_path):
    try:
        if os.name == 'nt':  # Windows
            creation_time = os.path.getctime(file_path)
        else:  # Unix-based systems
            stat = os.stat(file_path)
            creation_time = getattr(stat, 'st_birthtime', stat.st_ctime)
        
        # Convert timestamp to a readable format
        formatted_date = datetime.datetime.fromtimestamp(creation_time).strftime("%Y/%m/%d %H:%M")
        return formatted_date
    except Exception as e:
        print(f"Error: {e}")
        return None

# Directory containing the JSON files
directory_path = "output"

# Output CSV file
output_csv = "output/results.csv"

# Define the CSV header
csv_header = [
    "filename", 
    "dataset", 
    "Algorithm", 
    "Language", 
    "library", 
    "minSup", 
    "totalFI", 
    "Runtime", 
    "Memory",
    "topK",
    "Rank",
    "Items",
    "TopK 1-itemsets",
    "Date",
    "Time"
]

# Open the CSV file for writing
with open(output_csv, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    
    # Write the header
    writer.writerow(csv_header)
    
    # Iterate through JSON files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".json"):
            # Full path to the JSON file
            file_path = os.path.join(directory_path, file_name)
            
            try:
                # Read the JSON file
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
                
                # Extract dataset from the filename (substring before the first '_')
                dataset = file_name.split('_')[0]
                
                datetime1=get_file_creation_date(file_path).split(' ')

                # Write a row in the CSV file
                writer.writerow([
                    file_name.replace(".json", ""),  # filename without extension
                    dataset,                         # dataset
                    data.get("Algorithm", ""),       # Algorithm
                    data.get("Language", ""),        # Language
                    data.get("library", ""),         # library
                    str(data.get("minSup", "")).replace('.',','),          # minSup
                    data.get("totalFI", ""),         # totalFI
                    str(data.get("Runtime", "")).replace('.',','),         # Runtime
                    str(data.get("Memory", "")).replace('.',','),           # Memory
                    data.get("topK", ""),
                    data.get("Rank", ""),
                    data.get("Items", ""),
                    data.get("TopK 1-itemsets", ""),
                    datetime1[0],
                    datetime1[1]
                ])
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error processing file {file_name}: {e}")

print(f"CSV file created successfully at {output_csv}")

