from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import dotenv_values
# from exa_py import Exa
# from met import find_competitors #find_similar_and_contents_url
import os
from PIL import Image
import requests
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
     Mail, Attachment, FileContent, FileName, FileType, Disposition)

import streamlit as st

with open('./css/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

config = dotenv_values(".env")
EXA_API_KEY = config.get('EXA_API_KEY')
SENDGRID_API_KEY = config.get('SENDGRID_API_KEY')
ANTHROPIC_API_KEY = config.get('ANTHROPIC_API_KEY')
example_idea = "women's tennis clothes"


st.title("Who Done it: Diligence AI") 
st.write("You think you have original ideas? You don't.😘") 
image = Image.open('competition.jpeg')
st.image(image)

idea = st.text_area("""
Describe your startup idea in as much depth as you'd like💡. 
We'll show you who's building something similar:""", example_idea)
user_email = st.text_input("Email to get report📧")

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

idea = st.text_area("""
Describe your startup idea in as much depth as you'd like💡. 
We'll show you who's building something similar:""", example_idea)
user_email = st.text_input("Email to get report📧")

if st.button('Generate competitors report👩🏻‍🏫'):
    # exa semantic search,
    with st.spinner('Processing📈...'):
        startup_research = find_competitors(idea)
        print(f'startup_research ', startup_research)
        competitors = []
        
        for competitor in startup_research:
            url = competitor['url']
            # research = research_company(url)
            title = competitor['title']
            summary = competitor['snippet']  # company created on: {dateCreated}

            competitors.append(f'{title}: {url}. - Summary: {summary}\n\n')

        for x in range(len(competitors)):
            print(competitors[x])

        intro =  f"""
        Hey there,
        Thanks for sharing your idea! It’s a really great idea. So good in fact, that {len(competitors)} 
        other companies did the exact same thing. Here’s what we found.\n\n
        """
        conclusion = """
        \n\nBut hey, it’s .01 about the idea and .99 about execution 🙂

        Best of luck!
        """

        PROMPT= f"Summarize the following external data into multiple paragraphs going over the pros for each company, what makes them different or special, and including their website according to the external data: {competitors}"
        anthropic = Anthropic(
            api_key=ANTHROPIC_API_KEY
        )
        completion = anthropic.completions.create(
            model="claude-2.1",
            max_tokens_to_sample=700,
            prompt=f"{HUMAN_PROMPT}: {PROMPT}. {AI_PROMPT}",
        )
        print(completion.completion)
        report = completion.completion
        # report = requests.post(
        #     "https://model-7qkl0ne3.api.baseten.co/production/predict",
        #     headers={"Authorization": f"Api-Key {os.environ.get('BASETEN_API_KEY')}"},
        #     json={'prompt': prompt},
        # )
        # report = str(report.json()).replace('<s><s>', '').replace('[INST]', '').replace('[/INST]', '').replace(prompt, '').replace('</s>','')

    report = f'{intro} \n{report}\n {conclusion}'
    print(f'report printed {report}')

    message = Mail(
            from_email='existing_ideas@ai.com',
            to_emails=user_email,
            subject='Your competition report🔥',
            html_content=f'{report}'
        )

    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)
    if response.status_code == 202:
        st.success("Email sent! Check your email for your personal competitors report")
        print(f"Response Code: {response.status_code} \n Message sent!")
    else:
        st.warning("Email not sent--check console")
    


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

footer {
  margin-top: auto;
  text-align: center;
}
</style>
<footer>
<p>Developed with ❤ in SF🌁</p> 
<p>✅ out the code on <a href="https://github.com/elizabethsiegle/agihouse-rag-finetune-hackathon" target="_blank">GitHub</a></p>
</footer>
"""
st.markdown(footer,unsafe_allow_html=True)
