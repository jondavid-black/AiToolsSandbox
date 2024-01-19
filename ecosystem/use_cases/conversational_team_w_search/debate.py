import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun

# Override default OpenAI API base and key to use local LLM
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "NOT_A_KEY"

# You can choose to use a local model through Ollama for example.
#
# from langchain.llms import Ollama
# ollama_llm = Ollama(model="openhermes")

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

search_tool = DuckDuckGoSearchRun()

# Define your agents with roles and goals
pro_agent = Agent(
  role='Positive Advocate',
  goal='Uncover and evaluate positive cutting-edge developments in AI and data science and their potential impact on humanity',
  backstory="""You are an award winning debater. You argue for the positive side of the topic that you are given.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool]
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
  # llm=ollama_llm # was defined above in the file
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)

con_agent = Agent(
  role='Negative Advocate',
  goal='Uncover and evaluate negative cutting-edge developments in AI and data science and their potential impact on humanity',
  backstory="""You are an award winning debater. You argue for the negative side of the topic that you are given.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool]
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
  # llm=ollama_llm # was defined above in the file
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)

judge_agent = Agent(
  role='Debate Judge',
  goal='Evaluate teh arguments of both sides and decide who wins the debate',
  backstory="""You are a judge at a collegete level debate competition.  You carefully listen to both sides of the debate and decide who wins. You must choose either the pro_agent or the con_agent as the winner.  Explain the logic in your decision.""",
  verbose=True,
  allow_delegation=True,
  # (optional) llm=ollama_llm
)

# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.
  Your final answer is an compelling debate argument position on the positive impact of AI on humanity.""",
  agent=pro_agent
)

task2 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.
  Your final answer is an compelling debate argument position on the negative impact of AI on humanity.""",
  agent=pro_agent
)

task3 = Task(
  description="""Using the insights and arguments provided, evaluate and select a debate winner.  Consider the following criteria: validity of arguments, quality of evidence, and persuasiveness of delivery.""",
  agent=judge_agent
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[pro_agent, con_agent, judge_agent],
  tasks=[task1, task2, task3],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)