import os
import requests
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def ice_break_with(name:str)->str:
    linkedin_url = linkedin_lookup_agent(name = name)

    # If you do not want to waste proxycurl API call credits, you can use mock  True, which calls the JSON data you saved in gitgist url instead of calling from provided linkedin url
    # We wrote this logic in linkedin function in linkedin.py file
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/nagarjuna-nathani/", mock = False)
    print(linkedin_data)
    # data = """Elon is a good boy. He was born in 2020 and has one brother and studies at Elon school of Engineering"""

    variable_prompt = """
    Given the information {variable_data} about a person, i want you to create:
    1. His name
    2. Where is he doing during 2018?
    3. His highest level of education
    4. Can you guess his age right now as of 2024?
    5. How many years of work experience did he have?
    """

    prompt = PromptTemplate(template=variable_prompt, input_variables=["variable_data"])
    llm = ChatOpenAI(temperature = 0, model_name = "gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=prompt)
    res = chain.run(variable_data=linkedin_data)
    print(res)

ice_break_with(name = "Nagarjuna Nathani")