import os
import shutil
import csv

def clean_filename(filename):
    # List of strings to remove
    strings_to_remove = ["avg-", "-acceleration", "-steering"]
    
    # Iterate over each string to remove and replace it with an empty string
    for string in strings_to_remove:
        filename = filename.replace(string, "")
    
    return filename

# Paths
base_path = './Chunks/Chunk_1'
csv_files_path = 'manually_annotated_chunks/'
csv_file = os.path.join(csv_files_path, 'chunk1.csv')
source_folder = os.path.join(base_path, 'downsampled_csv_files')
true_folder = os.path.join(base_path, 'manually-annotated/lane-change-csv')
false_folder = os.path.join(base_path, 'manually-annotated/no-lane-change-csv')

# Create destination folders if they don't exist
os.makedirs(true_folder, exist_ok=True)
os.makedirs(false_folder, exist_ok=True)

# Read the CSV file into a list of dictionaries
with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    true_false_list = [{row['folder name']: row['lane change'].lower() == 'true'} for row in csv_reader]

# Iterate through the files in the source folder
for file_name in os.listdir(source_folder):
    source_file = os.path.join(source_folder, file_name)
    
    # Clean the file name
    cleaned_file_name = clean_filename(file_name)
    
    # Find the matching row in the CSV file
    matching_rows = [row for row in true_false_list if cleaned_file_name in row]
    
    if matching_rows:
        is_true = matching_rows[0][cleaned_file_name]
        
        # Move the file based on True/False value
        if is_true:
            shutil.copy(source_file, os.path.join(true_folder, file_name))
        else:
            shutil.copy(source_file, os.path.join(false_folder, file_name))
    else:
        print(f"No matching row for file {file_name} in CSV.")

print("File processing complete!")
