import os
from datetime import datetime
import time
from openai import OpenAI
import gradio as gr
from mvp_interface import MvpInterface
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.retrievers import MergerRetriever

# openai.api_key = "Not-a-real-key"  # Replace with your key
# openai.base_url = "http://127.0.0.1:8000/v1/"

client = OpenAI(base_url="http://127.0.0.1:11434/v1/", api_key="Not-a-real-key")

system_prompt = "You are a helpful AI engineering assistant.  You must always provide correct, complete, and concise responses to the user's requests.  Once you've answered the user's request, end your feedback."

time_fmt = "%Y-%m-%d %H:%M:%S"

users = {
    "Jack": "password",
    "Jill": "password"
}

retriever = None

def auth_user(username, password):
    if username in users and password == users[username]:
        print(f"Successful login for user {username}")
        return True
    else:
        print(f"Failed login for user {username}")
        return False

def append_to_log(prompt, response, duration, user):
    with open('assistant_log.md', 'a') as f:
        log_prompt = "> " + prompt.replace('\n', '\n> ')
        log_response = ">> " + response.replace('\n', '\n>> ')
        minutes, seconds = divmod(duration, 60)
        f.write(f"# Log Entry {datetime.now().strftime(time_fmt)} - User {user} - Duration {minutes}m {seconds:.2f}s\n\n{log_prompt}\n{log_response}\n\n")
        f.flush()

def initialize_rag():
    rag_init_start = time.time()

    embedding_model = LlamaCppEmbeddings(model_path="./model/mistral-7b-openorca.Q5_K_M.gguf")

    # AaC documentation
    aac_vectorstore = FAISS.load_local("aac_vectorstore", embedding_model, allow_dangerous_deserialization=True)
    aac_retriever = aac_vectorstore.as_retriever()

    # SysML v2 documentation
    sysml_vectorstore = FAISS.load_local("sysml_vectorstore", embedding_model, allow_dangerous_deserialization=True)
    sysml_retriever = sysml_vectorstore.as_retriever()

    retriever = MergerRetriever(retrievers=[aac_retriever, sysml_retriever])

    rag_init_end = time.time()
    print(f"RAG initialization took {rag_init_end - rag_init_start} seconds")
    return retriever

def predict(message, history, request: gr.Request):
    prompt_start = time.time()
    response = (chain({"question": message, "chat_history": history}))

    prompt_end = time.time()
    # for key, value in response.items():
    #     print(f"{key}: {value}\n")
    # append_to_log(message, answer, prompt_end - prompt_start, request.username)
    return response["answer"]

def vote(data: gr.LikeData, request: gr.Request):
    if data.liked:
        print(f"{request.username} upvoted this response: {data.value}")
    else:
        print(f"{request.username} downvoted this response: {data.value}")

def clear_content(input):
    return ""

# setup retrieval augmented generation (RAG)
retriever = initialize_rag()

# setup memory
memory = ConversationBufferMemory(
            memory_key="chat_history",
            max_len=50,
            return_messages=True,
        )

# base_url="http://127.0.0.1:11434/v1/", api_key="Not-a-real-key"
llm = ChatOpenAI(
    openai_api_base="http://127.0.0.1:11434/v1/", 
    openai_api_key="Not-a-real-key", 
    model_name="mistral", 
    temperature=0.2)

chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            # prompt_template=PROMPT,
        )

# Setup ChatInterface components
chatbot = gr.Chatbot(height=600, avatar_images=("human.jpg", "ai-bot.jpg"), scale=7)
clear = gr.Button(value="🗑️", variant="secondary", size="sm", scale=1)
prompt = gr.Textbox(label="User Prompt", placeholder="Enter your request here, and hit <enter>",  scale=7)
submit = gr.Button(value="▶️", variant="primary", size="sm", scale=1)
stop = gr.Button(value="🛑", variant="stop", size="sm", scale=1)

# Lanuch the MvpInterface
MvpInterface(predict,
            title="AI Engineering Assistant", 
            image="ai-bot.jpg",
            description="Your helpful AI engineering chat bot assistant.  How can I help you today?", 
            chatbot=chatbot, 
            textbox=prompt, 
            submit_btn=submit,
            stop_btn=stop,
            clear_btn=clear,
            retry_btn=None,
            undo_btn=None,
            # This js parameter sets the UI to "dark mode"...which I hacked out of the theme builder
            js="""() => {
            if (document.querySelectorAll('.dark').length) {
                document.querySelectorAll('.dark').forEach(el => el.classList.remove('dark'));
            } else {
                document.querySelector('body').classList.add('dark');
            }
        }""",
            like=vote).launch()
