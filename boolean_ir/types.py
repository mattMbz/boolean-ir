from typing import Dict, Set, Tuple, Union

DocID = str
Text = str

ASTNode = Union[
    Tuple[str, str],          # WORD
    Tuple[str, "ASTNode"],    # NOT
    Tuple[str, "ASTNode", "ASTNode"],  # AND / OR
]