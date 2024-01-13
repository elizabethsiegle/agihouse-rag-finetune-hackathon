from dotenv import load_dotenv
from metaphor_python import Metaphor
import requests
import streamlit as st

metaphor = Metaphor(os.environ.get("METAPHOR_API_KEY"))
load_dotenv()

st.title("Hackathon product name")
site = st.text_input("Link to company site")
if st.button('Generate competitors report'):

# st.text_input("Email to send report to")