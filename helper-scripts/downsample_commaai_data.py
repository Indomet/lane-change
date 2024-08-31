import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.stats import norm
import numpy as np
import os
import shutil

def average_over_intervals(df, interval=10):
    """
    Averages the values of `accel_lon`, `accel_trans`, and `accel_z` over every `interval` rows.
    Uses the first timestamp of each interval to represent the group.
    
    Parameters:
    - df (pd.DataFrame): The original DataFrame.
    - interval (int): The number of rows to average over.
    
    Returns:
    - pd.DataFrame: The new DataFrame with averaged values.
    """
    # Initialize lists to store the results
    timestamps = []
    accel_lon_avg = []
    accel_trans_avg = []
    accel_z_avg = []

    # Iterate over the DataFrame in steps of 'interval'
    for start in range(0, len(df), interval):
        # Define the end of the current interval
        end = start + interval

        # Handle the case where the last group has fewer than `interval` rows
        if end > len(df):
            end = len(df)

        # Slice the DataFrame to get the current group
        df_slice = df.iloc[start:end]

        # Append the first timestamp of the group
        timestamps.append(df_slice['timestamp'].iloc[0])

        # Calculate and append the average of each column for the group
        accel_lon_avg.append(df_slice['accel_lon'].mean())
        accel_trans_avg.append(df_slice['accel_trans'].mean())
        accel_z_avg.append(df_slice['accel_z'].mean())

    # Create a new DataFrame from the results
    averaged_df = pd.DataFrame({
        'timestamp': timestamps,
        'accel_lon': accel_lon_avg,
        'accel_trans': accel_trans_avg,
        'accel_z': accel_z_avg
    })

    return averaged_df


def downsample_dataframe(df, factor=5):
    """
    Downsamples the DataFrame by selecting every nth row, where n is the downsample factor.

    Parameters:
    - df (pd.DataFrame): The original DataFrame to downsample.
    - factor (int): The downsampling factor (e.g., 5 means take 1 out of every 5 rows).

    Returns:
    - pd.DataFrame: The downsampled DataFrame.
    """
    # Downsample the DataFrame by selecting every nth row
    downsampled_df = df.iloc[::factor].reset_index(drop=True)
    
    return downsampled_df


file_3 = "test_data-7.csv" 
file_4 = "combined_segment.csv"
file_5 = "test_data-10.csv" 
file_6 = "test_data-7b.csv" 
file_7 = "test_data-12b.csv"
file_8 = "test_data-5b.csv" 
file_9 = "b0c9d2329ad1606b|2018-07-27--06-03-57|3.csv" 

base_path = './Chunks/Chunk_1'
inp_path = os.path.join(base_path, "raw_csv_files/")
out_path = os.path.join(base_path, "downsampled_csv_files/")

# Create directories if they do not exist

os.makedirs(out_path, exist_ok=True)
# df = pd.read_csv(path + file_9, delimiter=';')

# downsampled_df = downsample_dataframe(df, factor=10)
# downsampled_df.to_csv('smoothened_file.csv', sep=';', index=False)


# Base directory for the dataset
# base_dir = './Test_chunk'  # Assuming in the same directory as the script

# Initialize lists to hold the combined data and segment information
combined_t = []
combined_values = []
segment_info = []

# Iterate through each segment directory
for filename in os.listdir(inp_path):
    if filename.endswith('-acceleration.csv'):
        df = pd.read_csv(inp_path + filename, delimiter=';')
        averaged_df = average_over_intervals(df, interval=10)
        averaged_df.to_csv(os.path.join(out_path, 'avg-' + filename), sep=';', index=False)
        print(filename, ' saved.')
    elif filename.endswith("-steering.csv"):
        # Copy the file without downsampling
        shutil.copy(inp_path +filename, out_path+filename)