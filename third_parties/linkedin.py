import os
import requests
from dotenv import load_dotenv

load_dotenv()

#By default mock is false (if nothing is defined mock is considered false)
def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    # If mock is True, the query from the saved gist_file that you already scraped and saved publicly using proxycurl (for saving api calls during testing)
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/Nagarjuna-09/12fecc9ad55d2b89da143f2b318c1112/raw/84669de3eba02370cec859204fcf2084789bc53e/johnmarty.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    # If mock is false, we are scraping data from the linkedin profile that we want using proxycurl api
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()

    # below code removes empty fields as some people may leave education section or project sections empty. This saves openai tokens as empty strings are saved
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


# if __name__ == "__main__":
#     print(
#         scrape_linkedin_profile(
#             linkedin_profile_url="https://www.linkedin.com/in/nagarjuna-nathani/", mock = False
#         )
#     )