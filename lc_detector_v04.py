import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.stats import norm
import numpy as np


# Load the data
file_1 = "inverted_single_lane_change.csv"  
file_2 = "inverted_multiple_lane_change.csv"  
file_3 = "testdata_1-commaai.csv" # no need for the timestamp calculation
file_4 = "combined_segment.csv" # no need for the timestamp calculation
file_5 = "averaged_file-3.csv" # no need for the timestamp calculation
file_6 = "averaged_file-7.csv" # no need for the timestamp calculation
file_7 = "test_data-7.csv" # no need for the timestamp calculation
file_8 = "averaged_file-10.csv" # no need for the timestamp calculation
file_9 = "averaged-3_10-combined.csv" # no need for the timestamp calculation
file_10 = "averaged_file-7b.csv" # commaai # b0c9d2329ad1606b_2018-07-27--06-50-48/7 # two lane changes 
file_11 = "averaged_file-12b.csv" # commaai # b0c9d2329ad1606b_2018-07-27--06-50-48/7 # one lane change
file_12 = "averaged_file-5b.csv" # commaai # b0c9d2329ad1606b_2018-07-29--16-37-17/5 # two lane changes
file_13 = "averaged_file-9.csv" # commaai # b0c9d2329ad1606b_2018-07-30--13-44-30/9 # two lane changes

folder = "test_files/"
df = pd.read_csv(folder + file_2, delimiter=';')

# Convert timestamps to seconds
# df['timestamp'] = df['sampleTimeStamp_seconds'] + df['sampleTimeStamp_microseconds'] / 1e6 # do not use for commaai data

# Initialize parameters
min_duration = 800 / 1000  # seconds
max_duration = 5000 / 1000  # seconds
min_diff_time = 1000 / 1000  # seconds

# Define the limits for "normal" transverse acceleration
lower_limit = -1.1
upper_limit = 1.1

# Function to apply moving average smoothing
def moving_average(data, window_size=3):
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')

def check_slope(point, position):
    flag = False
    uncertainty = 0.2
    '''
    # counter = 0
    # prev_list = []
    # next_list = []

    # prev_list.append(df['accel_trans'].iloc[position - 1])
    # prev_list.append(df['accel_trans'].iloc[position - 2])
    # prev_list.append(df['accel_trans'].iloc[position - 3])
    # prev_list.append(df['accel_trans'].iloc[position - 4])

    # next_list.append(df['accel_trans'].iloc[position + 1])
    # next_list.append(df['accel_trans'].iloc[position + 2])
    # next_list.append(df['accel_trans'].iloc[position + 3])
    # next_list.append(df['accel_trans'].iloc[position + 4])

    # if point == "Point 1":
    #     for i in range(0, 4):
    #         if prev_list[i]  < upper_limit and next_list[i] > upper_limit:
    #             counter += 1
    # elif point == "Point 2":
    #     for i in range(0, 4):
    #         if prev_list[i] > upper_limit and next_list[i] < upper_limit:
    #             counter += 1
    # elif point == "Point 3":
    #     for i in range(0, 4):
    #         if prev_list[i] > lower_limit and next_list[i] < lower_limit:
    #             counter += 1
    # elif point == "Point 4":
    #     for i in range(0, 4):
    #         if prev_list[i] < lower_limit and next_list[i] > lower_limit:
    #             counter += 1
    # if counter == 4:
    #     # print("Counter: ", counter)
    #     flag = True
    '''
    if point == "Point 1" or point == "Point 4":
        if df['accel_trans'].iloc[position - 1] - uncertainty < df['accel_trans'].iloc[position] < df['accel_trans'].iloc[position + 1] + uncertainty < df['accel_trans'].iloc[position + 2] + uncertainty:
            flag = True
    elif point == "Point 2" or point == "Point 3":
        if df['accel_trans'].iloc[position - 1] + uncertainty > df['accel_trans'].iloc[position] > df['accel_trans'].iloc[position + 1] - uncertainty:
            flag = True

    return flag


def detect_lane_change_events(df):
    events = []
    in_maneuver = False
    event_start_time = None
    positive_peak_detected = False
    negative_peak_detected = False
    counter = 0
    step_limit = 66

    for i in range(2, len(df) - 2):
        current_time = df['timestamp'].iloc[i]
        curr_trans_accel = df['accel_trans'].iloc[i]
       
        if not in_maneuver:
            # Look for the start of a maneuver
            if curr_trans_accel >= upper_limit and check_slope("Point 1", i):
                in_maneuver = True
                event_start_time = current_time
                positive_peak_detected = True
                print("----Positive peak True----")
                print(curr_trans_accel, current_time)
        else:
            # During a maneuver
            if positive_peak_detected:
                # Check if it returns to normal after positive peak
                if lower_limit <= curr_trans_accel <= upper_limit and check_slope("Point 2", i):
                    positive_peak_detected = False
                    print("----Positive peak False----")
                    print(curr_trans_accel, current_time)
            else:
                # Look for the negative peak
                counter += 1
                print(counter)
                if counter >= step_limit:
                    in_maneuver = False
                    positive_peak_detected = False
                    print(counter)
                    counter = 0
                    continue
                if curr_trans_accel <= lower_limit and check_slope("Point 3", i):
                    counter = 0
                    if not negative_peak_detected:
                        negative_peak_detected = True
                        print("----Negative peak True----")
                        print(curr_trans_accel, current_time)
                elif negative_peak_detected:
                    # print(curr_trans_accel)
                    if lower_limit <= curr_trans_accel <= upper_limit and check_slope("Point 4", i):
                        counter = 0
                        negative_peak_detected = False
                        print("----Negative peak False----")
                        print(curr_trans_accel, current_time)
                        event_end_time = current_time
                        duration = event_end_time - event_start_time
                        if min_duration <= duration <= max_duration:
                            events.append((event_start_time, event_end_time, duration))
                            print(f"Detected Lane Change Event: Start Time = {event_start_time}, End Time = {event_end_time}, Duration = {duration} seconds")
                        in_maneuver = False
                        event_start_time = None
    return events


# Apply moving average smoothing to the acceleration values
# df['accel_trans'] = moving_average(np.array(df['accel_trans']), window_size=15)

# save the smoothened file
# df.to_csv('smoothened_file.csv', sep=';', index=False)

# Detect lane change events
lane_change_events = detect_lane_change_events(df)

# Convert lane change events to a DataFrame for easier handling
events_df = pd.DataFrame(lane_change_events, columns=['start_time', 'end_time', 'duration'])

# Save the start and end times to a CSV file
events_df.to_csv('lane_change_events.csv', index=False)

# Plotting the results
plt.figure(figsize=(15, 7))

# plt.plot(df['timestamp'], df['accel_lon'], label='Longitudinal Acceleration', alpha=0.5)
plt.plot(df['timestamp'], df['accel_trans'], label='Transverse Acceleration', alpha=0.5, color='#ff7f0e')

# Plot the start and end times of each event with red dashed lines
for i, (start, end, _) in enumerate(lane_change_events, start=1):
    plt.axvline(x=start, color='red', linestyle='--', linewidth=0.5)
    plt.axvline(x=end, color='red', linestyle='--', linewidth=0.5)
    plt.text(start, plt.gca().get_ylim()[1], f'Event {i}', fontsize=8, verticalalignment='bottom', horizontalalignment='right')

plt.xlabel('Timestamp (seconds)')
plt.ylabel('Acceleration (m/s²)')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
# plt.savefig('AccelerationData-start_end.png')
plt.show()
