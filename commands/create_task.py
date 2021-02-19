from client_session import ClientSession
from commands.command_base import CommandBase


class CreateTask(CommandBase):
    def __init__(self):
        super().__init__("Sends Task creation request to the Server.")
        self._parser.add_argument("robot",
                                  help="Display name of the robot to create the Task for.")
        self._parser.add_argument("branch",
                                  help="Name of the Git branch containing the robot configuration.")
        self._parser.add_argument("runs",
                                  type=int,
                                  help="The requested number of evaluation runs.")

    def execute(self, arguments: str, session: ClientSession) -> int:
        """:returns Task id of the created Task"""
        parsed_arguments = self._parser.parse_args(arguments.split())
        return session.request_task_creation(parsed_arguments.robot,
                                             parsed_arguments.branch,
                                             parsed_arguments.runs,
                                             parsed_arguments.fail)
