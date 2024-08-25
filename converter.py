import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Base directory for the dataset
base_dir = './Chunk_1' 

# Initialize lists to hold the combined data and segment information
combined_t = []
combined_values = []
segment_info = []

base_path = 'Chunks/Chunk_1'
path = os.path.join(base_path, 'raw_csv_files')

# Create the directory if it does not exist
os.makedirs(path, exist_ok=True)
# Iterate through each segment directory
for root, dirs, files in os.walk(base_dir):
    combined_t = []
    combined_values = []
    segment_info = []
    if 'accelerometer' in root and 't' in files and 'value' in files:
        # Load the time and value data
        t_data = np.load(os.path.join(root, 't'))
        value_data = np.load(os.path.join(root, 'value'))
        
        # Append the data to the combined lists
        combined_t.extend(t_data)
        combined_values.extend(value_data)
        
        # Extract the segment number, which is two levels up from the current directory
        folder_id = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(root)))))
        segment_number = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(root))))
        # segment_info.append((segment_number, t_data[0], t_data[-1]))
        
        # Convert the combined lists to numpy arrays
        combined_t = np.array(combined_t)
        combined_values = np.array(combined_values)

        df_combined = pd.DataFrame({
            'timestamp': combined_t,
            'accel_lon': combined_values[:, 0],
            'accel_trans': combined_values[:, 1],
            'accel_z': combined_values[:, 2]
        })

        file_name = folder_id + '|' + segment_number + '.csv'
        df_combined.to_csv(os.path.join(path, file_name), sep=';', index=False)
        print(file_name, ' saved.')


