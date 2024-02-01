from dotenv import dotenv_values
from exa_py import Exa
import os
import requests

config = dotenv_values(".env")
EXA_API_KEY=
exa = Exa(api_key=EXA_API_KEY)

# given an idea, returns a list of competitors including snippets
def find_competitors(idea):
    search = "Here's my company idea, " + idea + ". Here's a company that's doing it:"
    url = "https://api.exa.ai/search/snippet"

    payload = { "query": search,
            "snippetLength": 3,
            "useAutoprompt": False,
            "numResults": 5,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": EXA_API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    results = response_json['results']
    # print(f'results {results}')
    return results

#given a company url, returns websites + document IDs about the company
# def research_company(company_link):
#     url = "https://api.exa.ai/search"

#     payload = {
#         "query": company_link,
#         "type": "keyword",
#         "numResults": 2,
#     }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "x-api-key": EXA_API_KEY
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     response_json = response.json()
#     results = response_json['results']
#     return results

def find_similar_and_contents_url(idea): 
    search_response = exa.find_similar_and_contents(
        idea,
        highlights={"num_sentences":2},
        num_results=10)
    competitors = search_response.results
    print(f'competitors {competitors}')
    urls = {}
    for c in competitors:
        print(f'{c.title}: {c.url}')
    return competitors

    # print(f"comp {competitors[0]}") 

idea = "women's tennis clothing"
# print(f'find_competitors(idea){find_competitors(idea)}')
# find_sim = []
# for i in find_competitors(idea):
#     x = find_similar_and_contents_url(i['url'])
#     find_sim.append(x)
# print(f'find_sim {find_sim}')
# print(find_competitors(idea)[0]['url'])


