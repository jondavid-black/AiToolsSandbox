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

I did test history and it worked, but now we've got a token size problem to fix.  At least the error message was clear.  Can we adjust something in lamma_cpp.server or our client setup to increase token size?
After a few prompts I got the following error in the qa_bot client:    
```bash
openai.BadRequestError: Error code: 400 - {'error': {'message': "This model's maximum context length is 2048 tokens. However, you requested 2078 tokens (2078 in the messages, None in the completion). Please reduce the length of the messages or completion.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}
```

But it appears to have originated in the LLM server:
```bash
Exception: Requested tokens (2078) exceed context window of 2048
Traceback (most recent call last):
  File "/home/jdblack/.local/lib/python3.11/site-packages/llama_cpp/server/errors.py", line 170, in custom_route_handler
    response = await original_route_handler(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jdblack/.local/lib/python3.11/site-packages/fastapi/routing.py", line 274, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jdblack/.local/lib/python3.11/site-packages/fastapi/routing.py", line 191, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jdblack/.local/lib/python3.11/site-packages/llama_cpp/server/app.py", line 368, in create_chat_completion
    first_response = await run_in_threadpool(next, iterator_or_completion)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jdblack/.local/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
    return await anyio.to_thread.run_sync(func, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jdblack/.local/lib/python3.11/site-packages/anyio/to_thread.py", line 33, in run_sync
    return await get_asynclib().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jdblack/.local/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 877, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/home/jdblack/.local/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 807, in run
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jdblack/.local/lib/python3.11/site-packages/llama_cpp/llama_chat_format.py", line 295, in _convert_text_completion_chunks_to_chat
    for i, chunk in enumerate(chunks):
  File "/home/jdblack/.local/lib/python3.11/site-packages/llama_cpp/llama.py", line 793, in _create_completion
    raise ValueError(
ValueError: Requested tokens (2078) exceed context window of 2048
INFO:     127.0.0.1:34140 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
```

