import os
import shutil
import csv

# Paths
csv_file = './chunk1truefalse.csv'  # Path to your CSV file
source_folder = './downsampled_csv_files'  # Folder where the 188 files are
true_folder = './true'  # Destination folder for 'True' files
false_folder = './false'  # Destination folder for 'False' files

# Create destination folders if they dont exist
os.makedirs(true_folder, exist_ok=True)
os.makedirs(false_folder, exist_ok=True)

# 188 rows
with open(csv_file, mode='r') as file:
    csv_reader = csv.reader(file)
    true_false_list = [row[0].lower() == 'true' for row in csv_reader][:188] 


files_in_source = sorted(os.listdir(source_folder)) 


for idx, is_true in enumerate(true_false_list):
    if idx < len(files_in_source):
        file_name = files_in_source[idx]  
        source_file = os.path.join(source_folder, file_name)
        
        # Move the file based on True/False value
        if is_true:
            shutil.move(source_file, os.path.join(true_folder, file_name))
        else:
            shutil.move(source_file, os.path.join(false_folder, file_name))
    else:
        print(f"More rows in CSV than files in the source folder at index {idx}.")

print("File processing complete!")
