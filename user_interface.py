import cmd

from commands.connect import Connect


class UserInterface(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "> "
        self.ruler = '-'
        self.intro = self.__make_welcome_message()
        self.was_exit_called = False

    def do_connect(self, arguments: str) -> None:
        """Sets the address of the target test server and queries last update time."""
        address, port = Connect().execute(arguments)
        print(f"{address}:{port}")

    def do_exit(self, _) -> None:
        """Sets the exit flag, resulting in program termination."""
        self.was_exit_called = True

    def postcmd(self, _1: bool, _2: str) -> bool:
        """Triggers main interface loop termination if exit flag was set. Overridden method."""
        if self.was_exit_called:
            print("Goodbye!")
        return self.was_exit_called

    @staticmethod
    def __make_welcome_message() -> str:
        message = "\nRobot Test API Demo\n"
        message += "-------------------\n"
        message += "Use the \"connect\" command to establish connection to a test server.\n"
        message += "Type \"help\" to see the list of available commands.\n"
        return message
