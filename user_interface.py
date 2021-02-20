import cmd

import commands
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
        self._commands = self._build_command_dict()

    def has_session(self) -> bool:
        return self._client_session is not None

    @raises_command_exceptions
    def do_connect(self, arguments: str) -> None:
        """Creates client session connecting to given address for other commands to use."""
        new_session = self._commands["connect"].execute(arguments)
        self._client_session = new_session
        print(f"Established connection to {self._client_session.get_address()}")

    @requires_session
    @raises_command_exceptions
    def do_get_modification_time(self, arguments: str) -> None:
        """Prints the last modification timestamp of the Server."""
        command = self._commands["get_modification_time"]
        modification_time = command.execute(arguments, self._client_session)
        print(f"Last Server modification time: {modification_time}")

    @requires_session
    @raises_command_exceptions
    def do_create_task(self, arguments: str) -> None:
        """Sends Task creation request to the Server."""
        created_task_id = self._commands["create_task"].execute(arguments, self._client_session)
        print(f"Created new Task with id: {created_task_id}")

    @requires_session
    @raises_command_exceptions
    def do_get_robots(self, arguments: str) -> None:
        """Requests the list of known robots and prints it."""
        robot_dict = self._commands["get_robots"].execute(arguments, self._client_session)
        print(robot_dict)

    @requires_session
    @raises_command_exceptions
    def do_get_task(self, arguments: str) -> None:
        """Requests one Task by its id and prints it."""
        task = self._commands["get_task"].execute(arguments, self._client_session)
        print(task.__dict__)

    @requires_session
    @raises_command_exceptions
    def do_get_many_tasks(self, arguments: str) -> None:
        """Queries Tasks using given filter parameters and prints them."""
        task_list = self._commands["get_many_tasks"].execute(arguments, self._client_session)
        for task in task_list:
            print(task.__dict__)

    def do_exit(self, _) -> None:
        """Sets the exit flag, resulting in program termination. Ignores any arguments."""
        self._was_exit_called = True

    def do_help(self, arg: str) -> None:
        """Displays command list"""
        def print_command(name: str, description: str) -> None:
            print(f"* {name}\n    {description}")

        print("Available commands")
        print("------------------")
        print("\nUse \"command -h\" to get usage details for a command.\n")
        for command_name, command_object in self._commands.items():
            print_command(command_name, command_object.get_description())
        print_command("help", "Displays this message.")
        print_command("exit", "Sets the exit flag, resulting in program termination.")

    def postcmd(self, _1: bool, _2: str) -> bool:
        """Triggers main interface loop termination if exit flag was set. Overridden method."""
        if self._was_exit_called:
            print("Goodbye!")
        else:
            print()
        return self._was_exit_called

    @staticmethod
    def __make_welcome_message() -> str:
        message = "\nRobot Test API Demo\n"
        message += "-------------------\n"
        message += "Use the \"connect\" command to establish connection to a test server.\n"
        message += "Type \"help\" to see the list of all available commands.\n"
        message += "Use \"command -h\" to get usage details for a command.\n"
        return message

    @staticmethod
    def _build_command_dict() -> dict:
        return {"connect": commands.Connect(),
                "get_modification_time": commands.GetModificationTime(),
                "get_robots": commands.GetRobots(),
                "create_task": commands.CreateTask(),
                "get_task": commands.GetTask(),
                "get_many_tasks": commands.GetManyTasks(),
                }
