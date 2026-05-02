import unicodedata


class Normalizer:
    def __init__(self, lowercase: bool = True, strip_accents: bool = True):
        self.lowercase = lowercase
        self.strip_accents = strip_accents

    def normalize(self, text: str) -> str:
        if self.lowercase:
            text = text.lower()

        if self.strip_accents:
            text = "".join(
                c
                for c in unicodedata.normalize("NFD", text)
                if unicodedata.category(c) != "Mn"
            )

        return text
