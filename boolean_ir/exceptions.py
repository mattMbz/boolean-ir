class BooleanRIError(Exception):
    pass


class InvalidQueryError(BooleanRIError):
    DEFAULT_MESSAGE = "Parser error: invalid or inappropriate query."

    def __init__(self, cause: str | None = None):
        self.cause = cause.strip() if cause else None
        message = self.DEFAULT_MESSAGE

        if self.cause:
            message = f"{message} Cause: {self.cause}"

        super().__init__(message)


class UnsupportedLanguageError(BooleanRIError):
    pass
