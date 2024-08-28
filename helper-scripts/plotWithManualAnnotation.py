import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.signal import savgol_filter

# Define the base path
base_path = './Chunks/Chunk_1/manually-annotated/'
csv_files_path = 'manually_annotated_chunks/'

# Define the input and output directories
input_folders = {
    'lane-change-csv': os.path.join(base_path, 'lane-change-csv'),
    'no-lane-change-csv': os.path.join(base_path, 'no-lane-change-csv')
}

output_folders = {
    'lane-change-csv': os.path.join(base_path, 'lane-change-images'),
    'no-lane-change-csv': os.path.join(base_path, 'no-lane-change-images')
}

# Create the output folders if they don't exist
for folder in output_folders.values():
    os.makedirs(folder, exist_ok=True)

# Read the lane change data
lane_change_file = os.path.join(csv_files_path, "chunk1.csv")
lane_change_data = pd.read_csv(lane_change_file)

# Function to apply noise reduction based on steering angle
def apply_noise_reduction(accel_df, steer_df, window_size=11, polyorder=2, threshold=0.5):
    accel_df = accel_df.drop_duplicates(subset='timestamp')
    steer_df = steer_df.drop_duplicates(subset='timestamp')

    steer_df = steer_df.set_index('timestamp').reindex(accel_df['timestamp']).interpolate().reset_index()
    steer_df['steering_angle_diff'] = steer_df['steering_angle'].diff().fillna(0)
    significant_steering = np.abs(steer_df['steering_angle_diff']) > threshold

    accel_df['accel_trans_smoothed'] = savgol_filter(accel_df['accel_trans'], window_length=window_size, polyorder=polyorder)
    accel_df['accel_trans_smoothed'] = np.where(
        significant_steering,
        accel_df['accel_trans'],
        accel_df['accel_trans_smoothed']
    )

    return accel_df['accel_trans_smoothed']

# Function to adjust transverse acceleration based on steering angle
def adjust_transverse_acceleration(accel_df, steer_df, correction_factor=0.1):
    steer_df['steering_angle_normalized'] = steer_df['steering_angle'] - steer_df['steering_angle'].mean()
    accel_df['accel_trans_adjusted'] = accel_df['accel_trans'] - (steer_df['steering_angle_normalized'] * correction_factor)
    accel_df['accel_trans_adjusted_smoothed'] = accel_df['accel_trans_adjusted'].rolling(window=5).mean()
    return accel_df

# Function to plot and save adjusted data with enhanced visuals
def plot_adjusted_csv(accel_file, steer_file, output_path, lane_change_seconds):
    accel_df = pd.read_csv(accel_file, delimiter=';')
    steer_df = pd.read_csv(steer_file, delimiter=';')

    if 'timestamp' not in accel_df.columns or 'accel_trans' not in accel_df.columns:
        print(f"Columns 'timestamp' or 'accel_trans' are missing in {accel_file}. Skipping.")
        return

    if 'timestamp' not in steer_df.columns or 'steering_angle' not in steer_df.columns:
        print(f"Columns 'timestamp' or 'steering_angle' are missing in {steer_file}. Skipping.")
        return

    min_timestamp = accel_df['timestamp'].min()
    max_timestamp = accel_df['timestamp'].max()
    accel_df['timestamp'] = 60 * (accel_df['timestamp'] - min_timestamp) / (max_timestamp - min_timestamp)
    steer_df['timestamp'] = 60 * (steer_df['timestamp'] - min_timestamp) / (max_timestamp - min_timestamp)

    accel_df = adjust_transverse_acceleration(accel_df, steer_df)

    steer_df['steering_angle_smoothed'] = steer_df['steering_angle'].rolling(window=5).mean()

    fig, ax1 = plt.subplots(figsize=(15, 7))
    ax1.plot(accel_df['timestamp'], accel_df['accel_trans_adjusted_smoothed'], label='Adjusted Transverse Acceleration (Smoothed)', color='#ff7f0e')
    ax1.set_xlabel('Timestamp (seconds)')
    ax1.set_ylabel('Adjusted Transverse Acceleration (m/s²)', color='#ff7f0e')

    ax2 = ax1.twinx()
    ax2.plot(steer_df['timestamp'], steer_df['steering_angle_smoothed'], label='Steering Angle (Smoothed)', color='#0000FF', alpha=0.7)
    ax2.set_ylabel('Steering Angle (degrees)', color='#0000FF')

    for second in lane_change_seconds:
        ax1.axvline(x=second, color='g', linewidth=0.5, linestyle='--')

    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    plt.title(os.path.basename(output_path).replace('.png', ''))
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {output_path}")

# Iterate through each input folder
for folder_key, folder_path in input_folders.items():
    output_folder = output_folders[folder_key]

    accel_files = sorted([f for f in os.listdir(folder_path) if 'acceleration' in f])
    steer_files = sorted([f for f in os.listdir(folder_path) if 'steering' in f])

    for accel_file, steer_file in zip(accel_files, steer_files):
        accel_file_path = os.path.join(folder_path, accel_file)
        steer_file_path = os.path.join(folder_path, steer_file)
        output_file_name = accel_file.replace('-acceleration.csv', '-combined.png')
        output_path = os.path.join(output_folder, output_file_name)

        matching_rows = lane_change_data[lane_change_data.iloc[:, 0] == accel_file.replace("avg-", "").replace('-acceleration', '')]
        if not matching_rows.empty:
            lane_change_row = matching_rows.iloc[0]
            lane_change_seconds = []
            for column_name, value in lane_change_row.items():
                if column_name != "lane change":
                    try:
                        second = float(value)
                        if second != 0:
                            lane_change_seconds.append(second * 1.25)
                    except ValueError:
                        pass

            lane_change_seconds = [x for x in lane_change_seconds if not np.isnan(x)]
            print(f"File: {accel_file}, Lane Change Seconds: {lane_change_seconds}")
            plot_adjusted_csv(accel_file_path, steer_file_path, output_path, lane_change_seconds)
        else:
            print(f"No matching lane change data for {accel_file}")

print("All combined plots have been generated and saved.")
