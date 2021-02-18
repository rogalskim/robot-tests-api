class ParsingError(RuntimeError):
    pass


class ParserExitWarning(RuntimeWarning):
    pass


class ExecutionError(RuntimeError):
    def __init__(self, message: str) -> None:
        self.message = message
