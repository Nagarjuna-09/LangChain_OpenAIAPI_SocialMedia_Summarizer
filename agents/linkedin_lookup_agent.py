import os
from langchain_openai import ChatOpenAI # To use open ai as our LLM
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
#------------------------------
# Langchain tools are interfaces that help our langchain agents, chains or LLMs use and  interact with real world
# Like if you want to search online or in a database, these tools already have some built-in functions to search online
# Tools help LLMs to interact with real world, in our case we are using a tool that can search online
# And the power of LangChain is that we convert any function in Python into a LangChain tool and make it accessible to our LLM.
# ReAct is one popular way to implement agent with LLMs

# importing tools
from langchain_core.tools import Tool
from tools.tools import get_profile_url_tavily

#------------------------------
# create_react_agent function is a built-in function in LangChain, which is going to be receiving an LLM that
# we'll be using to power our agent.

# Agent executor is the runtime of the agent. This is actually the object which is going
# to receive our prompts and our instructions what to do.

from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
#------------------------------

# langchain hub is used to download pre-made prompts by the community from the langchain team
from langchain import hub

# Takes name of person and returns his linkedin url
def lookup(name: str) -> str:
    # based on the complexity of the task you are doing, you can use higher llm models, for just getting linkedin url got-3.5 is enough
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    variable_prompt = """ given the full name {name_of_person}, I want to get the link to their linkedin profile page. Your answer should only contain url"""

    prompt = PromptTemplate(template = variable_prompt, input_variables = ["name_of_person"])

    # This will include all tools that our search agent is using.
    # We supply it with 3 algorithms (name, function - function to run, description - very imp as this is needed by LLM to decide to use this or not and when to use it)
    tools_for_agent = [
        Tool(
            name="Linkedin Crawler for url",
            func=get_profile_url_tavily,
            description="useful for when you need to get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    # creating agent
    agent = create_react_agent(llm=llm, tools=tools_for_agent,prompt=react_prompt)
    agent_executor = AgentExecutor(agent = agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": variable_prompt.format(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url
