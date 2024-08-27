import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the base path
base_path = './Chunks/Chunk_1/manually-annotated/'
csv_files_path = 'manually_annotated_chunks/'

# Define the input and output directories
input_folder = {
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

# Function to plot and save combined CSV files (acceleration and steering)
def plot_combined_csv(accel_file, steer_file, output_path, lane_change_seconds):
    # Load the data
    accel_df = pd.read_csv(accel_file, delimiter=';')
    steer_df = pd.read_csv(steer_file, delimiter=';')
    
    # Check if necessary columns exist
    if 'timestamp' not in accel_df.columns or 'accel_trans' not in accel_df.columns:
        print(f"Columns 'timestamp' or 'accel_trans' are missing in {accel_file}. Skipping.")
        return
    
    if 'timestamp' not in steer_df.columns or 'steering_angle' not in steer_df.columns:
        print(f"Columns 'timestamp' or 'steering_angle' are missing in {steer_file}. Skipping.")
        return
    
    # Normalize the timestamps to range from 0 to 60 seconds
    min_timestamp = accel_df['timestamp'].min()
    max_timestamp = accel_df['timestamp'].max()
    accel_df['timestamp'] = 60 * (accel_df['timestamp'] - min_timestamp) / (max_timestamp - min_timestamp)
    steer_df['timestamp'] = 60 * (steer_df['timestamp'] - min_timestamp) / (max_timestamp - min_timestamp)
    
    # Plotting the data
    plt.figure(figsize=(15, 7))
    plt.plot(accel_df['timestamp'], accel_df['accel_trans'], label='Transverse Acceleration', alpha=0.5, color='#ff7f0e')
    plt.plot(steer_df['timestamp'], steer_df['steering_angle'], label='Steering Angle', alpha=0.5, color='#0000FF')

    # Draw lines based on the lane change seconds
    for second in lane_change_seconds:
        plt.axvline(x=second, color='g', linewidth=0.5, linestyle='--')
    
    # Add labels and legend
    plt.xlabel('Timestamp (seconds)')
    plt.ylabel('Value')
    plt.legend(loc='upper left')
    
    # Save the plot as an image
    plt.title(os.path.basename(output_path).replace('.png', ''))  # Use the output file name as the title
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {output_path}")

# Iterate through each input folder
for folder_key, input_folder in input_folder.items():
    output_folder = output_folders[folder_key]
    
    # Filter acceleration and steering files
    accel_files = sorted([f for f in os.listdir(input_folder) if 'acceleration' in f])
    steer_files = sorted([f for f in os.listdir(input_folder) if 'steering' in f])
    
    for accel_file, steer_file in zip(accel_files, steer_files):
        # Construct the full paths for acceleration and steering files
        accel_file_path = os.path.join(input_folder, accel_file)
        steer_file_path = os.path.join(input_folder, steer_file)
        
        # Construct the output image file path
        output_file_name = accel_file.replace('-acceleration.csv', '-combined.png')
        output_path = os.path.join(output_folder, output_file_name)
        
        # Find the corresponding lane change data row by matching the file name
        matching_rows = lane_change_data[lane_change_data.iloc[:, 0] == accel_file.replace("avg-", "").replace('-acceleration', '')]
        if not matching_rows.empty:
            lane_change_row = matching_rows.iloc[0]
            lane_change_seconds = []
            for column_name, value in lane_change_row.items():
                if column_name != "lane change":
                    try:
                        second = float(value)
                        if second != 0:  # Ignore 0 values
                            # Multiply by 1.25 since the videos are fast-forwarded
                            lane_change_seconds.append(second * 1.25)
                    except ValueError:
                        pass
            
            # Print the lane change seconds on the console
            print(f"File: {accel_file}, Lane Change Seconds: {lane_change_seconds}")
            plot_combined_csv(accel_file_path, steer_file_path, output_path, lane_change_seconds)
        else:
            print(f"No matching lane change data for {accel_file}")

print("All combined plots have been generated and saved.")
