from lark import Lark, Transformer
from .exceptions import InvalidQueryError

grammar = r"""
?start: expr

?expr: expr "OR" term   -> or_op
     | term

?term: term "AND" factor -> and_op
     | factor

?factor: "NOT" factor    -> not_op
       | WORD            -> word
       | "(" expr ")"

WORD: /(?!AND\b|OR\b|NOT\b)[a-zA-Z0-9_]+/

%import common.WS
%ignore WS
"""

_parser = Lark(grammar, start="start", parser="lalr")


class _Transformer(Transformer):
    def word(self, items):
        return ("WORD", str(items[0]).lower())

    def and_op(self, items):
        return ("AND", items[0], items[1])

    def or_op(self, items):
        return ("OR", items[0], items[1])

    def not_op(self, items):
        return ("NOT", items[0])


class BooleanParser:
    def parse(self, query: str):
        try:
            tree = _parser.parse(query)
            return _Transformer().transform(tree)
        except Exception as e:
            raise InvalidQueryError(str(e)) from e
