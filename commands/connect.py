from commands.command_base import CommandBase


class Connect(CommandBase):
    def __init__(self):
        super().__init__()
        self._parser.add_argument("--address",
                                  help="IP address or host name of the test server.",
                                  default="192.168.1.2")
        self._parser.add_argument("--port",
                                  help="Port number of the test server to send requests to.",
                                  type=int,
                                  default=5000)

    def execute(self, arguments: str) -> tuple:
        super().execute(arguments)

        if self._parsed_arguments is None:
            return None, None

        return self._parsed_arguments.address, self._parsed_arguments.port
