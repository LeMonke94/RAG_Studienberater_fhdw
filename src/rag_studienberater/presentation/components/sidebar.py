"""
Sidebar-Komponente
"""

# Imports
import streamlit as st

from rag_studienberater.bootstrap.container import Container
from rag_studienberater.presentation import state


def render(container: Container) -> None:
    """Rendert die gesamte Sidebar."""

    with st.sidebar:
        st.header('Studienberater')
        st.caption('RAG-basiertes Frage-Antwort-System\nfür FHDW-Studieninteressierte.')

        st.divider()

        _render_ingest_section(container)

        st.divider()

        _render_chat_controls()

def _render_ingest_section(container: Container) -> None:
    st.subheader('Wissensbasis')
    st.caption('PDFs (inkl. Unterordner) und Webseiten in den Vector Store laden.')

    if st.button('📥 Wissensbasis aufbauen', use_container_width=True):
        try:
            with st.spinner('Lese PDFs ein (inkl. Unterordner)...'):
                container.ingest_use_case.execute_folder('data/raw/pdf')

            with st.spinner('Lese Webseiten ein...'):
                container.ingest_use_case.execute_urls_from_file('data/raw/web/url.json')

            st.success('Wissensbasis erfolgreich aufgebaut.')
        except Exception as e:
            st.error(f'Fehler: {e}')

def _render_chat_controls() -> None:
    st.subheader('Chat')

    if st.button('🗑️ Chatverlauf löschen', use_container_width=True):
        state.clear_messages()
        st.rerun()