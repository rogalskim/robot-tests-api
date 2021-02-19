from client_session import ClientSession
from commands.command_base import CommandBase


class GetModificationTime(CommandBase):
    def __init__(self) -> None:
        super().__init__("Prints the last modification timestamp of the Server.")

    def execute(self, arguments: str, session: ClientSession) -> int:
        parsed_arguments = self._parser.parse_args(arguments.split())
        return session.get_server_modification_time(simulate_failure=parsed_arguments.fail)
