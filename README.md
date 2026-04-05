# RAG-Studienberater

RAG-basiertes Frage-Antwort-System für FHDW-Studienberatung.

---

# Technologieauswahl

| Technologie       | Paket                      | Zweck                                          |
|-------------------|----------------------------|------------------------------------------------|
| Laufzeitumgebung  | Python 3.11+               | Basis des Gesamtprojekts                       |
| LLM (lokal)       | qwen2.5:7b via Ollama      | Generiert die Antworten                        |
| Embedding         | bge-m3 via Ollama          | Wandelt Text in Vektoren um                    |
| Text-Splitting    | langchain-text-splitters   | Teilt Dokumente in Chunks auf                  |
| LLM-Integration   | langchain-ollama           | Verbindet die Pipeline mit Ollama              |
| Vektordatenbank   | Qdrant                     | Speichert Chunks und Vektoren                  |
| PDF-Extraktion    | pdfplumber                 | Extrahiert Text aus PDFs                       |
| Web-Scraping      | BeautifulSoup4 + requests  | Extrahiert Text aus FHDW-Webseiten             |
| User Interface    | Streamlit                  | Chat-Interface                                 |
| Konfiguration     | pydantic-settings          | Typsichere Verwaltung von Einstellungen        |
| Testing           | pytest                     | Automatisierte Unit-Tests                      |
| Code-Qualität     | ruff                       | Linting und automatische Formatierung          |
| Typ-Prüfung       | mypy                       | Statische Typprüfung                           |
| Projektdefinition | pyproject.toml             | Metadaten, Abhängigkeiten, Tool-Konfiguration  |

---

# Projektstruktur

```
data/
  raw/pdf/          FHDW-Dokumente (PDFs) die eingelesen werden
  evaluation/       Testset und Evaluationsergebnisse

scripts/
  smoke_test.py     Schnelltest der gesamten Pipeline
  evaluate.py       Systematische Evaluation anhand des Testsets

src/rag_studienberater/
  application/
    services/       Einzelne, klar abgegrenzte Bausteine
    use_cases/      Zusammengesetzte Abläufe (IngestUseCase, AnswerUseCase, ...)
  bootstrap/        Verdrahtung aller Abhängigkeiten (Container)
  config/           Einstellungen und Logging
  domain/
    models/         Datenstrukturen (Document, Chunk, Answer, ...)
    ports/          Abstrakte Interfaces (EmbeddingPort, VectorStorePort, ...)
  infrastructure/   Konkrete Implementierungen der Ports
    document_loaders/
    embedding_models/
    language_models/
    text_splitters/
    vector_stores/
  presentation/     UI-Schicht (Streamlit)

tests/
  conftest.py       Stubs und Fixtures für alle Unit-Tests
  unit/
    services/       Tests für Application Services
    use_cases/      Tests für Use Cases
```

---

# Datenmodelle

**Dokumentstruktur:** `Document` → `Page`

**Retrieval/Kontextstruktur:** `Chunk`, `ScoredChunk`, `RetrievalResult`

**Interaktionsstruktur:** `Query`, `Answer`

---

# Installationsanweisung

## Voraussetzungen

- Python 3.11+
- [Ollama](https://ollama.com) installiert und gestartet
- [Qdrant Cloud](https://cloud.qdrant.io) Account (oder lokale Qdrant-Instanz)

## Installation
py -m pytest tests/ 

**1. Repository klonen**
```bash
git clone <repo-url>
cd RAG_Studienberater
```

**2. Virtuelle Umgebung erstellen und aktivieren**
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/macOS:
source .venv/bin/activate
```

**3. Pakete installieren**
```bash
# Nur Laufzeit-Abhängigkeiten:
pip install -e .

# Mit Dev-Tools (pytest, ruff, mypy):
pip install -e .[dev]
```

**4. Ollama-Modelle herunterladen**
```bash
ollama pull qwen2.5:7b
ollama pull bge-m3
```

**5. Umgebungsvariablen konfigurieren**

Kopiere `.env.example` zu `.env` und trage deine Zugangsdaten ein:

```bash
cp .env.example .env
```

`.env` befüllen:
```env
QDRANT__ENDPOINT=https://deine-url.qdrant.io
QDRANT__API_KEY=dein_api_key
QDRANT__COLLECTION_NAME=studienberater
QDRANT__VECTOR_DIMENSIONS=1024

OLLAMA__BASE_URL=http://localhost:11434
OLLAMA__LANGUAGE_MODEL=qwen2.5:7b
OLLAMA__EMBEDDING_MODEL=bge-m3

CHUNKING__CHUNK_SIZE=512
CHUNKING__CHUNK_OVERLAP=50

GUARDRAIL__MIN_SCORE=0.5

LOGGING__LEVEL=INFO
```

> **Wichtig:** Die verschachtelten Einstellungen verwenden doppelte Unterstriche (`__`) als Trennzeichen.

---

## Verwendung

**Schritt 1 — Dokumente einlesen**

FHDW-PDFs in `data/raw/pdf/` ablegen, dann:
```bash
py scripts/smoke_test.py
```

**Schritt 2 — Tests ausführen**
```bash
py -m pytest tests/ -v
```

**Schritt 3 — Evaluation durchführen**
```bash
# Ingest + alle 30 Testfragen auswerten:
py scripts/evaluate.py

# Dokumente bereits geladen — Ingest überspringen:
py scripts/evaluate.py --skip-ingest
```

Ergebnisse werden automatisch in `data/evaluation/results_<datum>.json` gespeichert.



"""st.markdown(###
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stApp {
    background: linear-gradient(135deg, #0B1E3D 0%, #1A2E55 50%, #2A1810 100%) !important;
    color: #F0F4FF;
}
.stTextInput > div > div > input {
    font-family: 'IBM Plex Sans', sans-serif;
}
</style>
###, unsafe_allow_html=True)"""