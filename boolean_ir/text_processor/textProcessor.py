from nltk.stem.snowball import SnowballStemmer

from ..exceptions import UnsupportedLanguageError
from .normalizer import Normalizer
from .stop_words import LANG_CONFIG, SUPPORTED_LANGUAGES


class TextProcessor:
    def __init__(
        self,
        language: str = "spanish",
        remove_stopwords: bool = False,
        stemming: bool = False,
    ):
        language = self._normalize_language(language)
        self.language = language
        self.remove_stopwords_enabled = remove_stopwords
        self.stemming_enabled = stemming
        self.normalizer = Normalizer()
        self.stop_words = self._load_stopwords()
        self.stemmer = SnowballStemmer(language)

    def process(self, tokens: list[str]) -> list[str]:
        if self.remove_stopwords_enabled:
            tokens = self.remove_stopwords(tokens)

        if self.stemming_enabled:
            tokens = self.stem_tokens(tokens)

        return tokens

    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        return [token for token in tokens if token not in self.stop_words]

    def stem_tokens(self, tokens: list[str]) -> list[str]:
        return [self.stemmer.stem(token) for token in tokens]

    def _load_stopwords(self) -> set[str]:
        words = LANG_CONFIG[self.language]
        return {self.normalizer.normalize(word) for word in words}

    def _normalize_language(self, language: str) -> str:
        language = language.lower().strip()

        if language not in LANG_CONFIG:
            supported = ", ".join(SUPPORTED_LANGUAGES)
            raise UnsupportedLanguageError(
                f"Unsupported language '{language}'. Supported languages: {supported}."
            )

        return language
