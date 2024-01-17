# Chatty Cathy Q&A AI Bot with Conversation History

An enhancement to the miminum viable product for a chatbot to answer questions and remember the user conversation. This bot can answer questions and include previous details of the conversation in the user interaction. It is still not very smart, but at least supports refinement based on user feedback.  It provides a minimal web ui for asking questions and getting answers.

## Technology

- Ollama:  A LLM execution tool for linux.
- Mistral 7B:  A LLM model trained on the Mistral 7B dataset.
- Gradio: A python-based web ui framework tailored for AI applications.

## Approach

This is fundamentally identical to the ```../basic_q_a_bot``` use case, but with mods to the ```qa_bot.py``` to maintain conversation history and provide that as context to the model via the Ollama REST call.
- Cut-and-paste evrything from the basic_q_a_bot use case into this directory (except the ```readme.md``` obviously).
- Add a ```chat_history``` variable to the ```qa_bot.py``` script.
- Add a ```chat_history``` parameter to the ```ollama``` call in the ```qa_bot.py``` script.
- Run some manual tests and log the results.

Everything else is unchanged from the basic_q_a_bot use case.

## Observations

This was very quick to put in place given the original example already had a chat history capability.  Things worked as expected.  Most importantly, the AI clearly maintained context from the previous conversation.  I was able to refer to prior interactions and the AI handled it well.