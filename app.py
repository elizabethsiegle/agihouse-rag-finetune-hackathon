from metaphor_python import Metaphor
import streamlit as st

st.title("Hackathon product name")
site = st.text_input("Link to company site")
if st.button('Generate competitors report'):
    
# st.text_input("Email to send report to")