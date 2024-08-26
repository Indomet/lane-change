# Project Overview

This project consists of several Python scripts that process and analyze CSV data related to lane changes. Below is a brief description of each script and its functionality.

## Files

### `converter.py`
This script is responsible for converting raw data into a specific format required for further processing. It reads the input data from binary and saves the output in a csv.

### `downsample_commaai_data.py`
This script processes the raw CSV files by averaging acceleration data over specified intervals to reduce noise. It reads the raw CSV files from the raw_csv_files directory, performs the averaging, and saves the processed files to the downsampled_csv_files directory.

### `csvSeperator.py`
This script separates the downsampled CSV files into two categories: lane-change and no-lane-change. It reads the downsampled CSV files, gets the information from manually annotated csv about whether a lane change occurred or not and moves the files to the appropriate directories (`lane-change-csv` and `no-lane-change-csv`).

### `plotWithManualAnnotation.py`
This script processes CSV files containing lane change data by reading from two folders: one for lane changes and another for no lane changes. It normalizes the time data to start from 0 seconds to accurately represent the timeline and then creates a plot showing the vertical acceleration. Green lines are added to the plot at the moments when lane changes occurred, based on information from a reference CSV file that has been manually annotated (chunk1.csv). The script saves these plots as images in designated folders, ensuring those folders exist beforehand.


### `lc_detector.py`


## Running the Scripts

To run all the scripts in the correct order, you can use the `main.py` script. This script will sequentially execute the following scripts:

1. `converter.py`
2. `downsample_commaai_data.py`
3. `csvSeperator.py`
4. `plotWithManualAnnotation.py`

### Example Usage

```bash
python3 main.py