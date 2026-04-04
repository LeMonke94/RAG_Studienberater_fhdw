"""
Evaluations-Skript für den RAG-Studienberater.

Lädt das Testset, schickt jede Frage durch die vollständige Pipeline
und bewertet die Antwortqualität anhand messbarer Kriterien.

Verwendung:
    py scripts/evaluate.py
    py scripts/evaluate.py --testset data/evaluation/testset.json
    py scripts/evaluate.py --skip-ingest   # wenn Dokumente bereits geladen sind
"""

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Datenmodell für Ergebnisse
# ---------------------------------------------------------------------------

@dataclass
class FrageErgebnis:
    id: str
    kategorie: str
    frage: str
    erwartet_antwort: bool

    # System-Output
    hat_antwort: bool = False
    antwort_text: str = ""
    quellen: list[str] = field(default_factory=list)
    laufzeit_sek: float = 0.0

    # Automatische Metriken
    guardrail_korrekt: bool = False      # System verhält sich wie erwartet (Antwort / Kein-Antwort)
    hat_quellen: bool = False            # Antwort enthält Quellenangaben
    keyword_recall: float = 0.0         # Anteil gefundener Schlüsselwörter (0.0–1.0)

    # Manuell bewertbar (nach Durchlauf ausfüllen)
    korrektheit: int = -1               # 0=falsch, 1=teilweise, 2=korrekt  (-1 = nicht bewertet)
    vollständigkeit: int = -1           # 0=unvollständig, 1=teilweise, 2=vollständig
    anmerkung: str = ""


@dataclass
class EvaluationsBericht:
    zeitstempel: str
    testset_pfad: str
    gesamt: int = 0
    guardrail_korrektheit: float = 0.0
    quellenangabe_quote: float = 0.0
    durchschnittlicher_keyword_recall: float = 0.0
    durchschnittliche_laufzeit_sek: float = 0.0
    ergebnisse: list[FrageErgebnis] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def berechne_keyword_recall(antwort_text: str, schlüsselwörter: list[str]) -> float:
    """Anteil der Schlüsselwörter, die in der Antwort vorkommen (case-insensitive)."""
    if not schlüsselwörter:
        return 1.0  # Keine Erwartung = volle Punktzahl

    antwort_lower = antwort_text.lower()
    treffer = sum(1 for kw in schlüsselwörter if kw.lower() in antwort_lower)
    return treffer / len(schlüsselwörter)


def score_ergebnis(ergebnis: FrageErgebnis, frage_data: dict) -> None:
    """Berechnet alle automatischen Metriken und schreibt sie ins Ergebnis."""
    ergebnis.guardrail_korrekt = ergebnis.hat_antwort == ergebnis.erwartet_antwort
    ergebnis.hat_quellen = ergebnis.hat_antwort and len(ergebnis.quellen) > 0
    ergebnis.keyword_recall = berechne_keyword_recall(
        ergebnis.antwort_text,
        frage_data.get("schlüsselwörter", [])
    )


# ---------------------------------------------------------------------------
# Report-Ausgabe
# ---------------------------------------------------------------------------

TRENNLINIE = "─" * 80

def symbol(wert: bool) -> str:
    return "✓" if wert else "✗"


def recall_balken(recall: float, breite: int = 10) -> str:
    gefüllt = round(recall * breite)
    return f"[{'█' * gefüllt}{'░' * (breite - gefüllt)}] {recall:.0%}"


def drucke_ergebnisse(ergebnisse: list[FrageErgebnis]) -> None:
    print(f"\n{TRENNLINIE}")
    print("  EINZELERGEBNISSE")
    print(TRENNLINIE)

    for e in ergebnisse:
        guardrail_sym = symbol(e.guardrail_korrekt)
        quellen_sym   = symbol(e.hat_quellen) if e.hat_antwort else " –"
        recall_str    = recall_balken(e.keyword_recall) if e.erwartet_antwort else "   (off-topic)"

        print(f"\n  [{e.id}] {e.frage[:65]}")
        print(f"       Kategorie : {e.kategorie}")
        print(f"       Guardrail : {guardrail_sym}  (erwartet={'Antwort' if e.erwartet_antwort else 'Keine Antwort'}, "
              f"erhalten={'Antwort' if e.hat_antwort else 'Keine Antwort'})")

        if e.hat_antwort:
            print(f"       Quellen   : {quellen_sym}  ({len(e.quellen)} Quelle(n): {', '.join(e.quellen[:2])}{'...' if len(e.quellen) > 2 else ''})")
            print(f"       Keywords  : {recall_str}")
            print(f"       Antwort   : {e.antwort_text[:120]}{'...' if len(e.antwort_text) > 120 else ''}")
        else:
            print(f"       Antwort   : [Guardrail ausgelöst]")

        print(f"       Zeit      : {e.laufzeit_sek:.2f}s")


def drucke_zusammenfassung(bericht: EvaluationsBericht) -> None:
    print(f"\n{TRENNLINIE}")
    print("  ZUSAMMENFASSUNG")
    print(TRENNLINIE)

    print(f"\n  Gesamt-Fragen         : {bericht.gesamt}")
    print(f"  Guardrail-Korrektheit : {bericht.guardrail_korrektheit:.0%}  "
          f"({round(bericht.guardrail_korrektheit * bericht.gesamt)}/{bericht.gesamt} korrekt)")
    print(f"  Quellenangabe-Quote   : {bericht.quellenangabe_quote:.0%}  "
          f"(bei beantworteten Fragen)")
    print(f"  Ø Keyword-Recall      : {bericht.durchschnittlicher_keyword_recall:.0%}")
    print(f"  Ø Laufzeit            : {bericht.durchschnittliche_laufzeit_sek:.2f}s pro Frage")

    # Aufschlüsselung nach Kategorie
    kategorien: dict[str, list[FrageErgebnis]] = {}
    for e in bericht.ergebnisse:
        kategorien.setdefault(e.kategorie, []).append(e)

    print(f"\n  {'Kategorie':<22} {'Fragen':>6}  {'Guardrail':>10}  {'Quellen':>8}  {'Keywords':>10}")
    print(f"  {'─'*22} {'─'*6}  {'─'*10}  {'─'*8}  {'─'*10}")

    for kat, einträge in sorted(kategorien.items()):
        n = len(einträge)
        gc = sum(1 for e in einträge if e.guardrail_korrekt) / n
        qc = sum(1 for e in einträge if e.hat_quellen) / max(1, sum(1 for e in einträge if e.hat_antwort))
        kr = sum(e.keyword_recall for e in einträge) / n
        print(f"  {kat:<22} {n:>6}  {gc:>9.0%}  {qc:>7.0%}  {kr:>9.0%}")

    print()

    # Hinweis auf manuelle Bewertung
    print("  HINWEIS: Korrektheit und Vollständigkeit müssen manuell bewertet werden.")
    print("  Fülle die Felder 'korrektheit' und 'vollständigkeit' in der Ergebnisdatei aus:")
    print("    0 = falsch/unvollständig  |  1 = teilweise  |  2 = korrekt/vollständig")
    print()


# ---------------------------------------------------------------------------
# Hauptlogik
# ---------------------------------------------------------------------------

def lade_testset(pfad: str) -> list[dict]:
    with open(pfad, encoding="utf-8") as f:
        data = json.load(f)
    fragen = data.get("fragen", data) if isinstance(data, dict) else data
    print(f"  Testset geladen: {len(fragen)} Fragen aus '{pfad}'")
    return fragen


def speichere_bericht(bericht: EvaluationsBericht, ausgabe_dir: str) -> str:
    Path(ausgabe_dir).mkdir(parents=True, exist_ok=True)
    zeitstempel = bericht.zeitstempel.replace(":", "-").replace(" ", "_")
    dateiname = f"results_{zeitstempel}.json"
    pfad = str(Path(ausgabe_dir) / dateiname)

    # dataclass → dict (rekursiv)
    def zu_dict(obj):
        if isinstance(obj, list):
            return [zu_dict(i) for i in obj]
        if hasattr(obj, "__dataclass_fields__"):
            return {k: zu_dict(v) for k, v in asdict(obj).items()}
        return obj

    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(zu_dict(bericht), f, ensure_ascii=False, indent=2)

    return pfad


def berechne_bericht_metriken(bericht: EvaluationsBericht) -> None:
    """Aggregierte Metriken in den Bericht schreiben."""
    n = len(bericht.ergebnisse)
    if n == 0:
        return

    bericht.gesamt = n
    bericht.guardrail_korrektheit = sum(
        1 for e in bericht.ergebnisse if e.guardrail_korrekt
    ) / n

    beantwortete = [e for e in bericht.ergebnisse if e.hat_antwort]
    bericht.quellenangabe_quote = (
        sum(1 for e in beantwortete if e.hat_quellen) / len(beantwortete)
        if beantwortete else 0.0
    )

    bericht.durchschnittlicher_keyword_recall = (
        sum(e.keyword_recall for e in bericht.ergebnisse) / n
    )
    bericht.durchschnittliche_laufzeit_sek = (
        sum(e.laufzeit_sek for e in bericht.ergebnisse) / n
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG-Studienberater Evaluation")
    parser.add_argument(
        "--testset",
        default="data/evaluation/testset.json",
        help="Pfad zur Testset-JSON-Datei",
    )
    parser.add_argument(
        "--output",
        default="data/evaluation",
        help="Ausgabeverzeichnis für den Ergebnisbericht",
    )
    parser.add_argument(
        "--skip-ingest",
        action="store_true",
        help="Dokumente nicht erneut einlesen (Vector Store bereits befüllt)",
    )
    parser.add_argument(
        "--ingest-folder",
        default="data/raw/pdf",
        help="Ordner mit PDFs für den Ingest (Standard: data/raw/pdf)",
    )
    args = parser.parse_args()

    print(f"\n{'═' * 80}")
    print("  RAG-STUDIENBERATER — EVALUATION")
    print(f"{'═' * 80}")

    # Container initialisieren
    print("\n  Initialisiere Pipeline...")
    try:
        from rag_studienberater.bootstrap.container import create_container
        container = create_container()
    except Exception as exc:
        print(f"\n  FEHLER beim Initialisieren: {exc}")
        print("  Stelle sicher, dass Ollama läuft und .env korrekt konfiguriert ist.")
        sys.exit(1)

    # Ingest
    if not args.skip_ingest:
        print(f"  Lese Dokumente aus '{args.ingest_folder}' ein...")
        try:
            container.ingest_use_case.execute_folder(args.ingest_folder)
            print("  Ingest abgeschlossen.")
        except Exception as exc:
            print(f"\n  WARNUNG: Ingest fehlgeschlagen: {exc}")
            print("  Fahre fort mit bestehendem Vector-Store-Inhalt.")
    else:
        print("  Ingest übersprungen (--skip-ingest).")

    # Testset laden
    print()
    fragen = lade_testset(args.testset)

    # Evaluation durchführen
    bericht = EvaluationsBericht(
        zeitstempel=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        testset_pfad=args.testset,
    )

    print(f"\n  Starte Evaluation ({len(fragen)} Fragen)...\n")

    for i, frage_data in enumerate(fragen, start=1):
        frage_id = frage_data.get("id", f"Q{i:02d}")
        frage_text = frage_data["frage"]
        kategorie = frage_data.get("kategorie", "unbekannt")
        erwartet_antwort = frage_data.get("erwartet_antwort", True)

        print(f"  [{i:02d}/{len(fragen)}] {frage_text[:70]}", end="", flush=True)

        ergebnis = FrageErgebnis(
            id=frage_id,
            kategorie=kategorie,
            frage=frage_text,
            erwartet_antwort=erwartet_antwort,
        )

        try:
            start = time.perf_counter()
            answer = container.answer_use_case.execute(frage_text)
            ergebnis.laufzeit_sek = time.perf_counter() - start

            ergebnis.hat_antwort = answer.has_evidence
            ergebnis.antwort_text = answer.text
            ergebnis.quellen = list({
                f"{chunk.source} S.{chunk.page}" if chunk.page else chunk.source
                for chunk in answer.sources
            })

        except Exception as exc:
            ergebnis.laufzeit_sek = 0.0
            ergebnis.antwort_text = f"[FEHLER: {exc}]"

        score_ergebnis(ergebnis, frage_data)

        status = symbol(ergebnis.guardrail_korrekt)
        print(f"  {status}  ({ergebnis.laufzeit_sek:.1f}s)")

        bericht.ergebnisse.append(ergebnis)

    # Metriken berechnen und ausgeben
    berechne_bericht_metriken(bericht)
    drucke_ergebnisse(bericht.ergebnisse)
    drucke_zusammenfassung(bericht)

    # Bericht speichern
    ergebnis_pfad = speichere_bericht(bericht, args.output)
    print(f"  Ergebnisse gespeichert: {ergebnis_pfad}")
    print(f"{'═' * 80}\n")


if __name__ == "__main__":
    main()
