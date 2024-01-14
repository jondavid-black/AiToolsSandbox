import json
import argparse

def format_logs(logs_file):
    # Read the logs
    with open(logs_file, 'r') as f:
        logs = json.load(f)

    # Output the logs
    for log in logs:
        # Check if the log entry is an LLM execution entry
        if all(key in log for key in ['time', 'model', 'category', 'difficulty', 'prompt', 'answer', 'duration']):

            chat_stream = ""

            # Add the entry to the chat stream
            chat_stream += f"---{log['model']}---\n"
            chat_stream += f"Time: {log['time']}\n"
            chat_stream += f"Prompt: {log['prompt']}\n"
            chat_stream += f"Response: {log['answer']}\n"
            chat_stream += f"Duration: {log['duration']}\n"
            chat_stream += "---------------------\n\n"

            # Wait for the user to hit a key to continue
            input("Hit a key to continue...")
            print(chat_stream)

    return chat_stream

# Parse command line arguments
parser = argparse.ArgumentParser(description='Format logs.')
parser.add_argument('logs_file', type=str, help='The logs file to format.')
args = parser.parse_args()

# Use the function
format_logs(args.logs_file)
