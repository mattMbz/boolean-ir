from collections import defaultdict
from .tokenizer import Tokenizer


class InvertedIndex:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.index = defaultdict(set)

    def add_document(self, doc_id: str, content: str):
        tokens = set(self.tokenizer.tokenize(content))

        for token in tokens:
            self.index[token].add(doc_id)

    def remove_document(self, doc_id: str):
        for term in list(self.index.keys()):
            if doc_id in self.index[term]:
                self.index[term].remove(doc_id)
                if not self.index[term]:
                    del self.index[term]

    def get(self, term: str):
        return self.index.get(term, set())
