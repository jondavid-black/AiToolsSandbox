import os
import requests, json
import time
from datetime import datetime
import gradio as gr
from langchain_openai import OpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain


time_fmt = "%Y-%m-%d %H:%M:%S"

def append_to_log(prompt, response, duration):
    with open('summary_log.md', 'a') as f:
        log_prompt = "> " + prompt.replace('\n', '\n> ')
        log_response = ">> " + response.replace('\n', '\n>> ')
        minutes, seconds = divmod(duration, 60)
        f.write(f"# Log Entry {datetime.now().strftime(time_fmt)} - Duration {minutes}m {seconds:.2f}s\n\n{log_prompt}\n{log_response}\n\n")
        f.flush()


def summarize(url, chat_history):

    # load the url content
    loader = WebBaseLoader(url)
    docs = loader.load()

    # setup the llm
    llm = OpenAI(base_url="http://localhost:8000/v1", api_key="NOT_A_KEY")

    # summarize content
    start = time.time()
    chain = load_summarize_chain(llm, chain_type="stuff")
    result = chain.invoke(docs)
    print(f"DEBUG:  result = {result}")
    end = time.time()

    output = result["output_text"]
    append_to_log(url, output, end - start)
    chat_history.append((url, output))

    return "", chat_history


#########################Gradio Code##########################
block = gr.Blocks()

with block:

    gr.Markdown("""
        <h1><center> The Summarization-inator! </center></h1>
    """)

    with gr.Row():
        message = gr.Textbox(placeholder="URL here")
        button = gr.Button("Summarize")
    
    chatbot = gr.Chatbot(height="height: 50vh", avatar_images=("rock.jpg", "doof.jpg"))

    button.click(summarize, inputs=[message, chatbot], outputs=[message, chatbot])


block.launch(debug=True)