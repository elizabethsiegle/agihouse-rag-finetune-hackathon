from metaphor_python import Metaphor
import requests

METAPHOR_API_KEY = "2e22c147-fe26-4934-8c1f-a82a834afafd"
# given an idea, returns a list of competitors 
def find_competitors(idea):
    search = "Here's my company idea, " + idea + ". Here's a company that's doing it:"
    url = "https://api.metaphor.systems/search/snippet"

    payload = { "query": search,
            "snippetLength": 3,
            "useAutoprompt": False,
            "numResults": 5,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": METAPHOR_API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    results = response_json['results']
    return results

#given a company url, returns websites + document IDs about the company
def research_company(company_link):
    url = "https://api.metaphor.systems/search"

    payload = {
        "query": company_link,
        "type": "keyword",
        "numResults": 2,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": METAPHOR_API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    results = response_json['results']
    return results

def get_contents(document_id):
    base_url = "https://api.metaphor.systems/contents"
    url = f"{base_url}?ids={document_id}"
    headers = {
        "accept": "application/json",
        "x-api-key": METAPHOR_API_KEY
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    results = response_json['contents'][0]["extract"]
    return results

def whodoneit(idea):
    #find the top 10 competitors
    competitors = {}
    competitor_results = find_competitors(idea)
    for competitor in competitor_results:
        
        #for each competitor, look up 5 links
        competitor_contents = []
        competitor_contents.append(competitor['snippet'])
        competitor_research = research_company(competitor['url'])
        for link in competitor_research:
            competitor_contents.append(get_contents(link['id']))
        competitors[competitor['url']] = competitor_contents
    print(competitors)
    return competitors

idea = "women's tennis clothing"
print(find_competitors(idea))
#whodoneit(idea)
