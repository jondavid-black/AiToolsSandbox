# Code Assistant (Cody)

This is a little outside the current scope, but I discovred this and didn't want to lose it.

One of our use cases id to provide a developer assistant.  Ideally, we'd fine something along the lines of GitHub Copilot but it's not likely we'll achieve that level of performance using local open tooling.  However, there are some interesting tools that can help.  Previously we discovered Continue, a VS Code extension that enables use of a local LLM.  Here we'll look at [coLLaMA](https://github.com/iohub/coLLaMA), another VS Code extension that may provide an alternative in that space.

## The Plan

While I'd like to prove this in a completely network disconnected way, I don't see a good way to do that.  I also don't want to muck up my local VS Code configuration (which has GitHub Copilot).  I believe I'll the following:

- Create an AWS EC2 server to run the LLM
  - Download a code-oriented LLM model GGUF from HuggingFace
  - Install python-llama-cpp
  - Serve the model using the python-llama-cpp server
- Create a new Ubuntu VM using VirtualBox
  - Install VS Code on the VM
  - Install the coLLaMA extension
  - Configure the coLLaMA extension to use my EC2 python-llama-cpp LLM server

Running the EC2 server may cost me a few dollars, but shouldn't be too bad.  Once I run a few tests, I'll write up my results and destroy everything.

## Setup

The first thing I did was setup an AWS EC2 server.  I used a c5a.8xlarge instance running Ubuntu 20.04.  I then connected using VSCode's Remote SSH extension.  

First we setup the server:
- Installed anaconda: Follow [published instructions](https://docs.anaconda.com/free/anaconda/install/linux/)
- Install CPP compiler:  ```sudo apt update```, ```sudo apt install build-essential```
- Create conda environment:  ```conda create -n llamacpp python=3.11.7```, ```conda activate llamacpp```
- Install llama-cpp-python:
  - ```pip install llama-cpp-python```
  - ```pip install llama-cpp-python[server]```
- Download LLM model: ```wget https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf```
- Run the LLM server: ```python3 -m llama_cpp.server --model ./mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf```

Now we setup the client:
- We're already remoted in via VS Code's remote SSH extension.  This means we're running a "fresh" VS Code server install on the EC2 server without all the extensions we have installed locally.
- Install the coLLaMA extension by searching "collama" in the extensions panel and clicking install.
This adds a little robot icon to the left panel and opens the "Cody: Chat" window.
- Open the Extension Settings and set the Server Endpoint to ```http://localhost:8080```

## Failure

This is where we should be up and running, but instead every time I try to use the chat I get an error message:

```
Request failed: {"detail":"Not Found"}
```

After doing a little digging I can see that the coLLaMA extension is trying to connect to the server using ```http://127.0.0.1/vi/completion``` but the server URL is ```http://127.0.0.1/v1/completions```.  Notice that extra s at the end of the url?  I checked the collama code base and found this is a [hard coded endpoint in the client code](https://github.com/iohub/collama/blob/main/vscode/src/completions/client.ts).

It appears that the API changed in the past and ```collama``` is expecting the old API.  [I'm not the only person who has encountered this](https://stackoverflow.com/questions/77435356/openai-api-new-version-v1-of-the-openai-python-package-appears-to-contain-bre).  I checked the ```collama``` repo and saw that the client code was last updated 2 weeks ago (today is 1/21/24), so I'm a little stumped.  I don't really know anything about the OpenAI API release history, but it's probably worth investigating.

## Resolution Attempt

In an attempt to overcome this issue I'm going to build and run [llama.cpp](https://github.com/ggerganov/llama.cpp) directly rather than use the python binding.  I just followed the build instructions in the readme using ```make``` to perfrom the build.

I the ran the llama.cpp server:
'''bash
./server -m models/7B/ggml-model.gguf -c 2048
```

I updated the collama extenstion settings to use the new server endpoint ```http://localhost:8080``` using the default server port and tested the chat again.

> tell me a joke
>> Sure, here's a joke for you:
>>  Why couldn't the bicycle stand up by itself?
>>  Because it was two-tired!

Success!!!

I then tried a coding example:

> I'd like your help developing a python application.  I'd like to make thegame snake.  Can you help me?
>
>> Certainly! I'd be happy to help you develop a snake game in Python. Here are the basic steps we can follow:
>> 
>> 1. Set up the game window using a library like Pygame or Turtle.
>> 2. Create the snake object, which will be represented as a list of rectangles.
>> 3. Implement user input so that the snake moves in the desired direction.
>> 4. Add a function to generate food for the snake to eat.
>> 5. Increase the snake's length and score each time it eats food.
>> 6. Check for collisions between the snake and the game window boundaries or itself.
>> 7. Display the score on the game screen.
>> 8. Implement game over conditions when the snake collides with itself or the boundary.
>> 9. Allow the user to restart the game after it ends.
>> 
>> Do you have any specific requirements for your snake game? Let me know and I can help you customize it accordingly.
>
> I'd like to use a, s, d, w keys to control the snake.  Otherwise your recommendation is great. Will you write the prototype code for me?
>
>> Sure, I'd be happy to help you write the prototype code for your snake game using Pygame and the a, s, d, w keys for control. Here is an initial version of the code:

```python
import sys
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
SIZE = 20
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Create a font object for displaying score
font = pygame.font.SysFont(None, 30)

# Create the snake list and starting position
snake_list = [(WIDTH // 2, HEIGHT // 2)]
direction = (0, -SIZE)

# Create food
food_position = None
generate_food()

# Set up the clock
clock = pygame.time.Clock()

def generate_food():
    global food_position
```

Overall performance isn't too bad.  It took a few seconds for the AI to respond, but the response started streaming cleanly and was engaging to watch.  Obviously, the response was cut off.  I suspect this is because of the max Tokens parameter in the collama extension.  I changed the default value of 300 to 2048 and tried again.

> Will you repeat the prototype code you wrote for me?

```python
import sys
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
SIZE = 20
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Create a font object for displaying score
font = pygame.font.SysFont(None, 30)

# Create the snake list and starting position
snake_list = [(WIDTH // 2, HEIGHT // 2)]
direction = (0, -SIZE)

# Create food
food_position = None
generate_food()

# Set up the clock
clock = pygame.time.Clock()

def generate_food():
    global food_position
   
    while True:
        x = random.randrange(0, WIDTH, SIZE)
        y = random.randrange(0, HEIGHT, SIZE)
        if (
```

Well...we got a little further, but not much.  I was impressed that is actually gave me the same response as before.  I cut and pasted the code into a file called ```snake.py``` and prompted the AI: 'Continue generating code'.  After a few seconds (maybe 15-30 sec) it started streaming the response:

```python
        if (x, y) not in snake_list:
            food_position = (x, y)
            break

def draw_objects():
    screen.fill(BACKGROUND_COLOR)
    for segment in snake_list:
        pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(segment[0], segment[1], SIZE, SIZE))
    if food_position is not None:
        pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food_position[0], food_position[1], SIZE, SIZE))
    score_text = font.render('Score: {}'.format(len(snake_list) - 1), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, SIZE):
                direction = (0, -SIZE)
```

OK...so maybe we're on to something?  Let's keep going.  This time I pulled up ```top``` in a separate terminal. The server process was using ~1600% CPU and ~50% MEM.  Again, after a few seconds it returned:

```python
        elif event.key == pygame.K_DOWN and direction != (0, -SIZE):
            direction = (0, SIZE)

        elif event.key == pygame.K_LEFT and direction != (SIZE, 0):
            direction = (-SIZE, 0)

        elif event.key == pygame.K_RIGHT and direction != (-SIZE, 0):
            direction = (SIZE, 0)
```
>> def move_snake(): head = snake_list[0] new_head = (head[0] + direction[0], head[1] + direction[1]) if new_head in snake_list or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT): return False snake_list.insert(0, new_head) if new_head == food_position: generate_food() else: snake_list.pop() return True
>> 
>> def main(): while True: draw_objects() handle_input() if not move_snake(): break pygame.display.flip() clock.tick(10)
>>
>>  if name == 'main':

No, that's not an error in the markdown, it gave me a partial code block and a partial text response containing code.

Regardless, let's see if it will finish the code for me.

>> main()

```python
This should give you a basic prototype of the snake game that can be controlled with the a, s, d, w keys. The snake will grow in length each time it eats food, and the game will end if the snake collides with itself or the boundaries of the game window.
```

Once again, the formatting in the response was botched.  It provided the code as text and the text as a code block.  Strange.

I did notice that at the bottom on the chat window it is showing the ```snake.py``` as if it's using that for context.

I manually corrected formatting issues to see if the code itself had any errors.  There were 2 warnings:  the initial call to ```generate_food()``` and the ```if name == 'main':``` line near the bottom.  I moved ```generate_food()``` into the first line of ```main()```.  I changed the if statement to ```if __name__ == '__main__':```.  

I can now see the ```pygame``` is being used but isn't installed on the system.  Rather than just installing it, I asked the AI to generate a ```requirements.txt``` file for me.  This time, it just spun forever so I cancelled the prompt.  I went ahead and created / opened the ```requirements.txt``` file and asked the AI "what do I need to put in my requirements file for the snake game to work properly?"  Once again...it just spun forever.  Finally, I restarted the server and tried again.  This time it took a minute or two (actually 124.261 sec based on the console) to responsd and gave me:

> Instruction:
> what do I need to put in my requirements file for the snake game to work properly?
> 
> Response:
> To create a requirements.txt file for the snake game, you will need to list all of the required Python packages and their corresponding versions that are used in your project. In this case, we have only used Pygame, so the contents of the requirements.txt file would be:

```
pygame==2.1.2
```

> You can generate this file by running the following command in your terminal or command prompt:

```
pip freeze > requirements.txt
```

> This will create a requirements.txt file with all of the installed packages and their versions listed. You can then use this file to install the same dependencies on another machine or environment by running:

```
pip install -r requirements.txt
```


So I created a new conda environment and followed the instructions (omitting the freeze command).  

```bash
conda create -n snake python=3.11.7
conda activate snake
pip install -r requirements.txt
```

This failed because the version of pygame provided doesn't exist.  I removed the version and was successful running pip.  I then ran the code and...it failed again.

```bash
(snake) ubuntu@ip-172-31-24-208:~/ai/test$ python ./snake.py 
pygame 2.5.2 (SDL 2.28.2, Python 3.11.7)
Hello from the pygame community. https://www.pygame.org/contribute.html
ALSA lib confmisc.c:855:(parse_card) cannot find card '0'
ALSA lib conf.c:5178:(_snd_config_evaluate) function snd_func_card_inum returned error: No such file or directory
ALSA lib confmisc.c:422:(snd_func_concat) error evaluating strings
ALSA lib conf.c:5178:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
ALSA lib confmisc.c:1334:(snd_func_refer) error evaluating name
ALSA lib conf.c:5178:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
ALSA lib conf.c:5701:(snd_config_expand) Evaluate error: No such file or directory
ALSA lib pcm.c:2664:(snd_pcm_open_noupdate) Unknown PCM default
libEGL warning: MESA-LOADER: failed to open swrast: /usr/lib/dri/swrast_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri, suffix _dri)

libEGL warning: MESA-LOADER: failed to open swrast: /usr/lib/dri/swrast_dri.so: cannot open shared object file: No such file or directory (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri, suffix _dri)

/home/ubuntu/anaconda3/envs/snake/lib/python3.11/site-packages/pygame/sysfont.py:223: UserWarning: 'fc-list' is missing, system fonts cannot be loaded on your platform
  warnings.warn(
```

I think this may because I'm running remotely on an EC2 instance without any graphics capability.  I'm going to stop here, but I found this exercise informative.

## Observations

- Using a large EC2 instance (32 vCPU / 64GB MEM ) allowed me to run a much larger model than I could locally.  Overall the performance was pretty good...at least considering response times compared to my laptop.  That said, it is still a far cry from what I've seen with GitHub Copilot or other online AI tools.
- I genuinely wonder if a cloud server with GPU would have provided a substantially better experience.  I suspect it would have, but I'm not able to test it due to AWS quota limitations.
- We saw API deltas previously between tools like ```Ollama``` and ```llama-cpp-python```.  Now we're experiencing API differences again and need to understand them better.  Perhaps we may need to fork ```llama-cpp-python``` to create a proxy interface for the "old" API endpoints.
- ```collama``` looks good overall.  The chat window is pretty nice, but get's confused in response formatting.  I never saw ```collama``` attempt to perform code completion.  Looking over the extension settings I see Autocomplete is Enabled, but there's also a lot of items marked as "Experimental".  This leaves me questioning the maturity of ```collama```.