from datetime import datetime

# Function to extract the timestamp and return it for sorting
def extract_timestamp(line):
    try:
        # Split the line based on the delimiter '|'
        parts = line.split('|')
        # Extract the timestamp part and replace '--' with spaces
        timestamp_str = parts[1].replace('--', ' ')
        # Convert the timestamp to a datetime object
        return datetime.strptime(timestamp_str, '%Y-%m-%d %H-%M-%S')
    except (IndexError, ValueError):
        # Handle lines without a valid timestamp by returning None
        return None

# Function to extract the numeric part of the filename for secondary sorting
def extract_numeric_filename(line):
    try:
        # Split the line based on the delimiter '|'
        parts = line.split('|')
        # Extract the filename part and remove the '.csv'
        filename = parts[2].replace('.csv', '')
        # Return the numeric part of the filename for sorting
        return int(filename)
    except (IndexError, ValueError):
        # Handle lines without a valid filename by returning a high number
        return float('inf')

def rearrange_by_timestamp(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Filter out lines without valid timestamps and sort them
    sorted_lines = sorted(
        [line for line in lines if extract_timestamp(line) is not None],
        key=lambda line: (extract_timestamp(line), extract_numeric_filename(line))
    )

    # Write the sorted lines to a new file
    with open(output_file, 'w') as file:
        file.writelines(sorted_lines)

# Example usage
input_file = 'aa.txt'
output_file = 'output.txt'
rearrange_by_timestamp(input_file, output_file)
