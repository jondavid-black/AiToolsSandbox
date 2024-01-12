import psutil
from datetime import datetime
import time
import csv
import subprocess

time_fmt = "%Y-%m-%d %H:%M:%S"

# Launch the LLM test main.py script
process = subprocess.Popen(['python3', './main.py'])

# Open the CSV file in write mode
with open('usage.csv', 'w', newline='') as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the headers
    writer.writerow(['time', 'cpu_usage', 'memory_usage'])

    # Loop for a certain duration (e.g., 60 seconds)
    while process.poll() is None:
        # Get CPU and memory usage
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        # Write to the CSV file
        writer.writerow([datetime.now().strftime(time_fmt), cpu_usage, memory_usage])

        # Flush the file write buffer
        f.flush()

        # Wait for 5 seconds
        time.sleep(5)