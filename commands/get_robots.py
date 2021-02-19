from client_session import ClientSession
from commands.command_base import CommandBase


class GetRobots(CommandBase):
    def __init__(self) -> None:
        super().__init__("Requests the list of known robots and prints it.")

    def execute(self, arguments: str, session: ClientSession) -> dict:
        parsed_arguments = self._parser.parse_args(arguments.split())
        return session.get_robot_dict(simulate_failure=parsed_arguments.fail)
