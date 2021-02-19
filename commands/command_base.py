import argparse
from typing import NoReturn

from exceptions import ParsingError
from exceptions import ParserExitWarning


class CalmerParser(argparse.ArgumentParser):
    """Throws exceptions instead of killing the process."""

    def exit(self, _1=..., _2=...) -> NoReturn:
        raise ParserExitWarning

    def error(self, _1) -> NoReturn:
        raise ParsingError


class CommandBase:
    def __init__(self, description: str) -> None:
        self._parser = CalmerParser()
        self._parser.description = description
        self._parser.add_argument("-f", "--fail",
                                  help="Cause the mock API to reject the command's HTTP request.",
                                  action="store_true",
                                  default=False)

    def get_description(self) -> str:
        return self._parser.description
