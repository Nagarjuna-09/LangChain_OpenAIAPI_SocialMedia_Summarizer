import os
import requests
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary
from typing import Tuple

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)

    # If you do not want to waste proxycurl API call credits, you can use mock  True, which calls the JSON data you saved in gitgist url instead of calling from provided linkedin url
    # We wrote this logic in linkedin function in linkedin.py file
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=False)
    print(linkedin_data)

    variable_prompt_template = """
    Given the information {variable_data} about a person, i want you to create:
    1. Provide a short summery about the person
    2. Tell me two interesting facts about the person
    
    \n {format_instructions}
    """

    # partial variables are used to plug in format instructions of the output into the prompt
    prompt = PromptTemplate(template=variable_prompt_template, input_variables=["variable_data"],
                            partial_variables={"format_instructions": summary_parser.get_format_instructions()})
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # chain = LLMChain(llm=llm, prompt=prompt)
    chain = prompt | llm | summary_parser
    res: Summary = chain.invoke({"variable_data": linkedin_data})
    return res, linkedin_data.get("profile_pic_url")


ice_break_with(name="Nagarjuna Nathani")
