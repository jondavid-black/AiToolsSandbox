# Code Assistant (Cody)

This is a little outside the current scope, but I discovred this and didn't want to lose it.

One of our use cases id to provide a developer assistant.  Ideally, we'd fine something along the lines of GitHub Copilot but it's not likely we'll achieve that level of performance using local open tooling.  However, there are some interesting tools that can help.  Previously we discovered Continue, a VS Code extension that enables use of a local LLM.  Here we'll look at [coLLaMA](https://github.com/iohub/coLLaMA), another VS Code extension that may provide an alternative in that space.

## The Plan

While I'd like to prove this in a completely network disconnected way, I don't see a good way to do that.  I also don't want to muck up my local VS Code configuration (which has GitHub Copilot).  I believe I'll the following:

- Create an AWS EC2 server to run the LLM
  - Download a code-oriented LLM model GGUF from HuggingFace
  - Install python-llama-cpp
  - Serve the model using the python-llama-cpp server
- Create a new Ubuntu VM using VirtualBox
  - Install VS Code on the VM
  - Install the coLLaMA extension
  - Configure the coLLaMA extension to use my EC2 python-llama-cpp LLM server

Running the EC2 server may cost me a few dollars, but shouldn't be too bad.  Once I run a few tests, I'll write up my results and destroy everything.