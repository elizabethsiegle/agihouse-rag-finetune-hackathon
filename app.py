from met import find_competitors, research_company
from metaphor_python import Metaphor
import os
from PIL import Image
import requests
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
     Mail, Attachment, FileContent, FileName, FileType, Disposition)
from dotenv import dotenv_values
import streamlit as st
from typing import List, Union

with open('./css/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
config = dotenv_values(".env")
os.environ["METAPHOR_API_KEY"] = config.get('METAPHOR_API_KEY')
os.environ["SENDGRID_API_KEY"] = config.get('SENDGRID_API_KEY')
os.environ["BASETEN_API_KEY"] = config.get('BASETEN_API_KEY')
metaphor = Metaphor(os.environ.get("METAPHOR_API_KEY"))
example_idea = "women's tennis clothes"


st.title("Who Done it: Diligence AI") 
st.write("You think you have original ideas? You don't.😘") # semantic search
image = Image.open('competition.jpeg')
st.image(image)

idea = st.text_area("Describe your startup idea in as much depth as you'd like💡. We'll show you who's building something similar:", example_idea)
user_email = st.text_input("Email to get report📧")

if st.button('Generate competitors report👩🏻‍🏫'):
    # metaphor semantic seatch, st.write
    with st.spinner('Processing📈...'):
        startup_research = find_competitors(idea)
        print(f'startup_research ', startup_research)
        results_formatted = ''
        competitors = []
        
        for competitor in startup_research:
            url = competitor['url']
            research = research_company(url)
            print(research_company(url)) # 
            title = competitor['title']
            summary = competitor['snippet']  # company created on: {dateCreated}

            competitors.append(f'{title}: {url}. - Summary: {summary}\n\n')

        for x in range(len(competitors)):
            print(competitors[x])

    intro =  f"""
    Hey there,
    Thanks for sharing your idea! It’s a really great idea. So good in fact, that {len(competitors)} other companies did the exact same thing. Here’s what we found.
    """
    conclusion = """
    But hey, it’s .01 about the idea and .99 about execution 🙂

    Best of luck!
    """
    prompt = f"Provide an 8-word summary for each company in this list highlighting what makes them special and include their website URL and nothing else. There should be no brackets, only words. Do not repeat the prompt. {competitors}"


    report = requests.post(
        "https://model-7qkl0ne3.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {os.environ.get('BASETEN_API_KEY')}"},
        json={'prompt': prompt},
    )
    report = str(report.json()).replace('<s><s>', '').replace('[INST]', '').replace('[/INST]', '').replace(prompt, '').replace('</s>','')

    report = f'{intro} \n{report}\n {conclusion}'
    print(f'report printed {report}')

    message = Mail(
            from_email='existing_ideas@ai.com',
            to_emails=user_email,
            subject='Your competition report🔥',
            html_content=f'{report}'
        )

    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)
    if response.status_code == 202:
        st.success("Email sent! Check your email for your personal competitors report")
        print(f"Response Code: {response.status_code} \n Message sent!")
    else:
        st.warning("Email not sent--check email")
    


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
<p>Developed with ❤ by <a href="https://twitter.com/engineer_abel" target="_blank">Abel Regalado</a>, <a href="https://twitter.com/sarahchieng" target="_blank">Sarah Chieng</a>, & <a href="https://twitter.com/lizziepika" target="_blank">Lizzie Siegle</a></p>
<p>✅ out the code on <a href="https://github.com/elizabethsiegle/agihouse-rag-finetune-hackathon" target="_blank">GitHub</a></p>
</footer>
"""
st.markdown(footer,unsafe_allow_html=True)
