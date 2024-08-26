import subprocess

def run_script(script_name):
    try:
        print(f"running {script_name}...")
        result = subprocess.run(['python3', script_name], check=True, capture_output=True, text=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")

if __name__ == "__main__":
    scripts = [
        'helper-scripts/converter.py',
        'helper-scripts/downsample_commaai_data.py',
        'helper-scripts/csvSeperator.py',
        'helper-scripts/plotWithManualAnnotation.py'
    ]

    for script in scripts:
        run_script(script)