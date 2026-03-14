"""
SpaCy Natural Language Processing Demo

This script demonstrates entity extraction and simple relation extraction
using spaCy on text from data.txt.
"""

import spacy
from pathlib import Path
from typing import List, Tuple


def load_model(model_name: str = "en_core_web_sm") -> spacy.Language:
    """Load the spaCy model."""
    try:
        return spacy.load(model_name)
    except OSError:
        print(f"Model '{model_name}' not found. Please install it with:")
        print(f"python -m spacy download {model_name}")
        raise


def read_text_file(file_path: Path) -> str:
    """Read text from a file."""
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{file_path}' not found.")


def extract_entities(doc: spacy.tokens.Doc) -> List[Tuple[str, str]]:
    """Extract named entities from the document."""
    return [(ent.text, ent.label_) for ent in doc.ents]


def extract_relations(doc: spacy.tokens.Doc) -> List[Tuple[str, str, str]]:
    """Extract simple subject-verb-object relations."""
    relations = []
    for token in doc:
        if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            subject = token.text
            verb = token.head.text
            # Find object
            for child in token.head.children:
                if child.dep_ in ("dobj", "pobj"):
                    obj = child.text
                    relations.append((subject, verb, obj))
                    break
    return relations


def write_results(output_path: Path, entities: List[Tuple[str, str]], relations: List[Tuple[str, str, str]]) -> None:
    """Write extracted entities and relations to a file."""
    with output_path.open("w", encoding="utf-8") as f:
        f.write("Named Entities:\n")
        for ent_text, ent_label in entities:
            f.write(f"- {ent_text} ({ent_label})\n")

        f.write("\nRelations (Subject-Verb-Object):\n")
        for subj, verb, obj in relations:
            f.write(f"- {subj} -> {verb} -> {obj}\n")


def main():
    """Main function to run the NLP processing."""
    # File paths
    input_file = Path("data.txt")
    output_file = Path("output.txt")

    # Load model
    nlp = load_model()

    # Read text
    text = read_text_file(input_file)

    # Process text
    doc = nlp(text)

    # Extract information
    entities = extract_entities(doc)
    relations = extract_relations(doc)

    # Write results
    write_results(output_file, entities, relations)

    print(f"Entities and relations extracted and saved to {output_file}")


if __name__ == "__main__":
    main()