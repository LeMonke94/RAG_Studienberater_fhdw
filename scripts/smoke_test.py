from rag_studienberater.bootstrap.container import create_container

def main() -> None:
    container = create_container()
    container.ingest_use_case.execute_folder('data/raw/pdf')

    fragen = [
        "Welche KI-Tools sind an der FHDW erlaubt?",
        "Was passiert bei einem Verstoß gegen die KI-Richtlinien?",
        "Was ist die Hauptstadt von Frankreich?",  # Guardrail Test
    ]

    for frage in fragen:
        print(f"\n{'='*50}")
        print(f"FRAGE: {frage}")
        print('='*50)
        answer = container.answer_use_case.execute(frage)
        print(f"ANTWORT: {answer.text}")
        if answer.has_evidence:
            print(f"\nQUELLEN:")
            for chunk in answer.sources:
                print(f'   - {chunk.source}, Seite {chunk.page}')

if __name__ == '__main__':
    main()