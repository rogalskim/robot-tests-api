import cmd

from commands.connect import Connect
from commands.exceptions import ParserExitWarning
from client_session import ClientSession


class UserInterface(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "> "
        self.ruler = '-'
        self.intro = self.__make_welcome_message()
        self._was_exit_called = False
        self._client_session = None

    def do_connect(self, arguments: str) -> None:
        """Sets the address of the test server and checks the connection."""
        try:
            new_session = Connect().execute(arguments)
        except ParserExitWarning:
            return

        if new_session is not None:
            self._client_session = new_session
            print(f"Established connection to {self._client_session.get_address()}")
        else:
            print(f"Failed to establish connection to server.")

    def do_exit(self, _) -> None:
        """Sets the exit flag, resulting in program termination."""
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
        message += "Type \"help\" to see the list of available commands.\n"
        return message
