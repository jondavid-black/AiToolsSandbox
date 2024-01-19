# Chat with Docs 2

This is a clone of the ```Chat With Docs``` use case, swapping LlamaIndex for LangChain.  Based on a quick review of the LlamaIndex, it appears to provide a cleaner API for RAG capability.  Although it appears that LlamaIndex is capable or running LLMs itself, we'll stick with Ollama for consistency.  I'll use an [Ollama Example](https://medium.com/poatek/building-open-source-llm-based-chatbots-using-llama-index-e6de9999ee76) from Medium as a starting point.

## Technology
Although this is a bit repetitive from other use cases, we are adding a new item so I'll include everything for completeness and update as needed.

- Ollama:  A LLM execution tool for linux.
- Mistral 7B:  A LLM model trained on the Mistral 7B dataset and run through Ollama.
- Gradio: A python-based web ui framework tailored for AI applications.
- LlamaIndex: A python-based library that provides a simple API for interacting with LLMs.

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

### LlamaIndex

TODO Add LlamaIndex information.

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

- The first time I ran this, it downloaded stuff from the internet.  I'm not sure what it was, but it was a little concerning when conidering an offline production environment.

```bash
(chat_with_docs_2) jdblack@jd-omen ~/documents/repos/AiToolsSandbox/ecosystem/use_cases/chat_with_docs_2 (main)$ python3 ./main.py
2024/01/18 13:40:49 images.go:808: total blobs: 24
2024/01/18 13:40:49 images.go:815: total unused blobs removed: 0
2024/01/18 13:40:49 routes.go:930: Listening on 127.0.0.1:11434 (version 0.1.20)
2024/01/18 13:40:52 shim_ext_server.go:142: Dynamic LLM variants [cuda rocm]
2024/01/18 13:40:52 gpu.go:88: Detecting GPU type
2024/01/18 13:40:52 gpu.go:203: Searching for GPU management library libnvidia-ml.so
2024/01/18 13:40:52 gpu.go:248: Discovered GPU libraries: [/usr/lib/wsl/lib/libnvidia-ml.so.1]
2024/01/18 13:40:52 gpu.go:94: Nvidia GPU detected
2024/01/18 13:40:52 gpu.go:135: CUDA Compute Capability detected: 7.5
config.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 743/743 [00:00<00:00, 5.62MB/s]
model.safetensors: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 133M/133M [00:22<00:00, 5.98MB/s]
tokenizer_config.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 366/366 [00:00<00:00, 4.26MB/s]
vocab.txt: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 232k/232k [00:00<00:00, 520kB/s]
tokenizer.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 711k/711k [00:00<00:00, 1.97MB/s]
special_tokens_map.json: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 125/125 [00:00<00:00, 1.48MB/s]
Running on local URL:  http://127.0.0.1:7862

To create a public link, set `share=True` in `launch()`.
```

- Loading the PDF files takes a while (i.e. 378 sec) and doesn't seem to persist between runs.  It also hammers the GPU. I added a simple print statement to tell me precisely how long the loading portion of the code takes.
  - In an attempt to overcome this I'm adding a chroma db vector store using the [instructions provided](https://docs.llamaindex.ai/en/stable/understanding/storing/storing.html).  This in turn failed because it requires sqlite3 >= 3.35.0 which does not seem to be available in WSL via ```apt install```, even after running ```apt update``` and ```apt upgrade```.  After reviewing the [link provided in the console](https://docs.trychroma.com/troubleshooting#sqlite), I've added ```pysqlite3-binary``` to the ```requirements.txt``` file.
  - Making this work ended up being super goofy.  First, I had to manually install the latest version of sqlite3 from source.  The I had to find and update the ```__init__.py``` file in the ```chromadb``` directory under my python install's ```site-pacakges``` directory.  I cut and paste the following code to the top of the file:
  ```python
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
  ```
  - After all of that, it didn't improve performance.  Technically it's my fault.  The code is going to load the docs no matter what.  It appears possible to load the DB up front and then see if individual docs are present before loading them, but I didn't try to go that far...and it wasn't really clear how to do that.
- Initially, the slow response of Ollama on my laptop resulted in a timeout error.  I increased the llm request_timeout to 300 seconds to compensate.
- Running the actual query doesn't use my GPU as we saw with the LangChain example.
- I tried to kill the application using CTRL-C while it was loading the PDFs, but it didn't work immediately.  When it finally stopped, it put the system in a strange state.  Initially I tried to kill and restart WSL, but WSL would not restart.  I then had to reboot my machine to recover...which worked.
- Initial conclusion is that llama-index has promise, but feels less mature than LangChain.  The documentation looks really good at first glance, but the deeper you get the less useful / complete it becomes.  If you're working in their pre-defined expectations it seems ok, but doing anything different (i.e. wanting history in a Q&A session over some docs) doesn't seem to work.
- This setup creates a ```chroma_db``` folder that is large (163.11 MB).  When I tried to commit it to GitHub it failed due to exceeding max file size limite.  I just deleted it manually.  In the future we'll need to setup vector stores in a way that doesn't put things into the repo(s).
