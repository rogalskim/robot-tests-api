from client_session import ClientSession
from commands.command_base import CommandBase
from task import Task


class GetTask(CommandBase):
    def __init__(self) -> None:
        super().__init__("Requests one Task by its id and prints it.")
        self._parser.add_argument("task_id",
                                  help="The unique identifier of the requested Task",
                                  type=int)

    def execute(self, arguments: str, session: ClientSession) -> Task:
        parsed_arguments = self._parser.parse_args(arguments.split())
        return session.get_task(parsed_arguments.task_id, parsed_arguments.fail)
