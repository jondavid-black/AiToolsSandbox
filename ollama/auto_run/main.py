from langchain.llms import Ollama
import json
import time
from datetime import datetime

time_fmt = "%Y-%m-%d %H:%M:%S"

# setup the logger
logs = []
start_time = time.time()
logs.append({"time": datetime.now().strftime(time_fmt), "message": "Starting the program."})

# setup the model list
models = ["mistral", "mixtral"]

# setup the prompts
prompts = {}

def add_prompt(category: str, difficulty: str, prompt: str):
    if category not in prompts:
        prompts[category] = {}
    if difficulty not in prompts[category]:
        prompts[category][difficulty] = []
    prompts[category][difficulty].append(prompt)

add_prompt("general", "easy", "What is the capital of the United States?")
add_prompt("general", "easy", "Briefly describe our solar system.")
add_prompt("general", "hard", "Write a 5 paragraph white paper on modern generative AI technologies for the CTO of a Fortune 500 software development company.  Include a summary of the current state of the art, a description of the most promising research directions, and a discussion of the ethical implications of the technology.  Provide metrics and potential return on investment for each of the research directions.")
add_prompt("code", "medium", "Provide a Python function that accepts numbers a, b, and c for and computes the formula $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$.")
add_prompt("code", "easy", "Provide a Python function that accepts a list of numbers and returns the sum of the list.")
add_prompt("code", "easy", "Provide a Python function that accepts a list of numbers and returns the average of the list.")
add_prompt("code", "easy", "Provide a Python function that accepts a list of numbers and returns the median of the list.")
add_prompt("code", "hard", "Write the game snake in Python.  The game should be playable in the terminal.  The user should control the snake using the arrow keys.  The snake should grow when it eats food.  The game should end when the snake hits the wall or itself.")
add_prompt("code", "medium", "Write a Python function that calculates the angle between two 3D vectors in degrees. Assume the observer is at [0, 0, 0].  Include at least 2 unit tests and the requirements.txt file.  Use type hints and good documentation.")
add_prompt("logic", "easy", "There are two cups on the table.  A ball is placed in the cup on the right.  The cups are turned upside down and shuffled.  What is the probability that the ball is in the cup on the right?")
add_prompt("logic", "medium", "John and Mark are in a room with a ball, a basket and a box. John puts the ball in the box, then leaves for work. While John is away, Mark puts the ball in the basket, and then leaves for school. They both come back together later in the day, and they do not know what happened in the room after each of them left the room. Where do they think the ball is?")
add_prompt("logic", "hard", "You are in a room with 3 switches.  One of the switches controls a light bulb in the next room.  You can only enter the next room once.  How do you determine which switch controls the light bulb?")
add_prompt("logic", "hard", "Consider a town where all residents are either truth-tellers (always tell the truth) or liars (always lie). You meet two residents, A and B. A says 'At least one of us is a liar.' What can you deduce about A and B? Are they truth-tellers or liars?")

# loop over the models
for model in models:
    # loop over the prompts
    for category in prompts:
        for difficulty in prompts[category]:
            for prompt in prompts[category][difficulty]:
                # run the model
                llm = Ollama(model=model)
                prompt_start = time.time()
                res = llm.predict(prompt)
                prompt_end = time.time()
                prompt_duration = prompt_end - prompt_start
                print (f"Model: {model}, Category: {category}, Difficulty: {difficulty}, Prompt: {prompt}, Answer: {res}")
                # add the result to the logs
                logs.append({"time": datetime.now().strftime(time_fmt), "model": model, "category": category, "difficulty": difficulty, "prompt": prompt, "answer": res, "duration": prompt_duration})

end_time = time.time()
duration = end_time - start_time
logs.append({"time": datetime.now() .strftime(time_fmt), "message": f"Finished the program in {duration} seconds."})

# Write the logs to a JSON file
with open('logs.json', 'w') as f:
    json.dump(logs, f)
