import pytest

from boolean_ri import BooleanEngine
from boolean_ri.exceptions import InvalidQueryError


@pytest.fixture
def engine() -> BooleanEngine:
    engine = BooleanEngine()
    engine.add_documents(
        {
            "D1": "python fastapi backend",
            "D2": "django templates backend",
            "D3": "nginx reverse proxy",
        }
    )
    return engine


def test_empty_query_raises_invalid_query_error(engine: BooleanEngine) -> None:
    with pytest.raises(InvalidQueryError):
        engine.search("")


def test_whitespace_only_query_raises_invalid_query_error(engine: BooleanEngine) -> None:
    with pytest.raises(InvalidQueryError):
        engine.search("   ")


def test_unknown_term_returns_empty_list(engine: BooleanEngine) -> None:
    assert engine.search("kubernetes") == []


def test_not_over_unknown_term_returns_entire_corpus(engine: BooleanEngine) -> None:
    assert engine.search("NOT kubernetes") == ["D1", "D2", "D3"]


def test_not_over_existing_term_excludes_matching_documents(engine: BooleanEngine) -> None:
    assert engine.search("NOT backend") == ["D3"]


def test_search_on_empty_corpus_returns_empty_list() -> None:
    engine = BooleanEngine()
    assert engine.search("python") == []
    assert engine.search("NOT python") == []


def test_not_has_higher_precedence_than_and(engine: BooleanEngine) -> None:
    assert engine.search("backend AND NOT django") == ["D1"]
