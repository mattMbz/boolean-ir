import pytest

from boolean_ir.exceptions import InvalidQueryError
from boolean_ir.parser import BooleanParser


@pytest.fixture
def parser() -> BooleanParser:
    return BooleanParser()


def test_parse_single_word(parser: BooleanParser) -> None:
    ast = parser.parse("python")
    assert ast == ("WORD", "python")


def test_parse_word_is_normalized_to_lowercase(parser: BooleanParser) -> None:
    ast = parser.parse("PYTHON")
    assert ast == ("WORD", "python")


def test_parse_and_expression(parser: BooleanParser) -> None:
    ast = parser.parse("python AND fastapi")
    assert ast == ("AND", ("WORD", "python"), ("WORD", "fastapi"))


def test_parse_or_expression(parser: BooleanParser) -> None:
    ast = parser.parse("python OR django")
    assert ast == ("OR", ("WORD", "python"), ("WORD", "django"))


def test_parse_not_expression(parser: BooleanParser) -> None:
    ast = parser.parse("NOT django")
    assert ast == ("NOT", ("WORD", "django"))


def test_parse_parentheses_expression(parser: BooleanParser) -> None:
    ast = parser.parse("(python AND fastapi) OR django")
    assert ast == (
        "OR",
        ("AND", ("WORD", "python"), ("WORD", "fastapi")),
        ("WORD", "django"),
    )


def test_parse_operator_precedence(parser: BooleanParser) -> None:
    ast = parser.parse("python OR fastapi AND django")
    assert ast == (
        "OR",
        ("WORD", "python"),
        ("AND", ("WORD", "fastapi"), ("WORD", "django")),
    )


def test_parse_nested_not(parser: BooleanParser) -> None:
    ast = parser.parse("NOT NOT python")
    assert ast == ("NOT", ("NOT", ("WORD", "python")))


def test_parse_word_with_numbers_and_underscore(parser: BooleanParser) -> None:
    ast = parser.parse("doc_2025")
    assert ast == ("WORD", "doc_2025")


def test_parse_invalid_double_and_raises_error(parser: BooleanParser) -> None:
    with pytest.raises(InvalidQueryError):
        parser.parse("python AND AND fastapi")


def test_parse_invalid_leading_operator_raises_error(parser: BooleanParser) -> None:
    with pytest.raises(InvalidQueryError):
        parser.parse("AND python")


def test_parse_invalid_unclosed_parenthesis_raises_error(parser: BooleanParser) -> None:
    with pytest.raises(InvalidQueryError):
        parser.parse("(python OR django")


def test_parse_invalid_empty_string_raises_error(parser: BooleanParser) -> None:
    with pytest.raises(InvalidQueryError):
        parser.parse("")


def test_parse_invalid_only_parenthesis_raises_error(parser: BooleanParser) -> None:
    with pytest.raises(InvalidQueryError):
        parser.parse("()")


def test_parse_invalid_symbol_raises_error(parser: BooleanParser) -> None:
    with pytest.raises(InvalidQueryError):
        parser.parse("python & django")


def test_invalid_query_error_has_global_parser_message(parser: BooleanParser) -> None:
    with pytest.raises(InvalidQueryError) as exc_info:
        parser.parse("python AND AND fastapi")

    assert str(exc_info.value).startswith(InvalidQueryError.DEFAULT_MESSAGE)


def test_invalid_query_error_includes_specific_cause_when_available(
    parser: BooleanParser,
) -> None:
    with pytest.raises(InvalidQueryError) as exc_info:
        parser.parse("python & django")

    message = str(exc_info.value)
    assert "Cause:" in message
    assert "No terminal matches" in message
