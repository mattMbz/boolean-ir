import re
from .normalizer import Normalizer
from .text_processor import TextProcessor


class Tokenizer:
    def __init__(
        self,
        normalizer: Normalizer,
        text_processor: TextProcessor | None = None,
    ):
        self.normalizer = normalizer
        self.text_processor = text_processor

    def tokenize(self, text: str) -> list[str]:
        text = self.normalizer.normalize(text)
        tokens = re.findall(r"\w+", text)

        if self.text_processor is not None:
            tokens = self.text_processor.process(tokens)

        return tokens
