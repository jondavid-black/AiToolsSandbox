import time
from datetime import datetime
import gradio as gr
from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    set_global_service_context,
)
from llama_index.llms import Ollama
import chromadb
from llama_index.vector_stores import ChromaVectorStore

model = 'mistral'
context = [] 
time_fmt = "%Y-%m-%d %H:%M:%S"

#Call Ollama API
def generate(prompt, context):
    
    r = query_engine.query(prompt).response

    return r, r 

def append_to_log(prompt, response, duration):
    with open('assistant_log.md', 'a') as f:
        log_prompt = "NO PROMPT"
        if prompt:
            log_prompt = "> " + prompt.replace('\n', '\n> ')
        log_response = "NO RESPONSE"
        if response:
            log_response = ">> " + response.replace('\n', '\n>> ')
        minutes, seconds = divmod(duration, 60)
        f.write(f"# Log Entry {datetime.now().strftime(time_fmt)} - Duration {minutes}m {seconds:.2f}s\n\n{log_prompt}\n{log_response}\n\n")
        f.flush()


def chat(input, chat_history):

    chat_history = chat_history or []

    global context
    prompt_start = time.time()
    output, context = generate(input, context)
    prompt_end = time.time()
    
    append_to_log(input, output, prompt_end - prompt_start)
    chat_history.append((input, output))

    return chat_history, chat_history, ""
  #the first history in return history, history is meant to update the 
  #chatbot widget, and the second history is meant to update the state 
  #(which is used to maintain conversation history across interactions)
  #and the thrid return clears the input box

#########################Ollama and Document Setup#########################

load_start = time.time()
llm = Ollama(model=model, temperature=0.2, request_timeout=300.0)

# Reads pdfs at "./" path
documents = (
    SimpleDirectoryReader(
        input_dir = './files',
        required_exts = [".pdf"])
        .load_data()
)


# ServiceContext is a bundle of commonly used 
# resources used during the indexing and 
# querying stage 
service_context = (
    ServiceContext
    .from_defaults(
        llm=llm, 
        embed_model="local:BAAI/bge-small-en-v1.5", 
        chunk_size=300
    )
)
set_global_service_context(service_context)

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")

# create collection
chroma_collection = db.get_or_create_collection("homer")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create the vectorstore index
index = (
    VectorStoreIndex
    .from_documents(
        documents, 
        storage_context=storage_context, 
        llm=llm
        )
)
query_engine = index.as_query_engine(streaming=False)

load_end = time.time()
print(f"Loaded {len(documents)} documents in {load_end - load_start:.2f}s")

#########################Gradio Code##########################
block = gr.Blocks()

with block:

    gr.Markdown("""<h1><center> HomerBot - An Expert in Classical Literature </center></h1>
    """)

    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Type here")

    state = gr.State()

    message.submit(chat, inputs=[message, state], outputs=[chatbot, state, message])


block.launch(debug=True)