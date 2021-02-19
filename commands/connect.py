from commands.command_base import CommandBase
from client_session import ClientSession


class Connect(CommandBase):
    def __init__(self):
        super().__init__(
            "Creates client session connecting to given address for other commands to use.")
        self._parser.add_argument("-a", "--host", "--address",
                                  help="Host address or name of the test server.",
                                  default="192.168.1.2")
        self._parser.add_argument("-p", "--port",
                                  help="Port number of the test server to send requests to.",
                                  type=int,
                                  default=5000)

    def execute(self, arguments: str) -> ClientSession:
        parsed_arguments = self._parser.parse_args(arguments.split())
        return ClientSession(parsed_arguments.host,
                             parsed_arguments.port,
                             parsed_arguments.fail)
