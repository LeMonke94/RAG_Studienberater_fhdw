"""
Chat-Komponente
"""

# Imports
import streamlit as st

from rag_studienberater.bootstrap.container import Container
from rag_studienberater.domain.models import Answer
from rag_studienberater.presentation import state
from rag_studienberater.presentation.state import ChatMessage


def render(container: Container) -> None:
    """Rendert den Chatverlauf und verarbeitet neue Eingaben."""
    _render_history()
    _handle_input(container)

def _render_history() -> None:
    """Zeigt alle bisherigen Nachrichten der Session an."""
    for message in state.get_messages():
        with st.chat_message(message.role):
            st.markdown(message.content)
            if message.sources:
                _render_sources(message.sources)

def _handle_input(container: Container) -> None:
    """Nimmt eine neue Nutzerfrage entgegen und generiert die Antwort."""
    question = st.chat_input('Deine Frage zum Studium an der FHDW...')
    if not question:
        return

    # display and save user message
    state.add_message(ChatMessage(role='user', content=question))
    with st.chat_message('user'):
        st.markdown(question)

    # generate and display assistant answer
    with st.chat_message('assistant'):
        with st.spinner('Suche in den Unterlagen...'):
            answer = container.answer_use_case.execute(question)

        _render_answer(answer)

    # save answer
    sources = _format_sources(answer) if answer.has_evidence else []
    state.add_message(ChatMessage(
        role='assistant',
        content=answer.text,
        sources=sources,
        has_evidence=answer.has_evidence,
    ))

def _render_answer(answer: Answer) -> None:
    """Zeigt eine Antwort inkl. Quellenangaben an."""
    if answer.has_evidence:
        st.markdown(answer.text)
        sources = _format_sources(answer)
        if sources:
            _render_sources(sources)
    else:
        st.warning(answer.text)

def _render_sources(sources: list[str]) -> None:
    """Zeigt Quellenangaben in einem aufklappbaren Bereich."""
    with st.expander(f"📄 Quellen ({len(sources)})"):
        for source in sources:
            st.markdown(f"- {source}")

def _format_sources(answer: Answer) -> list[str]:
    """Wandelt Chunk-Objekte in lesbare Quellenstrings um."""
    return sorted({
        f"**{chunk.source}**, Seite {chunk.page}" if chunk.page
        else f"**{chunk.source}**"
        for chunk in answer.sources
    })