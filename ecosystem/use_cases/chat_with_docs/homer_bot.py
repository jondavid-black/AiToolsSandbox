import requests, json
import time
from datetime import datetime
import gradio as gr
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import textwrap
# from lang_funcs import *
from langchain.llms import Ollama
from langchain import PromptTemplate

model = 'mistral'
context = [] 
time_fmt = "%Y-%m-%d %H:%M:%S"


def load_pdf_data(dir_path):
    loader = PyPDFDirectoryLoader(path=dir_path)
    
    # loading the PDF file(s)
    docs = loader.load()
    
    # returning the loaded document
    return docs

def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    
    # Initializing the RecursiveCharacterTextSplitter with
    # chunk_size and chunk_overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Splitting the documents into chunks
    chunks = text_splitter.split_documents(documents=documents)
    
    # returning the document chunks
    return chunks

def load_embedding_model(model_path, normalize_embedding=True):
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={'device':'cpu'}, # here we will run the model with CPU only
        encode_kwargs = {
            'normalize_embeddings': normalize_embedding # keep True to compute cosine similarity
        }
    )


# Function for creating embeddings using FAISS
def create_embeddings(chunks, embedding_model, storing_path="vectorstore"):
    # Creating the embeddings using FAISS
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    
    # Saving the model in current directory
    vectorstore.save_local(storing_path)
    
    # returning the vectorstore
    return vectorstore

# Creating the chain for Question Answering
def load_qa_chain(retriever, llm, prompt):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever, # here we are using the vectorstore as a retriever
        chain_type="stuff",
        return_source_documents=True, # including source documents in output
        chain_type_kwargs={'prompt': prompt} # customizing the prompt
    )

def get_response(query, chain):
    # Getting response from chain
    response = chain({'query': query})
    
    # Wrapping the text for better output in Jupyter Notebook
    wrapped_text = textwrap.fill(response['result'], width=100)
    return wrapped_text

#Call Ollama API
def generate(prompt, context):
    # r = requests.post('http://localhost:11434/api/generate',
    #                  json={
    #                      'model': model,
    #                      'prompt': prompt,
    #                      'context': context
    #                  },
    #                  stream=False)
    # r.raise_for_status()

    r = get_response(prompt, chain)

    # response = "" 

    return r, r 

    # for line in r.iter_lines():
    #     body = json.loads(line)
    #     response_part = body.get('response', '')
    #     print(response_part)
    #     if 'error' in body:
    #         raise Exception(body['error'])

    #     response += response_part

    #     if body.get('done', False):
    #         context = body.get('context', [])
    #         return response, context

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

#########################Ollams Setup#########################

prompt = """
### System:
You are an AI Assistant that follows instructions extreamly well. \
Help as much as you can.

### User:
{prompt}

### Response:

"""

template = """
### System:
You are an respectful and honest assistant. You have to answer the user's \
questions using only the context provided to you. If you don't know the answer, \
just say you don't know. Don't try to make up an answer.

### Context:
{context}

### User:
{question}

### Response:
"""

# Loading model from Ollama
llm = Ollama(model=model, temperature=0)

# Loading the Embedding Model
embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

# loading and splitting the documents
docs = load_pdf_data(dir_path="./files")
documents = split_docs(documents=docs)

# creating vectorstore
vectorstore = create_embeddings(documents, embed)

# converting vectorstore to a retriever
retriever = vectorstore.as_retriever()

# Creating the prompt from the template which we created before
prompt = PromptTemplate.from_template(template)

# Creating the chain
chain = load_qa_chain(retriever, llm, prompt)

#########################LangChain Read Docs##################
loader = PyPDFDirectoryLoader("./files")
loader.load()

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