# SpaCy NLP Processing Project

This project demonstrates how to use spaCy for natural language processing tasks including named entity recognition and simple relation extraction from text files.

## Features

- Named Entity Recognition (NER)
- Simple Subject-Verb-Object relation extraction
- Modular code structure with error handling
- Type hints for better code quality

## Prerequisites

- Python 3.12
- spaCy library
- English language model (en_core_web_sm)

## Installation

1. Ensure Python 3.12 is installed and configured.

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the spaCy English model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

1. Place your text content in `data.txt` file.

2. Run the script:
   ```bash
   python main.py
   ```

3. View the results in `output.txt`.

## Example

With the provided `data.txt` containing:
```
Apple Inc. is a technology company founded by Steve Jobs in Cupertino, California. It develops products like the iPhone and iPad.
```

The output will include extracted entities like "Apple Inc." (ORG), "Steve Jobs" (PERSON), etc., and relations like "Apple -> develops -> products".

## Project Structure

- `main.py`: Main script for NLP processing
- `data.txt`: Input text file
- `requirements.txt`: Python dependencies
- `README.md`: This documentation
   ```
   python main.py
   ```
3. 查看 `output.txt` 文件中的提取结果。

## 输出格式

- **Entities**: 列出识别的实体及其类型（如 PERSON, ORG）。
- **Relations**: 基于依存分析的简单主语-动词-宾语关系。