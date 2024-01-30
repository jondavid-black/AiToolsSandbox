# AI Minimum Viable Product (MVP)

Based on the exploration performed in the ecosystem, I'm going to build a MVP that will be used to assert the feasibility of a stand-alone / private LLM chat capability.  

## Components

1. Mistral 7B (for now): The Mistral 7B model performed very well in my testing and was something I could run on my laptop.  I'll reserve the right to upgrade to a more powerful model if needed.
1. Llama.cpp (python):  This runtime gave me really good performance in comparison to Ollama along with an OpenAI compatible API.  I probably won't go for the GPU acceleration here, but may explore that in the future.
1. Gradio:  This provided a good UI out of the box and was easy to use.  I may explore other UI options in the future, but this is a good starting point.

There will be 2 processes at play here:  llama.cpp running the model and the Gradio UI.  I'll be using OpenAI API (i.e. REST API) for interaction between the two processes.

## Setup

First things first, let's create our conda virtual environment before we do anything.

```bash
conda create --name mvp
conda activate mvp
```

Now we just need to install the requirements.

```bash
pip install -r requirements.txt
```

## Running the Model

I did this as I had done for previous examples.  Simply download the GGUF file you want to run and then run the server.

```bash
python3 -m llama_cpp.server --model ./mistral-7b-instruct-v0.2.Q5_K_S.gguf
```

## Running the UI

This is where things got difficult.  Llama_cpp_server supports the new OpenAI v1.0 API, but most of the examples on the web are for the older API.  I ended up finding [documentation on the OpenAI](https://platform.openai.com/docs/api-reference/streaming#chat/create-stream) website that worked for me.  I specifically wanted to try streaming to improve the user experience, and that was tough to figure out for the first time.  I didn't do anything fancy with Gradio, just used the built-in defaults.  Overall it works, but the model's stream response rambles on-and-on sometimes.  I'll have to figure out how to improve that in the future.

```bash
python3 ./qa_bot.py
```

## TODO

I still need to get logging added, as well as some metric collection.

After a few prompts I got the following error:    
```bash
openai.BadRequestError: Error code: 400 - {'error': {'message': "This model's maximum context length is 2048 tokens. However, you requested 2078 tokens (2078 in the messages, None in the completion). Please reduce the length of the messages or completion.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}
```

I did test history and it worked, but now we've got a token size problem to fix.  At least the error message was clear.  Can we adjust something in lamma_cpp.server or our client setup to increase token size?