import os
import shutil
import csv

# Paths
csv_file = 'chunk1truefalse.csv'  # Path to your CSV file
source_folder = 'downsampled_csv_files'  # Folder where the 188 files are
true_folder = 'true'  # Destination folder for 'True' files
false_folder = 'false'  # Destination folder for 'False' files

# Create destination folders if they don't exist
os.makedirs(true_folder, exist_ok=True)
os.makedirs(false_folder, exist_ok=True)

# Read the CSV file into a list of tuples (file_name, is_true)
with open(csv_file, mode='r') as file:
    csv_reader = csv.reader(file)
    true_false_list = [(row[0], row[1].lower() == 'true') for row in csv_reader]

# Iterate through the files in the source folder
for file_name in os.listdir(source_folder):
    source_file = os.path.join(source_folder, file_name)
    
    # Remove "avg-" prefix if it exists
    stripped_file_name = file_name[4:] if file_name.startswith("avg-") else file_name
    
    # Find the matching row in the CSV file
    matching_rows = [row for row in true_false_list if row[0] == stripped_file_name]
    
    if matching_rows:
        is_true = matching_rows[0][1]
        
        # Move the file based on True/False value
        if is_true:
            shutil.copy(source_file, os.path.join(true_folder, file_name))
        else:
            shutil.copy(source_file, os.path.join(false_folder, file_name))
    else:
        print(f"No matching row for file {file_name} in CSV.")

print("File processing complete!")