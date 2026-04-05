"""
FHDW RAG Studienberater – Streamlit UI
Datei-Pfad im Projekt:
    src/rag_studienberater/presentation/ui.py

Starten vom Projekt-Root aus:
    streamlit run src/rag_studienberater/presentation/ui.py
"""

import streamlit as st
from rag_studienberater.bootstrap.container import create_container

# ──────────────────────────────────────────────
# Seiten-Konfiguration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="FHDW Studienberater",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={},
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --navy:        #0B1E3D;
    --navy-mid:    #112952;
    --navy-light:  #1A3A6B;
    --orange:      #E8500A;
    --orange-light:#FF6B2B;
    --text-main:   #F0F4FF;
    --text-muted:  #8BA3C7;
    --border:      rgba(255,255,255,0.10);
    --card:        rgba(255,255,255,0.06);
    --radius:      14px;
}

/* ── Hintergrund Gradient ── */
html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Sans', sans-serif;
    background: linear-gradient(135deg, #0B1E3D 0%, #1A2E55 50%, #2A1810 100%) !important;
    color: var(--text-main);
    min-height: 100vh;
}

/* Sidebar + Toggle komplett verstecken */
section[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] { display: none !important; }

#MainMenu, footer, header { visibility: hidden; }

/* ── Layout-Wrapper ── */
.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 100% !important;
}

/* ── Header ── */
.app-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 0 1.25rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.app-header h1 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
    background: linear-gradient(90deg, #FFFFFF, var(--orange-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-header .subtitle {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin: 0;
}

/* ── Linke Panel (Filter) ── */
.filter-panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1rem;
    height: fit-content;
    backdrop-filter: blur(10px);
}
.filter-panel h3 {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--orange-light);
    margin: 0 0 1rem 0;
}
.filter-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1rem 0;
}

/* ── Selectbox & Slider im Panel ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-main) !important;
}
.stSelectbox label, .stSlider label {
    font-size: 0.78rem !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
}
.stSlider > div > div > div > div {
    background: var(--orange) !important;
}

/* ── Chat Bubbles ── */
.user-bubble {
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange-light) 100%);
    color: #fff;
    border-radius: var(--radius) var(--radius) 4px var(--radius);
    padding: 0.85rem 1.1rem;
    margin: 0.75rem 0 0.75rem 15%;
    font-size: 0.92rem;
    line-height: 1.55;
    box-shadow: 0 4px 15px rgba(232,80,10,0.3);
}

.bot-bubble {
    background: var(--card);
    color: var(--text-main);
    border-radius: var(--radius) var(--radius) var(--radius) 4px;
    padding: 0.85rem 1.1rem;
    margin: 0.75rem 15% 0.75rem 0;
    font-size: 0.92rem;
    line-height: 1.6;
    border: 1px solid var(--border);
    backdrop-filter: blur(8px);
}

.no-evidence-bubble {
    background: rgba(255,200,50,0.1);
    border: 1px solid rgba(255,200,50,0.3);
    color: #FFD580;
    border-radius: var(--radius);
    padding: 0.75rem 1rem;
    margin: 0.75rem 15% 0.75rem 0;
    font-size: 0.9rem;
}

/* ── Quellen-Badges ── */
.quellen-header {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0.6rem 0 0.3rem;
}
.quelle-tag {
    display: inline-block;
    background: rgba(232,80,10,0.15);
    color: var(--orange-light);
    border: 1px solid rgba(232,80,10,0.3);
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem;
    font-family: 'IBM Plex Mono', monospace;
    margin: 0.15rem 0.2rem 0.15rem 0;
}

/* ── Eingabe ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-main) !important;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.95rem;
    padding: 0.65rem 1rem;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(232,80,10,0.2) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--orange), var(--orange-light)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    transition: opacity 0.2s, transform 0.1s;
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-1px);
}

/* ── Beispielfragen ── */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-main) !important;
    font-size: 0.85rem !important;
    text-align: left !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    border-color: var(--orange) !important;
    color: var(--orange-light) !important;
}

/* ── Ladeanimation ── */
.thinking-dots span {
    display: inline-block;
    width: 7px; height: 7px;
    background: var(--orange-light);
    border-radius: 50%;
    margin: 0 2px;
    animation: bounce 1.2s infinite ease-in-out;
}
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
    40%            { transform: scale(1);   opacity: 1; }
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Container (DI) – einmalig gecacht
# ──────────────────────────────────────────────
@st.cache_resource(show_spinner="🔗 Verbinde mit Qdrant & Ollama …")
def get_container():
    return create_container()


# ──────────────────────────────────────────────
# Session State
# ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "container" not in st.session_state:
    try:
        st.session_state.container = get_container()
        st.session_state.backend_error = None
    except Exception as e:
        st.session_state.container = None
        st.session_state.backend_error = str(e)


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <span style="font-size:2.2rem">🎓</span>
  <div>
    <h1>FHDW Studienberater</h1>
    <p class="subtitle">KI-Assistent für Fragen rund ums Studium · Basierend auf offiziellen Modulhandbüchern</p>
  </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.get("backend_error"):
    st.error(
        f"⚠️ Backend nicht erreichbar: {st.session_state.backend_error}\n\n"
        "Stelle sicher, dass **Ollama** läuft und **Qdrant** konfiguriert ist."
    )


# ──────────────────────────────────────────────
# Zwei-Spalten Layout: Links Filter, Rechts Chat
# ──────────────────────────────────────────────
col_filter, col_chat = st.columns([1, 3], gap="large")

studiengaenge = [
    "Alle Studiengänge",
    "BA Artificial Intelligence",
    "BA Betriebswirtschaft (VZ)",
    "BA Betriebswirtschaft (TZ)",
    "BA International Business Management",
    "BA Wirtschaftsinformatik (VZ)",
    "BA Wirtschaftsinformatik (TZ)",
    "BA Wirtschaftsrecht",
    "MA Betriebswirtschaft",
    "MA Corporate Finance",
    "MA E-Leadership",
    "MA IT-Management",
    "MA Management & Vertrieb",
    "MA Sustainable Unternehmensführung",
    "MA Wirtschaftsinformatik",
    "MBA General Management",
]

# ── Linkes Panel ──
with col_filter:
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    st.markdown('<h3>⚙️ &nbsp;Einstellungen</h3>', unsafe_allow_html=True)

    selected_sg = st.selectbox(
        "🎓 Studiengang",
        studiengaenge,
    )

    st.markdown('<hr class="filter-divider">', unsafe_allow_html=True)

    top_k = st.slider("🔍 Quellen (top-k)", min_value=1, max_value=10, value=5)

    st.markdown('<hr class="filter-divider">', unsafe_allow_html=True)

    if st.button("🗑️ Chat leeren", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:0.68rem;color:var(--text-muted);margin-top:1rem;"
        "text-align:center'>Powered by<br>Qdrant · Ollama · qwen2.5:7b</p>",
        unsafe_allow_html=True,
    )


# ── Rechter Chat-Bereich ──
with col_chat:

    # Render-Hilfsfunktion
    def render_message(role: str, content: str, sources=None, has_evidence: bool = True):
        if role == "user":
            st.markdown(f'<div class="user-bubble">{content}</div>', unsafe_allow_html=True)
        else:
            if not has_evidence:
                st.markdown(
                    f'<div class="no-evidence-bubble">⚠️ {content}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f'<div class="bot-bubble">{content}</div>', unsafe_allow_html=True)
                if sources:
                    tags_html = "".join(
                        f'<span class="quelle-tag">{s.source}'
                        f'{" · S. " + str(s.page) if s.page is not None else ""}'
                        f'</span>'
                        for s in sources[:6]
                    )
                    st.markdown(
                        f'<div class="quellen-header">📎 Quellen</div>{tags_html}',
                        unsafe_allow_html=True,
                    )

    # Eingabe ZUERST verarbeiten (vor dem Rendern)
    with st.form("chat_form", clear_on_submit=True):
        inp_cols = st.columns([8, 1])
        user_input = inp_cols[0].text_input(
            "Frage",
            placeholder="z. B. Welche Pflichtmodule hat der BA AI?",
            label_visibility="collapsed",
        )
        submitted = inp_cols[1].form_submit_button("→", use_container_width=True)

    if "pending_question" in st.session_state:
        user_input = st.session_state.pop("pending_question")
        submitted = True

    # Antwort generieren und in session_state speichern
    if submitted and user_input.strip():
        frage = user_input.strip()
        frage_mit_kontext = (
            f"[{selected_sg}] {frage}" if selected_sg != "Alle Studiengänge" else frage
        )

        st.session_state.messages.append({"role": "user", "content": frage})

        if st.session_state.container:
            try:
                answer       = st.session_state.container.answer_use_case.execute(frage_mit_kontext)
                text         = answer.text
                sources      = answer.sources
                has_evidence = answer.has_evidence
            except Exception as e:
                text         = f"Fehler beim Abrufen der Antwort: {e}"
                sources      = []
                has_evidence = False
        else:
            text         = "Backend nicht erreichbar. Bitte Ollama starten und .env prüfen."
            sources      = []
            has_evidence = False

        st.session_state.messages.append({
            "role":         "assistant",
            "content":      text,
            "sources":      sources,
            "has_evidence": has_evidence,
        })
        st.rerun()

    # Beispielfragen (nur wenn Chat leer)
    if not st.session_state.messages:
        st.markdown(
            "<p style='color:var(--text-muted);font-size:0.82rem;margin-top:1rem;"
            "text-align:center'>💡 Beispielfragen zum Ausprobieren</p>",
            unsafe_allow_html=True,
        )
        examples = [
            "Welche Module gehören zum Studiengang BA Wirtschaftsinformatik?",
            "Was sind die Zugangsvoraussetzungen für den MBA?",
            "Wie viele ECTS hat das Modul Projektmanagement?",
            "Gibt es ein Auslandssemester im BA International Business?",
        ]
        ex_cols = st.columns(2)
        for i, ex in enumerate(examples):
            if ex_cols[i % 2].button(ex, use_container_width=True, key=f"ex_{i}"):
                st.session_state.pending_question = ex
                st.rerun()

    # Chatverlauf NACH dem Eingabefeld rendern
    for msg in st.session_state.messages:
        render_message(
            msg["role"],
            msg["content"],
            sources=msg.get("sources"),
            has_evidence=msg.get("has_evidence", True),
        )