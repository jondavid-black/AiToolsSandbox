from datetime import datetime
import time
from openai import OpenAI
import gradio as gr

# openai.api_key = "Not-a-real-key"  # Replace with your key
# openai.base_url = "http://127.0.0.1:8000/v1/"

client = OpenAI(base_url="http://127.0.0.1:8000/v1/", api_key="Not-a-real-key")

system_prompt = "You are a helpful AI assistant named Tom.  You must always provide correct, complete, and concise responses to the user's requests.  Once you've answered the user's request, end your feedback.  If the user provides information rather than a question or a command, simply reply with OK."

time_fmt = "%Y-%m-%d %H:%M:%S"

users = {
    "Jack": "password",
    "Jill": "password"
}

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

def predict(message, history, request: gr.Request):
    prompt_start = time.time()
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "system", "content": system_prompt})
    history_openai_format.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages= history_openai_format,
        temperature=0.0,
        stream=True
    )

    partial_message = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message

    prompt_end = time.time()
    append_to_log(message, partial_message, prompt_end - prompt_start, request.username)

# Setup ChatInterface components
chatbot = gr.Chatbot(height=800, avatar_images=("human.jpg", "ai-bot.jpg"))
clear_btn = gr.Button(value="Clear Chat History", variant="secondary", size="sm")
prompt = gr.Textbox(label="User Prompt", placeholder="Enter your request here, and hit <enter>", info="This is the user prompt.  Enter your request here and the AI assistant will respond.")
submit_btn = gr.Button(value="Submit Prompt", variant="primary", size="sm")

# Lanuch the ChatInterface
gr.ChatInterface(predict,
                 title="AI Assistant", 
                 description="Your helpful AI chat bot assistant.  How can I help you today?", 
                 chatbot=chatbot, 
                 textbox=prompt, 
                 submit_btn=submit_btn,
                 clear_btn=clear_btn,
                 retry_btn=None,
                 undo_btn=None).launch(auth=auth_user)
