from .normalizer import Normalizer
from .tokenizer import Tokenizer
from .index import InvertedIndex
from .parser import BooleanParser
from .evaluator import BooleanEvaluator
from .text_processor import TextProcessor
from .types import ASTNode


class BooleanEngine:
    def __init__(
        self,
        stopwords: bool = False,
        stemming: bool = False,
        Stemming: bool | None = None,
        language: str = "spanish",
    ):
        if Stemming is not None:
            stemming = Stemming

        self.stopwords = stopwords
        self.stemming = stemming
        self.language = language
        self.normalizer = Normalizer()
        self.query_normalizer = Normalizer(lowercase=False)
        self.text_processor = TextProcessor(
            language=language,
            remove_stopwords=stopwords,
            stemming=stemming,
        )
        self.tokenizer = Tokenizer(self.normalizer, self.text_processor)
        self.index = InvertedIndex(self.tokenizer)
        self.parser = BooleanParser()
        self.evaluator = BooleanEvaluator(self.index)
        self.doc_ids = set()

    def add_document(self, doc_id: str, content: str):
        self.index.add_document(doc_id, content)
        self.doc_ids.add(doc_id)

    def add_documents(self, docs: dict[str, str]):
        for doc_id, content in docs.items():
            self.add_document(doc_id, content)

    def remove_document(self, doc_id: str):
        self.index.remove_document(doc_id)
        self.doc_ids.discard(doc_id)

    def search(self, query: str) -> list[str]:
        query = self.query_normalizer.normalize(query)
        ast = self.parser.parse(query)
        ast = self._process_query_ast(ast)
        result = self.evaluator.evaluate(ast, self.doc_ids)
        return sorted(result)

    def _process_query_ast(self, node: ASTNode) -> ASTNode:
        node_type = node[0]

        if node_type == "WORD":
            tokens = self.text_processor.process([node[1]])
            term = tokens[0] if tokens else ""
            return ("WORD", term)

        if node_type == "NOT":
            return ("NOT", self._process_query_ast(node[1]))

        if node_type in {"AND", "OR"}:
            return (
                node_type,
                self._process_query_ast(node[1]),
                self._process_query_ast(node[2]),
            )

        return node
