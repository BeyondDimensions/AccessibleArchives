import streamlit as st
from config import languages

def set_language(language_code:str):
    st.session_state["language_config"]= languages.get_language_config(language_code)
def get_language_config():
    if not "language_config" in st.session_state:
        set_language(languages.DEFAULT_LANGUAGE)
    return st.session_state["language_config"]