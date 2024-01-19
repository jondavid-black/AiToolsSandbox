import autogen

config_list = [
    {
        "base_url": "http://localhost:8000/v1",
        "api_key": "NOT_A_REAL_KEY",
        "model": "mistral"
    }
]


llm_config = {
    "timeout": 600,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0.6
}

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A human admin.",
    code_execution_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

pro_agent = autogen.AssistantAgent(
    name="pro_agent",
    llm_config=llm_config,
    system_message="You are an award winning debater. You argue for the side of the topic that you are given."
)

con_agent = autogen.AssistantAgent(
    name="con_agent",
    llm_config=llm_config,
    system_message="You are an award winning debater. You argue against the side of the topic that you are given."
)

judge_agent = autogen.AssistantAgent(
    name="judge_agent",
    llm_config=llm_config,
    system_message="You are a judge at a collegete level debate competition.  You carefully listen to both sides of the debate and decide who wins. You must choose either the pro_agent or the con_agent as the winner.  Explain the logic in your decision."
)

groupchat = autogen.GroupChat(agents=[user_proxy, pro_agent, con_agent, judge_agent], messages=[], max_round=6)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager, message="AI is a threat to humanity.",
)
