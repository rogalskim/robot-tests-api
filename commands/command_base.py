from abc import ABC
from abc import abstractmethod
import argparse
from typing import NoReturn

from commands.exceptions import ParsingError
from commands.exceptions import ParserExitWarning


class CalmerParser(argparse.ArgumentParser):
    """Throws exceptions instead of killing the process."""

    def exit(self, _1=..., _2=...) -> NoReturn:
        raise ParserExitWarning

    def error(self, _1) -> NoReturn:
        raise ParsingError


class CommandBase(ABC):
    def __init__(self):
        self._parser = CalmerParser()
        self._parsed_arguments = None

    @abstractmethod
    def execute(self, arguments: str) -> None:
        try:
            self._parsed_arguments = self._parser.parse_args(arguments.split())
        except ParserExitWarning:
            return
        except ParsingError:
            print(f"Invalid command arguments; type \"command --help\" for usage details.")
            return
