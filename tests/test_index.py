from boolean_ir.index import InvertedIndex
from boolean_ir.normalizer import Normalizer
from boolean_ir.text_processor import TextProcessor
from boolean_ir.tokenizer import Tokenizer


def make_index(stopwords: bool = False) -> InvertedIndex:
    normalizer = Normalizer()
    text_processor = TextProcessor(remove_stopwords=stopwords)
    tokenizer = Tokenizer(normalizer, text_processor)
    return InvertedIndex(tokenizer)


def test_index_adds_terms_with_document_ids() -> None:
    index = make_index()

    index.add_document("D1", "python fastapi backend")
    index.add_document("D2", "python django templates")

    assert index.get("python") == {"D1", "D2"}
    assert index.get("fastapi") == {"D1"}
    assert index.get("django") == {"D2"}


def test_repeated_words_are_indexed_once_per_document() -> None:
    index = make_index()

    index.add_document("D1", "python python python fastapi")

    assert index.get("python") == {"D1"}
    assert index.index["python"] == {"D1"}


def test_stopwords_do_not_appear_in_inverted_index() -> None:
    index = make_index(stopwords=True)

    index.add_document("D1", "error en servidor nginx y configuracion")

    assert "en" not in index.index
    assert "y" not in index.index
    assert index.get("error") == {"D1"}
    assert index.get("servidor") == {"D1"}
    assert index.get("nginx") == {"D1"}
