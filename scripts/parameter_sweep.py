"""
Parameter-Sweep

Testet automatisch verschiedene Konfigurationen und vergleicht die Ergebnisse.
Jede Konfiguration: Qdrant leeren → Ingest → Evaluate.

HINWEIS: Ein Durchlauf dauert ~10-20 Minuten (Ingest + 35 Fragen).
         Bei 3 Konfigurationen = ~30-60 Minuten Gesamtlaufzeit.

Verwendung:
    py scripts/parameter_sweep.py
    py scripts/parameter_sweep.py --testset data/evaluation/testset.json
"""

# Imports
import json
import sys
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

# Reuse evaluation logic from evaluate.py
sys.path.insert(0, str(Path(__file__).parent))
from evaluate import (
    EvaluationsBericht,
    FrageErgebnis,
    berechne_bericht_metriken,
    drucke_zusammenfassung,
    lade_testset,
    score_ergebnis,
    symbol,
)


# Configs to compare
@dataclass
class Configuration:
    name: str
    chunk_size: int
    chunk_overlap: int
    top_k: int


CONFIGURATIONS = [
    Configuration(name='small_chunks',  chunk_size=256,  chunk_overlap=30,  top_k=5),
    Configuration(name='medium_chunks', chunk_size=512,  chunk_overlap=50,  top_k=5),
    Configuration(name='large_chunks',  chunk_size=1024, chunk_overlap=100, top_k=5),
]


# Sweep logic
def run_sweep(testset_path: str, pdf_folder: str, url_json: str, output_dir: str) -> None:
    print(f"\n{'═' * 80}")
    print('  PARAMETER-SWEEP — RAG-STUDIENBERATER')
    print(f"{'═' * 80}")
    print(f'  {len(CONFIGURATIONS)} Konfigurationen × 35 Fragen')
    print(f'  Geschätzte Laufzeit: {len(CONFIGURATIONS) * 15}–{len(CONFIGURATIONS) * 20} Minuten\n')

    results: list[tuple[Configuration, str, EvaluationsBericht]] = []

    for i, config in enumerate(CONFIGURATIONS, start=1):
        print(f"\n{'─' * 80}")
        print(f'  [{i}/{len(CONFIGURATIONS)}] Konfiguration: {config.name}')
        print(f'       chunk_size={config.chunk_size}  chunk_overlap={config.chunk_overlap}  top_k={config.top_k}')
        print(f"{'─' * 80}\n")

        start = time.perf_counter()

        # Initialise container with this config
        try:
            container = _create_container(config)
        except Exception as e:
            print(f'  FEHLER beim Initialisieren: {e}')
            print('  Stelle sicher, dass Ollama und Qdrant laufen.\n')
            sys.exit(1)

        # Empty vector store
        print('  Leere Vector Store...')
        try:
            container.retrieval_use_case.retrieval_service.vector_store.clear()
            print('  Vector Store geleert.')
        except Exception as e:
            print(f'  WARNUNG: Leeren fehlgeschlagen: {e}')

        # Ingest
        print(f"\n  Ingest PDFs aus '{pdf_folder}'...")
        try:
            container.ingest_use_case.execute_folder(pdf_folder)
        except Exception as e:
            print(f'  WARNUNG: PDF-Ingest fehlgeschlagen: {e}')

        print(f"  Ingest URLs aus '{url_json}'...")
        try:
            container.ingest_use_case.execute_urls_from_file(url_json)
        except Exception as e:
            print(f'  WARNUNG: URL-Ingest fehlgeschlagen: {e}')

        # Evaluation
        print(f'\n  Starte Evaluation ({testset_path})...')
        path, report = _run_evaluation(container, testset_path, output_dir, config)
        results.append((config, path, report))

        duration = time.perf_counter() - start
        print(f"\n  Konfiguration '{config.name}' abgeschlossen in {duration/60:.1f} Minuten.")
        print(f'  Ergebnis: {path}')

    # Comparison table
    _print_comparison(results)


def _create_container(config: Configuration):
    """Creates a container with overridden chunking parameters."""
    import os
    os.environ['CHUNKING__CHUNK_SIZE']    = str(config.chunk_size)
    os.environ['CHUNKING__CHUNK_OVERLAP'] = str(config.chunk_overlap)
    os.environ['CHUNKING__TOP_K']         = str(config.top_k)

    # Clear settings cache so new env values are picked up
    from rag_studienberater.config.settings import get_settings
    get_settings.cache_clear()

    from rag_studienberater.bootstrap.container import create_container
    return create_container()


def _run_evaluation(
    container, testset_path: str, output_dir: str, config: Configuration
) -> tuple[str, EvaluationsBericht]:
    """Runs evaluation for one configuration and returns (file_path, report)."""
    questions = lade_testset(testset_path)
    report = EvaluationsBericht(
        zeitstempel=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        testset_pfad=testset_path,
    )

    for i, question_data in enumerate(questions, start=1):
        question_text    = question_data['frage']
        ergebnis = FrageErgebnis(
            id=question_data.get('id', f'Q{i:02d}'),
            kategorie=question_data.get('kategorie', 'unbekannt'),
            frage=question_text,
            erwartet_antwort=question_data.get('erwartet_antwort', True),
        )

        print(f'  [{i:02d}/{len(questions)}] {question_text[:70]}', end='', flush=True)

        try:
            t0 = time.perf_counter()
            answer = container.answer_use_case.execute(question_text)
            ergebnis.laufzeit_sek = time.perf_counter() - t0
            ergebnis.hat_antwort  = answer.has_evidence
            ergebnis.antwort_text = answer.text
            ergebnis.quellen      = list({
                f'{chunk.source} S.{chunk.page}' if chunk.page else chunk.source
                for chunk in answer.sources
            })
        except Exception as exc:
            ergebnis.antwort_text = f'[FEHLER: {exc}]'

        score_ergebnis(ergebnis, question_data)
        print(f'  {symbol(ergebnis.guardrail_korrekt)}  ({ergebnis.laufzeit_sek:.1f}s)')
        report.ergebnisse.append(ergebnis)

    berechne_bericht_metriken(report)
    drucke_zusammenfassung(report)

    # Save with config name so files are easy to identify
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = str(Path(output_dir) / f'sweep_{config.name}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(asdict(report), f, ensure_ascii=False, indent=2)

    return path, report


def _print_comparison(results: list[tuple[Configuration, str, EvaluationsBericht]]) -> None:
    """Prints a comparison table of all configurations."""
    print(f"\n\n{'═' * 80}")
    print('  VERGLEICH ALLER KONFIGURATIONEN')
    print(f"{'═' * 80}\n")

    col = 18
    print(f"  {'Konfiguration':<{col}} {'Chunk':>6} {'Overlap':>8} {'Top-K':>6} "
          f"{'Guardrail':>10} {'Quellen':>8} {'Keywords':>9} {'Ø Zeit':>7}")
    print(f"  {'─'*col} {'─'*6} {'─'*8} {'─'*6} {'─'*10} {'─'*8} {'─'*9} {'─'*7}")

    for config, path, report in results:
        print(
            f'  {config.name:<{col}} '
            f'{config.chunk_size:>6} '
            f'{config.chunk_overlap:>8} '
            f'{config.top_k:>6} '
            f'{report.guardrail_korrektheit:>9.0%} '
            f'{report.quellenangabe_quote:>7.0%} '
            f'{report.durchschnittlicher_keyword_recall:>8.0%} '
            f'{report.durchschnittliche_laufzeit_sek:>6.1f}s'
        )

    print(f'\n  Ergebnisdateien:')
    for _, path, _ in results:
        print(f'    {path}')
    print(f"\n{'═' * 80}\n")

# Entry point
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parameter-Sweep für den RAG-Studienberater')
    parser.add_argument('--testset',    default='data/evaluation/testset.json')
    parser.add_argument('--pdf-folder', default='data/raw/pdf')
    parser.add_argument('--url-json',   default='data/raw/web/url.json')
    parser.add_argument('--output',     default='data/evaluation')
    args = parser.parse_args()

    run_sweep(
        testset_path=args.testset,
        pdf_folder=args.pdf_folder,
        url_json=args.url_json,
        output_dir=args.output,
    )