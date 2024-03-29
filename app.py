from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from met import find_competitors, research_company, get_contents, whodoneit
from metaphor_python import Metaphor
import os
from PIL import Image
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition)
import streamlit as st

metaphor = Metaphor(os.environ.get("METAPHOR_API_KEY"))
example_idea = "PetMatchmaker: An AI-driven dating app for pets. The app uses advanced algorithms to find the perfect playdate or lifelong companion for their furry friends. It's like Tinder, but for pets, ensuring every whisker and wagging tail finds its soulmate."
load_dotenv()

st.title("Who Done it: Diligence AI") 
st.write("You think you have original ideas? You don't.😘") # semantic search
image = Image.open('competition.jpeg')
st.image(image)

idea = st.text_area("Describe your startup idea in as much depth as you'd like💡. We'll show you who's building something similar:", placeholder=example_idea)
user_email = st.text_input("Email to get report📧")

if st.button('Generate competitors report👩🏻‍🏫'):
    # metaphor semantic seatch, st.write
    startup_research = whodoneit(idea)
    print(startup_research)
    
    message = Mail(
        from_email='existing_ideas@ai.com',
        to_emails=user_email,
        subject='Your competition report🔥',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)
    # template = """Startup research: {startup_research}
    # Answer: Here are startups doing what you want to do."""
    # prompt = PromptTemplate(template=template, input_variables=["startup_research"])
    # llm = OpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    # llm_chain = LLMChain(prompt=prompt, llm=llm)
    # question = "BASED ON THE "
    # llm_chain.run(question)



with open('./css/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


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
