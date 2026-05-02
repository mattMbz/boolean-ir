import pytest

from boolean_ri import BooleanEngine
from boolean_ri.exceptions import InvalidQueryError, UnsupportedLanguageError


@pytest.fixture
def engine() -> BooleanEngine:
    engine = BooleanEngine()
    engine.add_documents(
        {
            "D1": "error en servidor nginx",
            "D2": "configuracion de nginx",
            "D3": "error en base de datos",
            "D4": "python fastapi backend",
            "D5": "django orm templates",
            "D6": "python boolean search engine",
        }
    )
    return engine


def test_add_documents_and_simple_and_query(engine: BooleanEngine) -> None:
    assert engine.search("error AND nginx") == ["D1"]


def test_or_query(engine: BooleanEngine) -> None:
    result = engine.search("nginx OR database")
    assert result == ["D1", "D2"]


def test_not_query(engine: BooleanEngine) -> None:
    result = engine.search("python AND NOT django")
    assert result == ["D4", "D6"]


def test_parentheses_query(engine: BooleanEngine) -> None:
    result = engine.search("(error AND nginx) OR database")
    assert result == ["D1"]


def test_single_word_query(engine: BooleanEngine) -> None:
    assert engine.search("django") == ["D5"]


def test_unknown_term_returns_empty_list(engine: BooleanEngine) -> None:
    assert engine.search("kubernetes") == []


def test_remove_document(engine: BooleanEngine) -> None:
    engine.remove_document("D1")
    assert engine.search("error AND nginx") == []


def test_add_single_document_after_init(engine: BooleanEngine) -> None:
    engine.add_document("D7", "nginx reverse proxy error")
    result = engine.search("error AND nginx")
    assert result == ["D1", "D7"]


def test_query_is_case_insensitive_for_terms(engine: BooleanEngine) -> None:
    # Los operadores siguen siendo AND/OR/NOT en mayúsculas según la gramática actual.
    result = engine.search("PYTHON AND NOT django")
    assert result == ["D4", "D6"]


def test_accent_normalization(engine: BooleanEngine) -> None:
    engine.add_document("D7", "configuración avanzada de sistemas")
    assert engine.search("configuracion") == ["D2", "D7"]


def test_query_is_accent_normalized_before_parsing(engine: BooleanEngine) -> None:
    engine.add_document("D7", "precio de productos")
    engine.add_document("D8", "cuantos productos hay")
    assert engine.search("precio OR cuántos") == ["D7", "D8"]


def test_stopwords_are_optional() -> None:
    engine = BooleanEngine()
    engine.add_document("D1", "error en servidor nginx")
    assert engine.search("en") == ["D1"]


def test_stopwords_are_applied_to_documents_and_queries() -> None:
    engine = BooleanEngine(stopwords=True)
    engine.add_document("D1", "error en servidor nginx")
    assert engine.search("en") == []
    assert engine.search("servidor") == ["D1"]


def test_stemming_is_applied_to_documents_and_queries() -> None:
    engine = BooleanEngine(stemming=True)
    engine.add_document("D1", "errores en servidores nginx")
    assert engine.search("error AND servidor") == ["D1"]


def test_stemming_alias_with_capital_s_is_supported() -> None:
    engine = BooleanEngine(Stemming=True)
    engine.add_document("D1", "configuracion de bases de datos")
    assert engine.search("base AND dato") == ["D1"]


def test_english_stopwords_and_stemming_are_supported() -> None:
    engine = BooleanEngine(stopwords=True, stemming=True, language="english")
    engine.add_document("D1", "running servers in production")
    assert engine.search("the") == []
    assert engine.search("run AND server") == ["D1"]


def test_portuguese_stopwords_and_stemming_are_supported() -> None:
    engine = BooleanEngine(stopwords=True, stemming=True, language="portuguese")
    engine.add_document("D1", "servidores em producao")
    assert engine.search("em") == []
    assert engine.search("servidor") == ["D1"]


def test_unsupported_language_raises_domain_error() -> None:
    with pytest.raises(UnsupportedLanguageError):
        BooleanEngine(language="italian")


def test_invalid_query_double_and_raises_error(engine: BooleanEngine) -> None:
    with pytest.raises(InvalidQueryError):
        engine.search("python AND AND fastapi")


def test_invalid_query_unclosed_parenthesis_raises_error(engine: BooleanEngine) -> None:
    with pytest.raises(InvalidQueryError):
        engine.search("(python AND fastapi")


def test_empty_query_raises_error(engine: BooleanEngine) -> None:
    with pytest.raises(InvalidQueryError):
        engine.search("")


def test_only_operator_query_raises_error(engine: BooleanEngine) -> None:
    with pytest.raises(InvalidQueryError):
        engine.search("AND")


def test_not_over_unknown_term_returns_all_documents(engine: BooleanEngine) -> None:
    result = engine.search("NOT kubernetes")
    assert result == ["D1", "D2", "D3", "D4", "D5", "D6"]
