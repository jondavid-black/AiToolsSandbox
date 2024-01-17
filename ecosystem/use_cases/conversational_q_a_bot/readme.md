# Dumb Q&A AI Bot

An enhancement to the miminum viable product for a chatbot to answer questions and remember the user conversation. This bot can answer questions and include previous details of the conversation in the user interaction. It is still not very smart, but at least supports refinement based on user feedback.  It provides a minimal web ui for asking questions and getting answers.

## Technology

- Ollama:  A LLM execution tool for linux.
- Mistral 7B:  A LLM model trained on the Mistral 7B dataset.
- Gradio: A python-based web ui framework tailored for AI applications.

## Approach

We can basically take the work from last week and just reuse it, but I'd like to enhance the data collection a bit.
- Reuse the /ollama/webui code from last week.
- Add the system monitoring from /ollama/auto_run.
- Add a top level script to launch and run everything from a single command.
- Add logging to capture prompts, responses, and response times that outputs in markdown for easier reuse in document creation and sharing.

## Implementation

1. Begin monitoring system utilization
1. If not already running, launch ```ollama serve``` process
1. Launch gradio web ui (add basic chat_hostory)

## Usage

1. Open web ui in a browser
1. Manually provide some prompts and see what's returned.
1. Request a few options for some topic
1. Request more detail on a returned option without naming it (i.e. option 2, or the last option)

## End

1. Close the browser
1. Terminate the CLI command (ctrl+c)
1. Review log to ensure data was captured