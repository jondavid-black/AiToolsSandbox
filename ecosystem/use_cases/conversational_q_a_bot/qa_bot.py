import requests, json
import time
from datetime import datetime
import gradio as gr


model = 'mistral_assistant'
context = [] 
time_fmt = "%Y-%m-%d %H:%M:%S"


import gradio as gr

#Call Ollama API
def generate(prompt, context):
    r = requests.post('http://localhost:11434/api/generate',
                     json={
                         'model': model,
                         'prompt': prompt,
                         'context': context
                     },
                     stream=False)
    r.raise_for_status()

    response = ""  

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        print(response_part)
        if 'error' in body:
            raise Exception(body['error'])

        response += response_part

        if body.get('done', False):
            context = body.get('context', [])
            return response, context

def append_to_log(prompt, response, duration):
    with open('assistant_log.md', 'a') as f:
        log_prompt = "> " + prompt.replace('\n', '\n> ')
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


#########################Gradio Code##########################
block = gr.Blocks()

with block:

    gr.Markdown("""<h1><center> Chatty Cathy - A Q&A Chatbot w/ Conversation History </center></h1>
    """)

    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Type here")

    state = gr.State()

    message.submit(chat, inputs=[message, state], outputs=[chatbot, state, message])


block.launch(debug=True)