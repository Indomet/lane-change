import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the input and output directories
input_folder = "downsampled_csv_files/"
lane_change_file = "chunk1.csv"
output_folder = "images/"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the lane change data
lane_change_data = pd.read_csv(lane_change_file)

# Function to plot and save CSV files
def plot_csv(file_path, output_path, lane_change_seconds):
    # Load the data
    df = pd.read_csv(file_path, delimiter=';')
    
    # Check if necessary columns exist
    if 'timestamp' not in df.columns or 'accel_trans' not in df.columns:
        print(f"Columns 'timestamp' or 'accel_trans' are missing in {file_path}. Skipping.")
        return
    
    # Normalize the timestamps to range from 0 to 60 seconds
    min_timestamp = df['timestamp'].min()
    max_timestamp = df['timestamp'].max()
    df['timestamp'] = 60 * (df['timestamp'] - min_timestamp) / (max_timestamp - min_timestamp)
    
    # Plotting the data
    plt.figure(figsize=(15, 7))
    plt.plot(df['timestamp'], df['accel_trans'], label='Transverse Acceleration', alpha=0.5, color='#ff7f0e')
    
    # Draw lines based on the lane change seconds
    for second in lane_change_seconds:
        plt.axvline(x=second, color='r', linestyle='--')
    
    # Add labels and legend
    plt.xlabel('Timestamp (seconds)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend(loc='upper left')
    
    # Save the plot as an image
    plt.title(os.path.basename(file_path))  # Use the file name as the title
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {output_path}")

# Iterate through CSV files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.png")
        
        # Find the corresponding lane change data row by matching the file name
        matching_rows = lane_change_data[lane_change_data.iloc[:, 0] == file_name.replace("avg-", "")]
        if not matching_rows.empty:
            lane_change_row = matching_rows.iloc[0]
            lane_change_seconds = []
            for value in lane_change_row[1:]:
                if value not in ['', 'TRUE', 'FALSE', '0.0','0']:
                    try:
                        second = float(value)
                        if second != 0:  # Ignore 0 values
                            lane_change_seconds.append(second)
                    except ValueError:
                        pass
            
            # Debug statement to print the lane change seconds
            print(f"File: {file_name}, Lane Change Seconds: {lane_change_seconds}")
            plot_csv(file_path, output_path, lane_change_seconds)
        else:
            print(f"No matching lane change data for {file_name}")

print("All plots have been generated and saved.")