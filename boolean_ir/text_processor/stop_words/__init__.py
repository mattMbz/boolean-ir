from .english import ENGLISH_STOPWORDS
from .portuguese import PORTUGUESE_STOPWORDS
from .spanish import SPANISH_STOPWORDS

LANG_CONFIG = {
    "spanish": SPANISH_STOPWORDS,
    "portuguese": PORTUGUESE_STOPWORDS,
    "english": ENGLISH_STOPWORDS,
}

SUPPORTED_LANGUAGES = tuple(LANG_CONFIG.keys())

__all__ = [
    "ENGLISH_STOPWORDS",
    "LANG_CONFIG",
    "PORTUGUESE_STOPWORDS",
    "SPANISH_STOPWORDS",
    "SUPPORTED_LANGUAGES",
]
