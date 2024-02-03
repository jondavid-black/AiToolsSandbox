# Chat with Docs

In this use case we'll explore an AI assistant that can receive documents from a user and converse about the document content.  We'll test this using Homer's [Illiad](https://www.gutenberg.org/cache/epub/2199/pg2199-images.html) and [Odyssey](https://www.gutenberg.org/cache/epub/3160/pg3160-images.html) as our documents.
Both of these books are published under the [Creative Commons](https://creativecommons.org/) license by [Project Gutenberg](https://www.gutenberg.org/).

In the interest of KISS (Keep It Simple Stupid), we're going to skip setting up a fancy document loading UI and just load the documents at startup.  We'll also use LangChain to provide a better API for interacting with the underlying LLM rather using Ollama's REST API as we've done in other use cases (Basic Q&A, Conversational Q&A).  We'll continue to use Gradio to provide the simple web UI.

This was built using an example from [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2023/10/a-step-by-step-guide-to-pdf-chatbots-with-langchain-and-ollama/).  It seems a little more complex than necessary when compared with the [LangChain Python RAG Document Example](https://github.com/jmorganca/ollama/blob/main/examples/langchain-python-rag-document/main.py) in the Ollama repo.

## Technology
Although this is a bit repetitive from other use cases, we are adding a new item so I'll include everything for completeness and update as needed.

- Ollama:  A LLM execution tool for linux.
- Mistral 7B:  A LLM model trained on the Mistral 7B dataset and run through Ollama.
- Gradio: A python-based web ui framework tailored for AI applications.
- LangChain: A python-based library that provides a simple API for interacting with LLMs.

### Ollama
Ollama is a open source software tool that allows you to run LLMs on linux.  It is a command line tool that can be used to run LLMs from the command line or via a REST API.  Ollama provides commands to easily allow you to download and execute models from the Hugging Face model repository.  Under the covers Ollama is a golang applicaiotn that uses llama.cpp to execute the LLMs.  Ollama is available from the [Ollama Github Repository]() and is installed via the following command:
    ```bash
    curl https://ollama.ai/install.sh | sh
    ```

### Mistral 7B
Mistral 7B is a LLM model trained on the Mistral 7B dataset published under the Apache 2 Open-Source license.  It is available from the [Hugging Face Model Repository](https://huggingface.co/).  The model is downloaded and installed using the following command:
    ```bash
    ollama pull mistral
    ```
This command will download the model and install it in the ```~/.ollama/models``` directory.  The model is then ready to be used by Ollama.  Practically speaking the Mistral 7B model is a GGUF file.  GGUF, previously GGML, is a quantization method that allows users to use the CPU to run an LLM but also offload some of its layers to the GPU for a speed up. Although using the CPU is generally slower than using a GPU for inference, it is an incredible format for those running models on CPU or Apple devices.  Ollama pulls the encoded data from the Mistral 7B GGUF file to establish the tensors and weights for the model.  The model is then ready to be used by Ollama.

In this specific instance, based on past observation, we established a custom model using a ```Modelfile``` to set the temperature parameter and system prompt for model execution.  We've tweaked the system prompt to indicate that the AI assistant is an expert on Homer's works.
```
FROM mistral
PARAMETER temperature 0.2
SYSTEM """
You are an advanced AI assistant using the Mistral 7B model. You are capable of understanding and generating responses for a wide range of topics, but you specialize in the works of the classical Greek author Homer. Your goal is to provide accurate, helpful, and contextually appropriate responses to user queries about Homer's most famous works. You maintain a neutral and professional tone in your interactions.
"""
```

We'll use the ollama CLI to create the local model using the following command:
```bash
ollama create homer -f ./Modelfile
```

### Gradio
[Gradio](https://www.gradio.app/docs/chatbot) is a python-based web ui framework tailored for AI applications.  It provides a simple way to create a web ui for an AI application.  In this instance we just use it to provide a chatbot window and a user prompt text box.  Gradio communicates with Ollama via a REST API.  The Gradio app is a simple python script that launches the web ui and provides a REST API endpoint for the web ui to communicate with Ollama.  The Gradio app is launched using the following command:

```bash
python3 ./homer_bot.py
```

Gradio provides a degree of simplicity which is nice, but is (IMHO) a little confusing to work with.  The APIs aren't completely clear.  Simple things like clearing the user prompt text box after a response is returned is not obvious.  The documentation is a little sparse and the examples are a little too simple.  It's a useful tool, but it may require some learning / practice before it truely feels easy to use.

### LangChain

[LangChain](https://python.langchain.com/docs/get_started/introduction) is a python-based library that provides a "simple" API for interacting with LLMs.  It is available from the [LangChain Github Repository](https://github.com/langchain-ai/langchain).  Here's LangChain's description of itself:

> LangChain is a framework for developing applications powered by language models. It enables applications that:
> - Are context-aware: connect a language model to sources of context (prompt instructions, few shot examples, content to ground its response in, etc.)
> - Reason: rely on a language model to reason (about how to answer based on provided context, what actions to take, etc.)
>
> This framework consists of several parts. 
> - LangChain Libraries: The Python and JavaScript libraries. Contains interfaces and integrations for a myriad of components, a basic run time for combining these components into chains and agents, and off-the-shelf implementations of chains and agents.
> - [LangChain Templates](https://github.com/langchain-ai/langchain/blob/master/templates): A collection of easily deployable reference architectures for a wide variety of tasks.
> - [LangServe](https://github.com/langchain-ai/langserve): A library for deploying LangChain chains as a REST API.
> - [LangSmith](https://smith.langchain.com/): A developer platform that lets you debug, test, evaluate, and monitor chains built on any LLM framework and seamlessly integrates with LangChain.
>
> The LangChain libraries themselves are made up of several different packages. 
> - [langchain-core](https://github.com/langchain-ai/langchain/blob/master/libs/core): Base abstractions and LangChain Expression Language.
> - [langchain-community](https://github.com/langchain-ai/langchain/blob/master/libs/community): Third party integrations.
> - [langchain](https://github.com/langchain-ai/langchain/blob/master/libs/langchain): Chains, agents, and retrieval strategies that make up an application's cognitive architecture.

## Testing

Since we're using Homer's work as our documents, I searched the internet for quizes on the topic.  Testing was done manually with results interpreted for correctness based on the below information.

- Who is Zeus' son, killed by the Greeks?
    - Sarpedon
- Whos is the son of one of the seven at Thebes?
    - Diomedes
- In Chryses' prayer to Apollo, he calls him 'lord in strength' over which place?
    - Tenedos
- Who is the son of Asklepios?
    - Machaon
- Why did Patroclus leave his homeland as a youth and come to live with Achilles?
    - He killed another boy by accident.
- Whose horse spoke?
    - Achilleus
- What event ends the Iliad?
    - The funeral of Hektor.
- Who is promoted as a role model for Telemachos?
    - Orestes
- What is the name of Alkinoos' bard?
    - Demodokos
- Who was Eurymachos' sweetheart?
    - Melantho
- What is the name of Oedipus' mother, whom Odysseus sees in Hades?
    - Epikaste
- What were Nausicaa and her women doing when Odysseus appeared?
    - playing ball
- Who is spared in the slaughter of the suitors?
    - Medon
- What is the name of Manelaus' son by a slave woman, who's marriage is being celebrated when Telemachos arrives?
    - Magapenthes

## Observations

- Choosing test data (i.e. The Iliad and The Odyssey) that you aren't deeply familiar with makes it difficult to determine if the responses are correct.
- It's not completely clear to me if the underlying LLM has knowledge of Homer's Iliad and Odyssey or if it's just using the text as a corpus.  I suspect it's just using the text as a corpus, but I'd like to confirm this.
- The model requires precision in the prompts.  Things like differences in spelling (Hektor vs Hector) have a big impact on the response.
- This implementation has broken conversation history.  The model doesn't remember the previous conversation.  This is a little disappointing, but understandable given the limited implementation.
- Overvall run-time performance is good.  The model is responsive and the responses are returned quickly.  This seems to be generally faster than other use cases.  Give the volume of data in the documents, this is a little surprising.

If I find some time, I'd like to come back to this use case and rework it a bit.  I think the Ollama example may be a better starting point.  I'd like to see what it would take to add a UI component that allows the user to upload a document and then have the AI assistant read the document and then be able to converse about the document.  I think this would be a more interesting use case and would be a better demonstration of the capabilities of the LLM.  I'd also like to try and find some document content that I'm more familiar with so I can better evaluate the responses.

## After-Thought
While I was testing some other configurations that don't use a RAG data set, I asked the model about Homer's Iliad and Odyssey.  It turns out the base model already knows these tests.  This really needs to be tested again with some unique (i.e. created) content to evaluate whether or not it is working properly.