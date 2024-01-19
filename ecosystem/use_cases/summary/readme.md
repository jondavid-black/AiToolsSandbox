# AI Summarizer

In this use case we'll attempt to take a url from the user and use AI to provide a summary of the content.  We'll provide a web UI for the user to interact with.  We'll also use a local LLM running in python-llama-cpp and LangChain to provide the summarization API.

## Setup

- Copy the basic_q_a_bot relevant files as a starting point.
- Reorder the UI to place the text box at the top and add a "summarize" button.
- Configure LangChain to use the local LLM.
- Change the chat function to use LangChain to generate a summary.
- Reconfigure the main script to launch the llama_ccp.server instead of Ollama.

Althought I did update ```main.py``` to run python-llama-cpp instead of Ollama, I ended up just running the sum_bot. To run the sum_bot application:

```bash
python3 -m llama_cpp.server --model ./mistral-7b-instruct-v0.2.Q5_K_S.gguf
```

```bash
python3 ./sum_bot.py
```

And then open a browser to http://localhost:7860

I just entered URLs that I own for testing purposes.  The results are in ```summary_log.md```.

## Observations

- I tried to summarize the CrewAI readme from the raw feed on GitHub and hit the token limit for the model.  I wonder if it can be increased?
  - openai.BadRequestError: Error code: 400 - {'error': {'message': "This model's maximum context length is 2048 tokens, however you requested 3090 tokens (2834 in your prompt; 256 for the completion). Please reduce your prompt; or completion length.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}
- I played around with different layouts in Gradio.  It wasn't too hard to do, but also seemed a bit limited.  It's probably worth more exploration.
- I did drop in avatars for the first time...and it was fun.  :)