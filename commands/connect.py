from typing import Optional

from commands.command_base import CommandBase
from commands.exceptions import ParserExitWarning
from client_session import ClientSession, ConnectionFailed


class Connect(CommandBase):
    def __init__(self):
        super().__init__()
        self._parser.add_argument("-a", "--host", "--address",
                                  help="Host address or name of the test server.",
                                  default="192.168.1.2")
        self._parser.add_argument("-p", "--port",
                                  help="Port number of the test server to send requests to.",
                                  type=int,
                                  default=5000)

    def execute(self, arguments: str) -> Optional[ClientSession]:
        super().execute(arguments)

        if self._parsed_arguments is None:
            raise ParserExitWarning

        try:
            session = ClientSession(self._parsed_arguments.host, self._parsed_arguments.port)
        except ConnectionFailed:
            return None

        return session
