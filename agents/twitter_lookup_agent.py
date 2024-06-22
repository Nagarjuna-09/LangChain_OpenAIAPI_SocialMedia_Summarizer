import os
from langchain_openai import ChatOpenAI # To use open ai as our LLM
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
load_dotenv()

# importing tools
from langchain_core.tools import Tool
from tools.tools import get_profile_url_tavily

from langchain import hub

def lookup(name: str) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    variable_prompt = """given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username
       In Your Final answer only the person's username"""

    prompt = PromptTemplate(template = variable_prompt, input_variables = ["name_of_person"])

    tools_for_agent = [
        Tool(
            name="Twitter Crawler for username",
            func=get_profile_url_tavily,
            description="useful for when you need to get the Twitter Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    # creating agent
    agent = create_react_agent(llm=llm, tools=tools_for_agent,prompt=react_prompt)
    agent_executor = AgentExecutor(agent = agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": variable_prompt.format(name_of_person=name)}
    )

    twitter_profile_url = result["output"]
    return twitter_profile_url

twitter_profile_url = lookup(name = "The Nagarjuna")
print(twitter_profile_url)