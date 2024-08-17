import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the input and output directories
input_folder = "downsampled_csv_files/"
output_folder = "images/"
lane_change_file = "chunk1.csv"  # Update this path to the correct location

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the lane change data
lane_change_df = pd.read_csv(lane_change_file, delimiter=',')
lane_change_df.columns = lane_change_df.columns.str.strip()  # Remove any leading/trailing whitespace from column names

# Print the column names to debug
print("Lane change data columns:", lane_change_df.columns)

# Function to plot and save CSV files
def plot_csv(file_path, output_path, lane_change_data):
    # Load the data
    df = pd.read_csv(file_path, delimiter=';')
    
    # Normalize the timestamps to range from 0 to 60 seconds
    min_timestamp = df['timestamp'].min()
    max_timestamp = df['timestamp'].max()
    df['timestamp'] = 60 * (df['timestamp'] - min_timestamp) / (max_timestamp - min_timestamp)
    
    # Plotting the data
    plt.figure(figsize=(15, 7))
    plt.plot(df['timestamp'], df['accel_trans'], label='Transverse Acceleration', alpha=0.5, color='#ff7f0e')
    
    # Draw blue lines for lane changes
    for col in ['mapped first lane start', 'mapped first lane end', 'mapped 2 lane start', 'mapped 2 lane end', 'mapped lane 3 start', 'mapped line 3 end']:
        if col in lane_change_data and lane_change_data[col] > 0:
            plt.axvline(x=lane_change_data[col], color='blue', linestyle='--', alpha=0.7)
    
    # Add labels and legend
    plt.xlabel('Timestamp (seconds)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend(loc='upper left')
    
    # Save the plot as an image
    plt.title(os.path.basename(file_path))  # Use the file name as the title
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {output_path}")

# Iterate through CSV files in the input folder and lane change data
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.png")
        
        # Find the corresponding lane change data row by matching the file name
        # Skip the header row
        matching_rows = lane_change_df[lane_change_df.iloc[:, 1] == file_name]
        print(f"Processing {file_name} with lane change data:", matching_rows)
        if not matching_rows.empty:
            lane_change_data = matching_rows.iloc[0]  # Get the first matching row
            # print(f"Processing {file_name} with lane change data:", lane_change_data)
            plot_csv(file_path, output_path, lane_change_data)
        # else:
            # print(f"No corresponding lane change data for {file_name}. Skipping.")

print("All plots have been generated and saved.")
