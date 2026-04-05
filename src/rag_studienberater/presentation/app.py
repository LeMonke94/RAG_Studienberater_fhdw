"""
Einstiegspunkt der Streamlit-App

Starten mit:
    streamlit run src/rag_studienberater/presentation/app.py
"""

# Imports
import streamlit as st

from rag_studienberater.bootstrap.container import Container, create_container
from rag_studienberater.presentation import state
from rag_studienberater.presentation.components import chat
from rag_studienberater.presentation.components import sidebar


@st.cache_resource
def get_container() -> Container:
    """Initialisiert den Container nur einmal pro Streamlit-Session. st.cache_resource verhindert wiederholte Verbindungsaufbauten zu Qdrant/Ollama."""
    
    return create_container()

st.set_page_config(
    page_title='FHDW Studienberater',
    page_icon='🎓',
    layout='centered',
)

st.title('FHDW Studienberater')
st.caption('Beantwortet Fragen auf Basis der FHDW-Unterlagen.')

state.init()
container = get_container()
sidebar.render(container)
chat.render(container)