# AGENTS.md - Boolean IR Engine

## Project Goal

This project implements a lightweight Python library for classic Boolean Information Retrieval.

The current scope is strictly a Boolean engine with:

- In-memory inverted index.
- Text normalization.
- Simple tokenization.
- Boolean query parsing with Lark.
- Query evaluation with `AND`, `OR`, `NOT`, and parentheses.
- Main public API through `BooleanEngine`.

Do not include in this project:

- TF-IDF.
- BM25.
- Embeddings.
- Semantic ranking.
- Vector databases.
- Machine Learning models.

Those components must live in a separate library.

---

## Current Architecture

The main package is `boolean_ir`.

Expected structure:

```text
boolean_ir/
├── __init__.py
├── engine.py
├── evaluator.py
├── exceptions.py
├── index.py
├── normalizer.py
├── parser.py
├── tokenizer.py
└── types.py

main.py
tests/
```

Module responsibilities:

### `engine.py`

Contains the main `BooleanEngine` class.

It acts as the system facade and orchestrates:

- `Normalizer`
- `Tokenizer`
- `InvertedIndex`
- `BooleanParser`
- `BooleanEvaluator`

Responsibilities:

- Add documents.
- Add multiple documents.
- Remove documents.
- Execute Boolean searches.
- Maintain the `doc_ids` set.

It must not contain internal parsing, tokenization, or evaluation logic.

---

### `normalizer.py`

Contains `Normalizer`.

Responsibilities:

- Convert text to lowercase.
- Remove accents.
- Prepare text for tokenization.

Keep it simple and deterministic.

---

### `tokenizer.py`

Contains `Tokenizer`.

Responsibilities:

- Receive text.
- Normalize it using `Normalizer`.
- Extract tokens with a regular expression.

It currently uses:

```python
re.findall(r"\w+", text)
```

It must not know anything about inverted indexes, queries, or documents.

---

### `index.py`

Contains `InvertedIndex`.

Responsibilities:

- Build the inverted index.
- Associate tokens with document sets.
- Add documents to the index.
- Remove documents from the index.
- Search documents by term.

The current internal structure is:

```python
defaultdict(set)
```

Conceptual example:

```python
{
    "python": {"001", "003"},
    "fastapi": {"001"},
    "django": {"002"}
}
```

---

### `parser.py`

Contains:

- The Lark grammar.
- `_parser`.
- `_Transformer`.
- `BooleanParser`.

Responsibilities:

- Parse query strings.
- Convert the Lark tree into a simple tuple-based AST.
- Raise `InvalidQueryError` when the query is invalid.

Supported operators:

- `AND`
- `OR`
- `NOT`
- Parentheses

Current precedence:

1. Parentheses
2. `NOT`
3. `AND`
4. `OR`

Example:

```python
"python AND fastapi"
```

Expected AST:

```python
("AND", ("WORD", "python"), ("WORD", "fastapi"))
```

---

### `evaluator.py`

Contains `BooleanEvaluator`.

Responsibilities:

- Evaluate the AST.
- Resolve Boolean operations using sets.
- Query individual terms in `InvertedIndex`.

Rules:

```python
WORD -> index.get(term)
AND  -> intersection
OR   -> union
NOT  -> all_docs - result
```

It must not parse strings or tokenize documents.

---

### `exceptions.py`

Contains project-specific exceptions.

Current hierarchy:

```python
BooleanRIError
├── InvalidQueryError
└── UnsupportedLanguageError
```

Use custom exceptions when the error belongs to the library domain.

`InvalidQueryError` should provide a global parser-error message for malformed or inappropriate queries and include the specific parser cause when available.

---

### `types.py`

Contains type aliases.

Currently:

```python
DocID = str
Text = str
ASTNode = Union[
    Tuple[str, str],
    Tuple[str, "ASTNode"],
    Tuple[str, "ASTNode", "ASTNode"],
]
```

Keep this module to improve domain documentation and readability.

---

## Main Indexing Flow

When this runs:

```python
engine.add_document("001", "python fastapi backend")
```

Expected flow:

```text
BooleanEngine.add_document
        ↓
InvertedIndex.add_document
        ↓
Tokenizer.tokenize
        ↓
Normalizer.normalize
        ↓
InvertedIndex.index[token].add(doc_id)
```

---

## Main Search Flow

When this runs:

```python
engine.search("python AND fastapi")
```

Expected flow:

```text
BooleanEngine.search
        ↓
BooleanParser.parse
        ↓
Lark parse tree
        ↓
_Transformer
        ↓
       AST
        ↓
BooleanEvaluator.evaluate
        ↓
InvertedIndex.get
        ↓
set[str]
        ↓
sorted list[str]
```

---

## Expected Public API

The main user-facing interface must be `BooleanEngine`.

Example:

```python
from boolean_ir import BooleanEngine

engine = BooleanEngine()

engine.add_documents({
    "001": "python fastapi backend",
    "002": "django orm templates",
    "003": "python boolean search engine",
})

results = engine.search("python")
print(results)
```

Expected result:

```python
["001", "003"]
```

---

## Rules for AI Agents

When modifying this project, follow these rules:

1. Keep the project simple.
2. Do not add unnecessary dependencies.
3. Do not mix this Boolean engine with TF-IDF, BM25, or embeddings.
4. Preserve separation of responsibilities between modules.
5. Do not move parsing logic into the engine.
6. Do not move evaluation logic into the parser.
7. Do not move tokenization logic into the index.
8. Keep `BooleanEngine` as the main facade.
9. Prefer small functions and classes.
10. Avoid overengineering.

---

## Code Style

Use modern Python with type hints.

Prefer:

```python
def search(self, query: str) -> list[str]:
    ...
```

Avoid ambiguous untyped code when the domain matters.

Recommended names:

- `doc_id`
- `content`
- `query`
- `tokens`
- `ast`
- `node`
- `all_docs`

Keep names explicit and close to the Information Retrieval domain.

---

## AST Conventions

The current AST uses tuples.

Do not change it to classes without a strong reason and without adapting tests.

Expected format:

### WORD

```python
("WORD", "python")
```

### AND

```python
("AND", left_node, right_node)
```

### OR

```python
("OR", left_node, right_node)
```

### NOT

```python
("NOT", node)
```

---

## Parsing Rules

The grammar must accept:

```text
python
python AND fastapi
python OR django
NOT python
python AND NOT django
python AND (fastapi OR django)
```

The grammar must reject:

```text
AND python
python OR
python AND AND django
python (
)
```

For an invalid query, raise:

```python
InvalidQueryError
```

---

## Boolean Evaluation Rules

Results must be handled internally as `set[str]`.

The public output of `BooleanEngine.search()` must be a sorted list:

```python
return sorted(result)
```

This keeps results deterministic and tests reproducible.

---

## Design Principles

This project must prioritize:

- Clarity.
- Simplicity.
- Separation of responsibilities.
- Testable code.
- Deterministic results.
- Low coupling.
- Low cognitive cost.

The engine must be easy to read, easy to explain, and easy to extend without breaking its Boolean core.

---

## Stopwords and Stemming

- Use NLTK for stemming.
- Stopword lists used by the project live locally in `text_processor/stop_words/`.
- Create and maintain the `text_processor/` package.
- The `normalizer.py` and `textProcessor.py` modules live in that package.
- `normalizer.py` must collaborate with `textProcessor.py`.

Conceptual shape:

```python
from nltk.stem.snowball import SnowballStemmer

class TextProcessor:
    def __init__(self, language: str = "spanish"):
        self.language = language
        self.stemmer = SnowballStemmer(language)

    def process(self, ...):
        """All processing code goes here."""
        ...
        tokens = self.remove_stopwords(tokens)
        tokens = self.stem_tokens(tokens)
        return tokens
```

Example input:

```python
text = "Errores en servidores nginx y configuracion de bases de datos"
```

Approximate output:

```python
["error", "servidor", "nginx", "configur", "bas", "dat"]
```

---

## Boolean IR Support for Other Languages

- By default, this project supports Boolean IR for Spanish, English, and Portuguese.
- The central code for multilingual processing must live in `text_processor/`.
- Stopword lists for different languages live in `text_processor/stop_words/`.
- Language modules must follow the same structure, for example `english.py`, `portuguese.py`, `spanish.py`.
- To add support for new languages, always use this structure.

Suggested configuration pattern inside `TextProcessor`:

```python
from .stop_words import (
    SPANISH_STOPWORDS,
    PORTUGUESE_STOPWORDS,
    ENGLISH_STOPWORDS,
)

LANG_CONFIG = {
    "spanish": SPANISH_STOPWORDS,
    "portuguese": PORTUGUESE_STOPWORDS,
    "english": ENGLISH_STOPWORDS,
}

class TextProcessor:
    def __init__(
        self,
        language: str = "spanish",
        remove_stopwords: bool = False,
        stemming: bool = False,
    ):
        ...
```

The language must be configurable when instantiating `BooleanEngine`:

```python
from boolean_ir import BooleanEngine

engine = BooleanEngine(stopwords=True, Stemming=True, language="spanish")
engine = BooleanEngine(stopwords=True, Stemming=False, language="portuguese")
engine = BooleanEngine(stopwords=False, Stemming=False, language="english")
```

---

## Testing Instructions

This project uses `pytest` for testing and Poetry to run the project environment.

Before delivering changes, always run:

```bash
poetry run pytest -q
```

For focused test runs:

```bash
poetry run pytest -q tests/test_parser.py
poetry run pytest -q tests/test_engine.py
poetry run pytest -q tests/test_index.py
poetry run pytest -q tests/test_edge_cases.py
poetry run pytest -q tests/test_txt_loader.py
```

### Current Test Organization

- `tests/test_parser.py`: covers Boolean grammar, precedence, expected AST, parser errors, and invalid queries.
- `tests/test_engine.py`: covers the public `BooleanEngine` API, indexing, search, document removal, normalization, stopwords, stemming, and supported languages.
- `tests/test_index.py`: covers direct inverted-index behavior, repeated words, and stopword absence in the index.
- `tests/test_edge_cases.py`: covers empty queries, unknown terms, `NOT` behavior, empty corpora, and precedence edge cases.
- `tests/test_txt_loader.py`: covers `.txt` file loading, missing files, empty files, UTF-8 content, and extension control.

### Rules for New Tests

When modifying parsing:

- Add or update tests in `tests/test_parser.py`.
- Verify the exact tuple-based AST.
- Keep invalid cases raising `InvalidQueryError`.
- Verify the global parser-error message when parser errors are involved.

When modifying search, indexing, normalization, or text processing:

- Add or update tests in `tests/test_engine.py`, `tests/test_index.py`, or `tests/test_edge_cases.py`, depending on the behavior.
- Always verify public output as an ordered `list[str]`.
- Cover both indexed documents and queries when processing applies to both paths.

When modifying stopwords, stemming, or language support:

- Test at least one case with `stopwords=True`.
- Test at least one case with `stemming=True` or `Stemming=True`.
- Test that processing applies to both indexed documents and the query.
- Keep coverage for the default supported languages: `spanish`, `english`, and `portuguese`.
- If adding a new language, add its file under `boolean_ir/text_processor/stop_words/`, register it in `LANG_CONFIG`, and add specific tests.

When modifying `.txt` loaders:

- Add or update tests in `tests/test_txt_loader.py`.
- Keep support limited to `.txt` files for simplicity.
- Verify missing files, empty files, UTF-8 content, and non-`.txt` extension rejection.

### Important Considerations

- Do not rely on nondeterministic results: `BooleanEngine.search()` must return `sorted(result)`.
- Do not add tests that require network access, corpus downloads, or external services.
- Stopwords used by the project must live in `boolean_ir/text_processor/stop_words/`.
- NLTK is used for stemming; tests must not require downloading additional NLTK data.
- Keep tests simple, direct, and close to the public behavior of the engine.
