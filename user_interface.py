import cmd

from commands.connect import Connect
from commands.create_task import CreateTask
from commands.get_modification_time import GetModificationTime
from commands.get_robots import GetRobots
from exceptions import ExecutionError, ParserExitWarning, ParsingError


def requires_session(method):
    """UserInterface method wrapper for checking if a client session was created."""
    def check_session_before_call(*args):
        user_interface = args[0]
        if not user_interface.has_session():
            print("Server connection required. Call \"connect\" first.")
            return
        else:
            return method(*args)

    return check_session_before_call


def raises_command_exceptions(method):
    """UserInterface method wrapper for handling shared command exceptions."""
    def handle_method_exceptions(*args):
        try:
            method(*args)
        except ParserExitWarning:
            return
        except ParsingError:
            print(f"Invalid command arguments; type \"command --help\" for usage details.")
        except ExecutionError as exception:
            print(exception.message)

    return handle_method_exceptions


class UserInterface(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "> "
        self.ruler = '-'
        self.intro = self.__make_welcome_message()
        self._was_exit_called = False
        self._client_session = None

    def has_session(self) -> bool:
        return self._client_session is not None

    @raises_command_exceptions
    def do_connect(self, arguments: str) -> None:
        """Creates client session connecting to given address for other commands to use."""
        new_session = Connect().execute(arguments)
        self._client_session = new_session
        print(f"Established connection to {self._client_session.get_address()}")

    @requires_session
    @raises_command_exceptions
    def do_get_modification_time(self, arguments: str) -> None:
        """Prints the last modification timestamp of the Server."""
        modification_time = GetModificationTime().execute(arguments, self._client_session)
        print(f"Last Server modification time: {modification_time}")

    @requires_session
    @raises_command_exceptions
    def do_create_task(self, arguments: str) -> None:
        """Sends Task creation request to the Server."""
        created_task_id = CreateTask().execute(arguments, self._client_session)
        print(f"Created new Task with id: {created_task_id}")

    @requires_session
    @raises_command_exceptions
    def do_get_robots(self, arguments: str) -> None:
        """Requests the list of known robots and prints it."""
        robot_dict = GetRobots().execute(arguments, self._client_session)
        print(robot_dict)

    def do_exit(self, _) -> None:
        """Sets the exit flag, resulting in program termination. Ignores any arguments."""
        self._was_exit_called = True

    def postcmd(self, _1: bool, _2: str) -> bool:
        """Triggers main interface loop termination if exit flag was set. Overridden method."""
        if self._was_exit_called:
            print("Goodbye!")
        return self._was_exit_called

    @staticmethod
    def __make_welcome_message() -> str:
        message = "\nRobot Test API Demo\n"
        message += "-------------------\n"
        message += "Use the \"connect\" command to establish connection to a test server.\n"
        message += "Type \"help\" to see the list of all available commands.\n"
        message += "Use \"command -h\" to get usage details for a command.\n"
        return message
