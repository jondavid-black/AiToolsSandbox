import psutil
import GPUtil
from datetime import datetime
import time
import csv
import subprocess

time_fmt = "%Y-%m-%d %H:%M:%S"

def find_process(process_name):
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


# run the LLM server
llm_process = subprocess.Popen(['python3', '-m llama_cpp.server --model ~/documents/ai/mistral-7b-instruct-v0.2.Q5_K_S.gguf'])

# Open the CSV file in write mode
with open('usage.csv', 'w', newline='') as f:
    # Create a CSV writer
    writer = csv.writer(f)

    # Write the headers
    writer.writerow(['time', 'cpu_usage', 'memory_usage', 'gpu_usage', 'gpu_memory_usage'])

    # get the gpu for performance monitoring
    gpus = GPUtil.getGPUs()
    gpu = gpus[0]

    # Launch the qa_bot.py script
    process = subprocess.Popen(['python3', './qa_bot.py'])

    # Loop for a certain duration (e.g., 60 seconds)
    while process.poll() is None:
        # Get CPU and memory usage
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        # Write to the CSV file
        writer.writerow([datetime.now().strftime(time_fmt), cpu_usage, memory_usage, gpu.load, gpu.memoryUtil])

        # Flush the file write buffer
        f.flush()

        # Wait for 5 seconds
        time.sleep(5)

llm_process.kill()