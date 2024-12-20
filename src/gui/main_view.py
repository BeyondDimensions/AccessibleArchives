import streamlit as st
from .chat_view import chat_view
from .pdf_view import pdf_view
from config import APP_NAME, FAVICON
from config.languages import get_languages
from storage import get_doc_colxns_names, get_doc_colxn
from rag import DocsEmbedding
from . import state_data
from utils import logger

def initialise_st_session():
    set_selected_doc_colxn(get_doc_colxns_names()[0])
    
    st.session_state['display_pdf'] = st.session_state.get('display_pdf',True)
    st.session_state['display_txt'] = st.session_state.get('display_txt',True)


def streamlit_config():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=FAVICON,
        layout="wide"
    )
    st.html("<style> .main {overflow: hidden} </style>")


def set_selected_doc_colxn(doc_colxn_name: str):
    st.session_state['current_doc_collection'] = get_doc_colxn(
        doc_colxn_name
    )
    st.session_state['current_doc_embeddings'] = DocsEmbedding(
        doc_colxn_name,
        st.session_state['current_doc_collection'].transcripts_dir
    )
    st.session_state['current_doc_colxn_name'] = doc_colxn_name
    print("HERE")


def main_view():
    # st.title('APP_NAME')

    streamlit_config()

    with st.container(height=None):
        label_col, doc_selector_col, pdf_chkbx,txt_chkbx,lang_selector_col = st.columns([2, 3,1,1, 1])
        with lang_selector_col: 
            language_code = st.selectbox(
                'language', get_languages(),
                label_visibility="collapsed"
            )
            state_data.set_language(language_code)
            
        with label_col:
            label = state_data.get_language_config().gui_text.DOCUMENT_COLLECTION
            st.html(f'<b style="font-size: 2em">{label}:</b>')
        with doc_selector_col:
            label = state_data.get_language_config().gui_text.SELECT_DOC_COLXN
            
            doc_colxn_name = st.selectbox(
                label, get_doc_colxns_names(),
                label_visibility="collapsed"
            )
            if doc_colxn_name != st.session_state["current_doc_colxn_name"]:
                set_selected_doc_colxn(doc_colxn_name)
        with pdf_chkbx:
            st.session_state['display_pdf'] = st.checkbox("PDF")
        with txt_chkbx:
            st.session_state['display_txt'] = st.checkbox("TXT")
            
            
        pdf_col = None
        if st.session_state['display_txt'] and st.session_state['display_pdf']:
            chat_col, pdf_col = st.columns([1, 2])
        elif not  st.session_state['display_txt'] and not  st.session_state['display_pdf']:
            chat_col = st.columns([1])[0]
        else:
            chat_col, pdf_col, = st.columns([1, 1])
             
        with chat_col:
            chat_view()  # IMPORTANT: load chat view before PDF-View
        if pdf_col:
            with pdf_col:
                pdf_view()  # IMPORTANT: load PDF-View after Chat view
