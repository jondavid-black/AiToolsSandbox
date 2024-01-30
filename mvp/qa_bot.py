import openai
from openai import OpenAI
import gradio as gr

# openai.api_key = "Not-a-real-key"  # Replace with your key
# openai.base_url = "http://127.0.0.1:8000/v1/"

client = OpenAI(base_url="http://127.0.0.1:8000/v1/", api_key="Not-a-real-key")

system_prompt = "You are a helpful AI assistant named Tom.  You must always provide correct and complete responses to the user's requests.  If the user provides information rather than a question or a command, simply reply with OK."

# def predict(message, history):
#     history_openai_format = []
#     for human, assistant in history:
#         history_openai_format.append({"role": "user", "content": human })
#         history_openai_format.append({"role": "assistant", "content":assistant})
#     history_openai_format.append({"role": "user", "content": message})

#     completion = openai.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {
#                 "role": "user",
#                 "content": message,
#             }, {
#                 "role": "system",
#                 "content": system_prompt,
#             }
#         ],
#     )

#     response = completion.choices[0].message.content
#     print(f"completion: {completion}")
#     print(f"response: {response}")

#     partial_message = ""
#     for chunk in response:
#         if len(chunk['choices'][0]['delta']) != 0:
#             partial_message = partial_message + chunk['choices'][0]['delta']['content']
#             yield partial_message

def predict(message, history):
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

    print(f"stream: {stream}")

    partial_message = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message

gr.ChatInterface(predict).launch()