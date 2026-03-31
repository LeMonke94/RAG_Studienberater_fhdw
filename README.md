# Architektur Konzepte

domain/
├── models/    → Definition der Datenstrukturen
│               werden überall durchgereicht
├── ports/     → Interfaces für externe Tools
│               werden in infrastructure implementiert
└── services/  → Fachlogik in reinem Python
                werden in application aufgerufen

infrastructure/
└── implementiert die Ports mit echten Tools
    VectorStorePort → QdrantStore (Qdrant)
    LLMPort         → OllamaClient (Ollama)

application/
└── koordiniert services + infrastructure
    "hole Chunks (infrastructure) dann prüfe Guardrail (service)"

ui/
└── zeigt Ergebnis an, ruft application auf

| Technologie       | Paket                  | Zweck                                         |
|-------------------|------------------------|-----------------------------------------------|
| Laufzeitumgebung  | Python 3.11+           | Basis des Gesammtprojekts                     |
| LLM  (lokal)      | qwen2.5:7b             | Generiert die Antworten                       |
| LLM Framework     | langchain-ollama       | Verbindet LangChain mit Ollama                |
| Text Embedding    | bge-m3                 | Wandelt Text in Vektoren um                   |
| RAG Framework     | LangChain              | Fertige Bausteine für Pipeline                |
| Vektordatenbank   | Qdrant                 | Speichert Chunks + Vektoren                   |
| PDF-Extraktion    | pypdf + pdfplumber     | Extrahiert Text aus PDFs                      |
| Web-Scraping      | BeautifulSoup4         | Extrahiert Text aus FHDW-Webseiten            |
| User Interface    | Streamlit              | Chat-Interface ohne Frontend-Kenntnisse       |
| Konfiguration     | pydantic-settings      | Typsichere Verwaltung von Einstellungen       |
| Konfiguration     | python-dotenv          | Lädt .env-Datei in Umgebungsvariablen         |
| Testing           | pytest + pytest-mock   | Automatisierte Tests                          |
| Code-Qualität     | ruff                   | Linting und automatische Formatierung         |
| Typ-Prüfung       | mypy                   | Statische Typprüfung vor der Ausführung       |
| Versionskontrolle | Git                    | Code-Versionierung und Zusammenarbeit         |
| Projektdefinition | pyproject.toml         | Metadaten, Abhängigkeiten, Tool-Konfiguration |
langchain-text-splitters-1.1.1


# Installationsanweisung:

## Voraussetzungen

- Python 3.11+
- [Ollama](https://ollama.com) installiert und gestartet
- [Qdrant Cloud](https://cloud.qdrant.io) Account

## Installation

**1. Repository klonen**
```bash
git clone 
cd RAG_Studienberater
```

**2. Virtuelle Umgebung erstellen**
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate
```

**3. Pakete installieren**
```bash
pip install -r requirements.txt
pip install -e .
```

**4. Ollama Modelle herunterladen**
```bash
ollama pull qwen2.5:7b
ollama pull bge-m3
```

**5. Umgebungsvariablen konfigurieren**

Kopiere `.env.example` zu `.env` und trage deine Zugangsdaten ein:

`.env` befüllen:
```
QDRANT_ENDPOINT=https://deine-url.qdrant.io
QDRANT_API_KEY=dein_api_key
QDRANT_COLLECTION_NAME=fhdw_studienberater
```

## Verwendung

**Schritt 1 — Dokumente einlesen**

FHDW-PDFs in `data/raw/pdf/` ablegen, dann:
```bash
python scripts/ingest.py
```

**Schritt 2 — Pipeline testen**
```bash
python scripts/test_retrieval.py
```