"""
SpaCy Knowledge Graph Construction and LLM Integration System

This system:
1. Extracts entities and relations from data.txt and question.txt using SpaCy
2. Creates knowledge bases (dataKB.txt, questionKB.txt)
3. Filters relevant knowledge based on question (preKG.txt)
4. Builds knowledge graph
5. Calls DeepSeek LLM API to generate answers (answer.txt)

Language Support:
- English (default): en_core_web_sm model
- Chinese: zh_core_web_sm model (configurable via .env)
"""

import spacy
from pathlib import Path
from typing import List, Tuple, Dict, Set
import json
import os
from dotenv import load_dotenv
import requests


# Load environment variables
load_dotenv()


def load_model(model_name: str = None) -> spacy.Language:
    """Load the spaCy model for text processing."""
    # Get model name from environment variable or use default
    if model_name is None:
        model_name = os.getenv("SPACY_MODEL", "en_core_web_sm")  # Changed to English default
    
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


def extract_entities(doc: spacy.tokens.Doc) -> List[Dict]:
    """Extract named entities from the document."""
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        })
    return entities


def extract_relations(doc: spacy.tokens.Doc) -> List[Dict]:
    """Extract subject-verb-object relations from the document."""
    relations = []
    
    for token in doc:
        # Check for subject-verb relationship
        if token.dep_ in ("nsubj", "nsubjpass") and token.head.pos_ in ("VERB", "AUX"):
            subject = token.text
            verb = token.head.text
            
            # Find object
            for child in token.head.children:
                if child.dep_ in ("dobj", "pobj", "obj", "attr"):
                    obj = child.text
                    relations.append({
                        "subject": subject,
                        "verb": verb,
                        "object": obj,
                        "sentence": token.sent.text.strip()
                    })
                    break
        
        # Also check for prepositional relationships
        if token.dep_ == "prep":
            head_word = token.head.text
            prep = token.text
            for child in token.children:
                if child.dep_ in ("pobj", "obj"):
                    obj = child.text
                    relations.append({
                        "subject": head_word,
                        "verb": f"{prep}",
                        "object": obj,
                        "sentence": token.sent.text.strip()
                    })
                    break
    
    return relations


def create_knowledge_base(entities: List[Dict], relations: List[Dict], output_file: Path) -> Dict:
    """Create and save a knowledge base."""
    kb = {
        "entities": entities,
        "relations": relations,
        "entity_count": len(entities),
        "relation_count": len(relations)
    }
    
    with output_file.open("w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Knowledge Base: {output_file.name}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("=== Named Entities ===\n")
        unique_entities = {}
        for ent in entities:
            key = f"{ent['text']}_{ent['label']}"
            if key not in unique_entities:
                unique_entities[key] = ent
                f.write(f"- {ent['text']} ({ent['label']})\n")
        
        f.write(f"\nTotal unique entities: {len(unique_entities)}\n\n")
        
        f.write("=== Relations (Subject-Verb-Object) ===\n")
        for rel in relations:
            f.write(f"- {rel['subject']} -> {rel['verb']} -> {rel['object']}\n")
            f.write(f"  Context: {rel['sentence']}\n")
        
        f.write(f"\nTotal relations: {len(relations)}\n")
    
    return kb


def filter_relevant_knowledge(data_kb: Dict, question_kb: Dict) -> Dict:
    """Filter relevant knowledge from data KB based on question KB."""
    relevant_entities = []
    relevant_relations = []
    
    # Extract entity texts from question
    question_entity_texts = set()
    for ent in question_kb["entities"]:
        question_entity_texts.add(ent["text"].lower())
    
    # Filter entities that appear in question
    for ent in data_kb["entities"]:
        if ent["text"].lower() in question_entity_texts:
            relevant_entities.append(ent)
    
    # Also include entities related to question entities through relations
    relevant_entity_texts = {ent["text"].lower() for ent in relevant_entities}
    
    for rel in data_kb["relations"]:
        subj_match = rel["subject"].lower() in question_entity_texts
        obj_match = rel["object"].lower() in question_entity_texts
        
        if subj_match or obj_match:
            relevant_relations.append(rel)
            
            # Add connected entities
            if not subj_match:
                for ent in data_kb["entities"]:
                    if ent["text"] == rel["subject"]:
                        relevant_entities.append(ent)
                        relevant_entity_texts.add(ent["text"].lower())
                        break
            
            if not obj_match:
                for ent in data_kb["entities"]:
                    if ent["text"] == rel["object"]:
                        relevant_entities.append(ent)
                        relevant_entity_texts.add(ent["text"].lower())
                        break
    
    # Remove duplicates
    seen_entities = set()
    unique_entities = []
    for ent in relevant_entities:
        key = f"{ent['text']}_{ent['label']}"
        if key not in seen_entities:
            seen_entities.add(key)
            unique_entities.append(ent)
    
    filtered_kb = {
        "entities": unique_entities,
        "relations": relevant_relations,
        "entity_count": len(unique_entities),
        "relation_count": len(relevant_relations)
    }
    
    return filtered_kb


def build_knowledge_graph(filtered_kb: Dict, output_file: Path) -> Dict:
    """Build and save the knowledge graph with context information."""
    # Create graph structure with context
    graph = {
        "nodes": [],
        "edges": [],
        "metadata": {
            "node_count": filtered_kb["entity_count"],
            "edge_count": filtered_kb["relation_count"]
        }
    }
    
    # Add nodes (entities) with context
    node_map = {}
    for idx, ent in enumerate(filtered_kb["entities"]):
        node_id = f"n{idx}"
        node_map[ent["text"]] = node_id
        
        # Find context sentences where this entity appears
        context_sentences = []
        for rel in filtered_kb["relations"]:
            if rel["subject"] == ent["text"] or rel["object"] == ent["text"]:
                if "sentence" in rel and rel["sentence"]:
                    context_sentences.append(rel["sentence"])
        
        node_data = {
            "id": node_id,
            "label": ent["text"],
            "type": ent["label"],
            "context": list(set(context_sentences))  # Remove duplicates
        }
        graph["nodes"].append(node_data)
    
    # Add edges (relations) with context
    for rel in filtered_kb["relations"]:
        source = node_map.get(rel["subject"])
        target = node_map.get(rel["object"])
        
        if source and target:
            edge_data = {
                "source": source,
                "target": target,
                "relation": rel["verb"],
                "label": f"{rel['subject']} -> {rel['verb']} -> {rel['object']}",
                "context": rel.get("sentence", "")  # Include the sentence context
            }
            graph["edges"].append(edge_data)
    
    # Save knowledge graph with context
    with output_file.open("w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("PRELIMINARY KNOWLEDGE GRAPH (preKG)\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("=== Graph Statistics ===\n")
        f.write(f"Total Nodes (Entities): {graph['metadata']['node_count']}\n")
        f.write(f"Total Edges (Relations): {graph['metadata']['edge_count']}\n\n")
        
        f.write("=== Nodes (Entities) ===\n")
        for node in graph["nodes"]:
            f.write(f"[{node['id']}] {node['label']} (Type: {node['type']})\n")
            if node["context"]:
                f.write(f"  Context:\n")
                for ctx in node["context"]:
                    f.write(f"    - {ctx}\n")
        
        f.write("\n=== Edges (Relations) ===\n")
        for edge in graph["edges"]:
            f.write(f"{edge['source']} --[{edge['relation']}]--> {edge['target']}\n")
            f.write(f"  Label: {edge['label']}\n")
            if edge["context"]:
                f.write(f"  Context: {edge['context']}\n")
        
        f.write("\n=== JSON Format ===\n")
        f.write(json.dumps(graph, ensure_ascii=False, indent=2))
    
    return graph


def call_deepseek_api(kg_data: Dict, question_text: str) -> str:
    """Call DeepSeek LLM API with knowledge graph and question."""
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
    
    # Get answer language from environment variable
    answer_language = os.getenv("ANSWER_LANGUAGE", "chinese")
    language_instruction = "请用中文回答:" if answer_language == "chinese" else "Please answer in English:"
    
    # Prepare the prompt
    kg_json = json.dumps(kg_data, ensure_ascii=False, indent=2)
    
    if answer_language == "chinese":
        prompt = f"""基于以下知识图谱信息，回答后面的问题。请尽量详细、准确地回答。

知识图谱数据:
{kg_json}

问题:
{question_text}

{language_instruction}"""
    else:
        prompt = f"""Based on the following knowledge graph information, answer the question below. Please be as detailed and accurate as possible.

Knowledge Graph Data:
{kg_json}

Question:
{question_text}

{language_instruction}"""
    
    # Call DeepSeek API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        return answer
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling DeepSeek API: {e}")
        return f"[Error: Failed to get answer from LLM. Details: {str(e)}]"


def save_answer(answer: str, question: str, output_file: Path) -> None:
    """Save the generated answer to a file."""
    with output_file.open("w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("GENERATED ANSWER\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("Question:\n")
        f.write(f"{question}\n\n")
        
        f.write("-" * 60 + "\n")
        f.write("Answer:\n")
        f.write("-" * 60 + "\n")
        f.write(answer)
        f.write("\n")


def main():
    """Main function to run the complete pipeline."""
    print("=" * 60)
    print("SpaCy Knowledge Graph Construction & LLM Integration")
    print("=" * 60)
    
    # File paths configuration
    # Input files (from data&question directory)
    input_dir = Path("data&question")
    data_file = input_dir / "data.txt"
    question_file = input_dir / "question.txt"
    
    # Output files for knowledge bases (in data&question directory)
    data_kb_file = input_dir / "dataKB.txt"
    question_kb_file = input_dir / "questionKB.txt"
    pre_kg_file = input_dir / "preKG.txt"
    
    # Answer output (in answer directory)
    answer_dir = Path("answer")
    answer_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    answer_file = answer_dir / "answer.txt"
    
    # Step 1: Load model
    print("\n[Step 1/7] Loading SpaCy model...")
    nlp = load_model()
    print(f"✓ Model loaded successfully")
    
    # Step 2: Read input files
    print("\n[Step 2/7] Reading input files...")
    print(f"  Data file: {data_file}")
    print(f"  Question file: {question_file}")
    
    try:
        data_text = read_text_file(data_file)
        print(f"✓ Data file loaded: {len(data_text)} characters")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print(f"  Please ensure '{data_file}' exists")
        return
    
    try:
        question_text = read_text_file(question_file)
        print(f"✓ Question file loaded: {len(question_text)} characters")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print(f"  Please ensure '{question_file}' exists")
        return
    
    # Step 3: Process texts with SpaCy
    print("\n[Step 3/7] Processing texts with SpaCy...")
    data_doc = nlp(data_text)
    question_doc = nlp(question_text)
    print("✓ Text processing completed")
    
    # Step 4: Extract entities and relations
    print("\n[Step 4/7] Extracting entities and relations...")
    data_entities = extract_entities(data_doc)
    data_relations = extract_relations(data_doc)
    print(f"✓ Data: {len(data_entities)} entities, {len(data_relations)} relations")
    
    question_entities = extract_entities(question_doc)
    question_relations = extract_relations(question_doc)
    print(f"✓ Question: {len(question_entities)} entities, {len(question_relations)} relations")
    
    # Step 5: Create knowledge bases
    print("\n[Step 5/7] Creating knowledge bases...")
    data_kb = create_knowledge_base(data_entities, data_relations, data_kb_file)
    print(f"✓ Data KB saved to {data_kb_file.name}")
    
    question_kb = create_knowledge_base(question_entities, question_relations, question_kb_file)
    print(f"✓ Question KB saved to {question_kb_file.name}")
    
    # Step 6: Filter relevant knowledge and build graph
    print("\n[Step 6/7] Filtering knowledge and building graph...")
    filtered_kb = filter_relevant_knowledge(data_kb, question_kb)
    print(f"✓ Filtered: {filtered_kb['entity_count']} entities, {filtered_kb['relation_count']} relations")
    
    knowledge_graph = build_knowledge_graph(filtered_kb, pre_kg_file)
    print(f"✓ Knowledge graph saved to {pre_kg_file.name}")
    
    # Step 7: Call LLM to generate answer
    print("\n[Step 7/7] Calling DeepSeek LLM API...")
    
    # Check if API key is configured
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("⚠ Warning: DEEPSEEK_API_KEY not configured")
        print("  Please configure your API key in .env file")
        print("  Skipping LLM answer generation...")
        
        # Create placeholder answer file
        with answer_file.open("w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("ANSWER NOT GENERATED\n")
            f.write("=" * 60 + "\n\n")
            f.write("Reason: DEEPSEEK_API_KEY not configured\n\n")
            f.write("To generate answers:\n")
            f.write("1. Get your API key from: https://platform.deepseek.com/\n")
            f.write("2. Edit .env file and add your API key\n")
            f.write("3. Run main.py again\n\n")
            f.write("Question:\n")
            f.write(f"{question_text}\n")
    else:
        try:
            answer = call_deepseek_api(knowledge_graph, question_text)
            save_answer(answer, question_text, answer_file)
            print(f"✓ Answer generated and saved to {answer_file.name}")
        except Exception as e:
            print(f"✗ Error calling LLM: {e}")
            print("  Check your API key and network connection")
    
    # Summary
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Generated files:")
    print(f"  - {data_kb_file.name}: Data knowledge base")
    print(f"  - {question_kb_file.name}: Question knowledge base")
    print(f"  - {pre_kg_file.name}: Knowledge graph")
    print(f"  - {answer_file.name}: Generated answer")
    print("=" * 60)


if __name__ == "__main__":
    main()
