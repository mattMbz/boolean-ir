# Boolean IR

A lightweight [Boolean Information Retrieval](https://en.wikipedia.org/wiki/Boolean_model_of_information_retrieval) engine for Python.

`boolean-ri` provides a small, deterministic search engine based on an in-memory [inverted index](https://en.wikipedia.org/wiki/Inverted_index). It indexes plain text documents and evaluates Boolean queries with `AND`, `OR`, `NOT`, and parentheses.

The project is intentionally focused on classic Boolean Information Retrieval: simple text processing, predictable results, and a clean Python API that can be embedded in backend services, scripts, teaching material, or small document search tools.

---

## Features

- In-memory inverted index
- Boolean query parsing with Lark
- Query operators:
  - `AND`
  - `OR`
  - `NOT`
  - parentheses `(...)`
- Deterministic sorted results
- Text normalization:
  - lowercase conversion
  - accent removal
- Simple tokenization
- Optional stopword filtering
- Optional stemming with NLTK Snowball stemmers
- Built-in language configuration for:
  - Spanish
  - English
  - Portuguese
- Document insertion and removal
- `.txt` directory loader
- Framework-agnostic public API

---

## Project Scope

This library is strictly a Boolean IR engine.

It does not implement:

- TF-IDF
- BM25
- vector databases
- embeddings
- semantic search
- machine learning models
- ranking or scoring
- OCR
- PDF, DOCX, or HTML parsing
- a REST API server

The goal is to keep the core retrieval model transparent, easy to test, and easy to extend without mixing it with ranking or semantic retrieval techniques.

---

## Installation

### With Poetry

```bash
poetry add boolean-ri
```

### Local Development

```bash
git clone <repository-url>
cd boolean-ri
poetry install
```

Requirements:

- Python `>=3.10`
- Poetry
- `lark`
- `nltk`
- `pytest` for development

---

## Quick Start

```python
from boolean_ir import BooleanEngine

engine = BooleanEngine()

engine.add_documents({
    "doc1": "python fastapi backend",
    "doc2": "django orm templates",
    "doc3": "python boolean search engine",
})

results = engine.search("python AND NOT django")
print(results)
```

Output:

```python
["doc1", "doc3"]
```

---

## Public API

The main public interface is `BooleanEngine`.

```python
from boolean_ir import BooleanEngine

engine = BooleanEngine()

engine.add_document("doc1", "python fastapi backend")
engine.add_documents({
    "doc2": "django orm templates",
    "doc3": "python search engine",
})

results = engine.search("python AND backend")
engine.remove_document("doc2")
```

### Methods

```python
add_document(doc_id: str, content: str)
```

Adds one document to the inverted index.

```python
add_documents(docs: dict[str, str])
```

Adds multiple documents from a dictionary where keys are document IDs and values are text contents.

```python
remove_document(doc_id: str)
```

Removes a document from the index and from the engine document set.

```python
search(query: str) -> list[str]
```

Evaluates a Boolean query and returns a sorted list of matching document IDs.

---

## Query Syntax

Supported examples:

```text
python
python AND fastapi
python OR django
NOT python
python AND NOT django
python AND (fastapi OR django)
(error AND nginx) OR (database AND NOT mysql)
```

Invalid examples:

```text
AND python
python OR
python AND AND django
python (
)
```

Invalid queries raise `InvalidQueryError`.

### Operator Precedence

The parser uses the following precedence:

1. Parentheses
2. `NOT`
3. `AND`
4. `OR`

Example:

```python
engine.search("python OR fastapi AND django")
```

Is interpreted as:

```text
python OR (fastapi AND django)
```

### Operators Are Uppercase

Boolean operators are expected as uppercase keywords:

```text
AND OR NOT
```

Terms are case-insensitive. For example, `PYTHON`, `Python`, and `python` match the same normalized term.

---

## Text Processing

The indexing and query pipeline supports normalization, stopword filtering, and stemming.

### Normalization

Normalization is always applied to documents and query terms:

- text is lowercased for indexed terms
- accents are removed

Example:

```python
engine = BooleanEngine()
engine.add_document("doc1", "configuración avanzada")

print(engine.search("configuracion"))
```

Output:

```python
["doc1"]
```

### Stopwords

Stopword filtering is optional and disabled by default.

```python
engine = BooleanEngine(stopwords=True)
engine.add_document("doc1", "error en servidor nginx")

print(engine.search("en"))
print(engine.search("servidor"))
```

Output:

```python
[]
["doc1"]
```

### Stemming

Stemming is optional and disabled by default.

```python
engine = BooleanEngine(stemming=True)
engine.add_document("doc1", "errores en servidores nginx")

print(engine.search("error AND servidor"))
```

Output:

```python
["doc1"]
```

The constructor also supports the `Stemming` alias:

```python
engine = BooleanEngine(stopwords=True, Stemming=True)
```

---

## Language Support

`boolean-ri` supports Boolean IR text processing for Spanish, English, and Portuguese.

The default language is Spanish:

```python
engine = BooleanEngine()
```

Explicit language configuration:

```python
spanish_engine = BooleanEngine(
    stopwords=True,
    Stemming=True,
    language="spanish",
)

portuguese_engine = BooleanEngine(
    stopwords=True,
    Stemming=False,
    language="portuguese",
)

english_engine = BooleanEngine(
    stopwords=False,
    Stemming=False,
    language="english",
)
```

Supported language values:

```text
spanish
english
portuguese
```

Unsupported languages raise `UnsupportedLanguageError`.

Stopword lists live in:

```text
boolean_ir/text_processor/stop_words/
```

To add another language, add a new stopword module in that package and register it in `LANG_CONFIG`.

---

## Loading `.txt` Documents

The package includes a small helper to load all `.txt` files from a directory.

```python
from boolean_ir import BooleanEngine, load_txt_directory

docs = load_txt_directory("./documents")

engine = BooleanEngine(stopwords=True, stemming=True, language="english")
engine.add_documents(docs)

results = engine.search("server AND error")
print(results)
```

`load_txt_directory()` returns a dictionary:

```python
{
    "file1.txt": "file content",
    "file2.txt": "another file content",
}
```

---

## Examples

### Spanish

```python
from boolean_ir import BooleanEngine

engine = BooleanEngine(stopwords=True, Stemming=True, language="spanish")

engine.add_documents({
    "D1": "Errores en servidores nginx y configuración de bases de datos",
    "D2": "Documentación de FastAPI para servicios backend",
})

print(engine.search("error AND servidor"))
```

Output:

```python
["D1"]
```

### English

```python
from boolean_ir import BooleanEngine

engine = BooleanEngine(stopwords=True, stemming=True, language="english")

engine.add_documents({
    "D1": "running servers in production",
    "D2": "database migrations and backend services",
})

print(engine.search("run AND server"))
```

Output:

```python
["D1"]
```

### Portuguese

```python
from boolean_ir import BooleanEngine

engine = BooleanEngine(stopwords=True, stemming=True, language="portuguese")

engine.add_documents({
    "D1": "servidores em producao",
    "D2": "configuracao de banco de dados",
})

print(engine.search("servidor"))
```

Output:

```python
["D1"]
```

---

## Architecture

The library follows a small modular design:

```text
BooleanEngine
    ↓
InvertedIndex
    ↓
Tokenizer
    ↓
Normalizer + TextProcessor

BooleanEngine.search()
    ↓
BooleanParser
    ↓
   AST
    ↓
TextProcessor for query terms
    ↓
BooleanEvaluator
    ↓
InvertedIndex
    ↓
sorted list[str]
```

### Main Modules

```text
boolean_ir/
├── engine.py
├── evaluator.py
├── exceptions.py
├── index.py
├── normalizer.py
├── parser.py
├── tokenizer.py
├── types.py
├── loaders/
│   └── txt_loader.py
└── text_processor/
    ├── normalizer.py
    ├── textProcessor.py
    └── stop_words/
        ├── english.py
        ├── portuguese.py
        └── spanish.py
```

Responsibilities:

- `engine.py`: public facade and orchestration
- `index.py`: in-memory inverted index
- `tokenizer.py`: token extraction
- `parser.py`: Boolean grammar and AST generation
- `evaluator.py`: Boolean set evaluation
- `text_processor/normalizer.py`: deterministic text normalization
- `text_processor/textProcessor.py`: stopword filtering and stemming
- `text_processor/stop_words/`: local stopword lists by language
- `loaders/txt_loader.py`: `.txt` directory loading

---

## Development

Install dependencies:

```bash
poetry install
```

Run tests:

```bash
poetry run pytest -q
```

Run focused test suites:

```bash
poetry run pytest -q tests/test_parser.py
poetry run pytest -q tests/test_engine.py
```

The test suite covers:

- Boolean parser behavior
- AST shape
- invalid query handling
- indexing and document removal
- normalized search
- stopwords and stemming
- Spanish, English, and Portuguese text processing

Tests should not require network access or external NLTK corpus downloads. Stopwords are stored locally in the repository, while NLTK is used for Snowball stemming.

---

## Design Principles

This project prioritizes:

- clarity
- deterministic behavior
- simple public API
- low coupling
- small modules
- explicit Boolean IR semantics
- easy testing

The implementation intentionally avoids over-engineering. If a feature belongs to ranking, semantic retrieval, vector search, or machine learning, it should live outside this package.

---

## License

No license has been specified yet.

---

## Author

Matias Barboza, AI Engineer

Social links:

- LinkedIn:
- GitHub:
- X:
- Website:
