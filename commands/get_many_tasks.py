from client_session import ClientSession
from commands.command_base import CommandBase


class GetManyTasks(CommandBase):
    def __init__(self):
        super().__init__("Queries Tasks using given filter parameters and prints them.")
        self._parser.add_argument("-r", "--robot",
                                  help="Will return only the Tasks assigned to given Robot name.")
        self._parser.add_argument("-s", "--status",
                                  help="Will return only the Tasks with given status.",
                                  choices=["waiting", "running", "finished"])

    def execute(self, arguments: str, session: ClientSession) -> list:
        parsed_arguments = self._parser.parse_args(arguments.split())
        return session.get_many_tasks(parsed_arguments.robot,
                                      parsed_arguments.status,
                                      parsed_arguments.fail)
