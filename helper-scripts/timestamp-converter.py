import os
import numpy as np
import pandas as pd


base_dir = './Chunk_1'

base_path = './Chunks/Chunk_1'
path = os.path.join(base_path, 'timeframe_csv_files')
os.makedirs(path, exist_ok=True)

combined_t = []
combined_values = []
segment_info = []
# Walk through the directories in base_dir
for root, dirs, files in os.walk(base_dir):
    
    combined_t = []
    combined_values = []
    segment_info = []

    if 'frame_times' in files:
        # Load the frame times
        frame_data = np.load(os.path.join(root, 'frame_times')) 
        
        folder_id = os.path.basename(
            os.path.dirname(
                os.path.dirname(root )
            )
        )
        
        segment_number = os.path.basename(
            os.path.dirname(root   )
        )
        

        df_frames = pd.DataFrame({'timestamp': frame_data})
        

        file_name = f"{folder_id}|{segment_number}-frame_times.csv"
        
 
        csv_path = os.path.join(path, file_name)
        df_frames.to_csv(csv_path, sep=';', index=False)
        print(f"{file_name} saved.")
