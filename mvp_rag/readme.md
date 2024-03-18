# AI Minimum Viable Product (MVP) with Basic Retrieval-Augmented Generation (RAG)

Based on the exploration performed in the original MVP, I'm going to expand that to include custom knowledge bases using RAG.  

## Components

1. Mistral 7B (for now): The Mistral 7B model performed very well in my testing and was something I could run on my laptop.  I'll reserve the right to upgrade to a more powerful model if needed.
1. Ollama (separate app):  I'm using the relatively new Ollama for Windows so that I can leverage GPU acceleration.
1. Gradio:  This provided a good UI out of the box and was easy to use.  I may explore other UI options in the future, but this is a good starting point.
1. LangChain:  
1. LlamaCppEmbeddings:  An embedding generator that transforms text chunks into vectors for similarity search in a vector store.
1. FAISS:  A simple / local vector store for my embeddings.

There will be 3 processes at play here:  load_rag which "reads" and embeds data, Ollama running the model, and the Gradio UI with Langchain to perform prompt/response with the user.  I'll be using OpenAI API (i.e. REST API) for interaction between the two processes.

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

I'm using Ollama for Windows which allows me to run Mistral outside the WSL environment and take advantage of GPU acceleration.

## Loading the Data

The data we're using here is documentation from the AaC project and the SysML v2 release project.

To load the data:

```bash
python3 ./load_rag.py
```

On my laptop this takes about 20 min to run.

## Running the UI

The UI is just an augmentation of the original MVP with a little LangChain put in place to load the vector store and integrate RAG behavior into the prompt / response.  One downside is I had to remove streaming.  It appears it is possible to do streaming with LangChain, but I didn't dig in deep enough to figure it out.

TO run the UI:

```bash
python3 ./mvp.py
```

## Observations
- I'm disappointed that streaming with LangChain isn't a clear / easy thing to implement.
- Runnign Ollama in Windows was a really nice update. It keeps things simple and overcomes some of the WSL "wierd-ness".
- Running the Embeddings for a large file took a lot longer than expected.
- Overall setting up the RAG wasn't too difficult.  Changing from the OpenAI streaming API to a chain was a little confusing.
- The RAG is definitely working, but it does result in some confusion in some respnoses the way it is currently setup.  Asking question that involves both data sets sometimes results in information "mix up" and incorrect responses.  It may be worth looking at agent constructs that can operate within a more isolated data space and then a user agent that aggregates information from the data-specific agents in a way that causes less confusion.

## Security

I [forked and ran the GitHub security scans on the Gradio](https://github.com/jondavid-black/gradio) baseline.  Here's all the findings:
![Gradio Code Security Scan](./img/gradio_security_scan.png)

- There are no security advisories published for Gradio.
- There are no Dependabot alerts.
- There are some code scanning findings:
    - All the `Critial` findings have to do with their GitHub Actions workflows and should not be relevant to the user.
    - The `High` findings relate to utility functions use of hashing and regex.  Initial review of the code doesn't raise any concerns here as these aren't actually used for security or privacy concerns.
    - The last `High` finding is about the potential for a "bad actor" to manipulate the `style` parameter for rendering.  Since this is somethign a developer would have to do as part of the API, I don't see a concern here.
    - The last `Medium` finding could present a challenge in the future.  It's pulling a javascript library from the web called `iframeResizer.contentWindow.min.js`.  It would be best to pull, scan, and pre-load this dependency in the future. 

I also [forked and ran the GitHub security scans on the llama-cpp-python](https://github.com/jondavid-black/llama-cpp-python) baseline.  Here's all the findings:
![Llama-cpp-python Code Security Scan](./img/llama-cpp-python-security-scan.png)

- There are no security advisories published for llama-cpp-pyton.
- There are no Dependabot alerts.
- All good!  No code scan security findings.

I ran a virus scan of the Mistral 7B instruct GGUF file.  It came back clean.
![Mistral 7B Instruct Virus Scan](./img/mistral_av_scan.png)

Finally, because I'm processing the RAG data in a separate process and storing it locally, I've got to load it in the UI.  The load process using what's called a "pickle" file which presents potential security issues if pulling from an untrusted source.  I override the security feature in the vector store load since I'm creating the data myself and trust it...but a better solution is needed in the future.
