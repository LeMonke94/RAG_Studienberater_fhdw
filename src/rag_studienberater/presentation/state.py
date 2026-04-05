"""
Zentrales Session-State Management.
Alle Streamlit session_state Zugriffe laufen über dieses Modul.
"""

# Imports
from dataclasses import dataclass, field
import streamlit as st


@dataclass
class ChatMessage:
    role: str       # "user" | "assistant"
    content: str
    sources: list[str] = field(default_factory=list)
    has_evidence: bool = True


def init() -> None:
    """Initialisiert den Session-State beim ersten Laden der Seite."""

    if 'messages_history' not in st.session_state:
        st.session_state['messages_history'] = []

def get_messages() -> list[ChatMessage]:
    return st.session_state['messages_history']

def add_message(message: ChatMessage) -> None:
    st.session_state['messages_history'].append(message)

def clear_messages() -> None:
    st.session_state['messages_history'] = []